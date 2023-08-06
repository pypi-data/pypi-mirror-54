#!/usr/bin/env python

import logging
import random
import shutil
import string
import tarfile
import tempfile
from pathlib import Path
from typing import Dict, Optional

import attr

from r2c.lib.filestore import FileStore
from r2c.lib.input import AnalyzerInput
from r2c.lib.manifest import AnalyzerOutputType
from r2c.lib.specified_analyzer import SpecifiedAnalyzer

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@attr.s(auto_attribs=True, frozen=True)
class CacheKey:
    """The key in the cache of unpacked output."""

    analyzer: SpecifiedAnalyzer
    output_type: AnalyzerOutputType = attr.ib(
        validator=attr.validators.in_(
            [AnalyzerOutputType.json, AnalyzerOutputType.filesystem]
        )
    )
    input: AnalyzerInput


@attr.s(auto_attribs=True)
class OutputStorage:
    """Copies the output of analyzers from the relevant FileStore.

    In addition, it keeps a cache on-disk to prevent repeatedly accessing the
    network.

    The cache is persistent between instances of OutputStorage.
    """

    _json_output_store: FileStore
    _filesystem_output_store: FileStore
    _cache_dir: Path

    # The value is the path on-disk of either the JSON file or the *uncompressed*
    # tarchive.
    _fetch_cache: Dict[CacheKey, Path] = attr.ib(init=False, factory=dict)

    def reset_cache(self) -> None:
        """Deletes all entries in the cache."""
        self._fetch_cache = dict()
        for child in self._cache_dir.iterdir():
            if child.is_file():
                child.unlink()
            else:
                shutil.rmtree(child)

    def upload(
        self,
        analyzer: SpecifiedAnalyzer,
        input: AnalyzerInput,
        output_type: AnalyzerOutputType,
        base_dir: Path,
    ) -> None:
        """Uploads the output of the given analyzer from the given path.

        This also adds it to the OutputStorage's cache.

        base_dir should be the *directory* that contains the output.json and/or
        fs folder.

        Note that unlike fetch(), this *does* work with AnalyzerOutputType.both
        analyzers.
        """
        if not base_dir.is_dir():
            raise ValueError(f"Argument {base_dir} to upload should be a directory")

        if output_type.has_json():
            output_file_path = base_dir / "output.json"
            logger.info(f"Uploading {output_file_path}")
            self._json_output_store.put(input, analyzer, str(base_dir / "output.json"))

            # Store it in our cache.
            cache_key = CacheKey(
                analyzer=analyzer, input=input, output_type=AnalyzerOutputType.json
            )
            cached_path = self._json_cache_path(analyzer)
            shutil.copyfile(output_file_path, cached_path)
            self._fetch_cache[cache_key] = Path(cached_path)

        if output_type.has_filesystem():
            output_dir = base_dir / "fs"
            logger.info(f"Uploading {output_dir}")
            # We create a tempdir because we want to make sure the tarchive
            # gets automatically deleted, and creating the tempfile using
            # TemporaryFile will result in it trying to unlink the wrong file.
            with tempfile.TemporaryDirectory(prefix="output-archive-") as d:
                tarfile_path = Path(d) / "output.tar.gz"
                with tarfile.open(tarfile_path, "w:gz") as tar:
                    tar.add(
                        str(output_file_path), arcname=analyzer.versioned_analyzer.name
                    )
                logger.info(f"Uploading {tarfile_path}")
                self._filesystem_output_store.put(input, analyzer, str(tarfile_path))

            # Store it in our cache.
            cache_key = CacheKey(
                analyzer=analyzer,
                input=input,
                output_type=AnalyzerOutputType.filesystem,
            )
            cached_path = self._filesystem_cache_path(analyzer)
            shutil.copytree(output_dir, cached_path)
            self._fetch_cache[cache_key] = cached_path

    def fetch_analyzer_output(
        self,
        analyzer: SpecifiedAnalyzer,
        input: AnalyzerInput,
        output_type: AnalyzerOutputType,
    ) -> Optional[Path]:
        """Gets the path to the output of an analyzer.

        If output_type is fs, this will fetch *and* extract the archive.
        Otherwise, it will just fetch it. Do not delete or modify the files
        returned from this function!

        This uses a cache to prevent repeatedly hitting the network; however,
        it will *not* cache failed lookups.

        Since this only returns a single path, if an analyzer has 'both' output
        type, you'll need to call this once with 'fs' and once with 'json'.

        Returns the path to the output on disk, or None if it couldn't be
        fetched.
        """
        if output_type == AnalyzerOutputType.both:
            # We can only return a single path; which path would we return if
            # the user asked for both?
            raise ValueError(
                "Internal error: cannot fetch both json and fs output from fetch_analyzer_output"
            )

        cache_key = CacheKey(analyzer=analyzer, input=input, output_type=output_type)
        if cache_key not in self._fetch_cache:
            path = self._fetch_analyzer_output_impl(analyzer, input, output_type)
            if path is None:
                logger.info(
                    "Could not fetch output of type {output_type} for {analyzer} when run on {input}"
                )
                return None
            self._fetch_cache[cache_key] = path
        return self._fetch_cache[cache_key]

    def _fetch_analyzer_output_impl(
        self,
        analyzer: SpecifiedAnalyzer,
        input: AnalyzerInput,
        output_type: AnalyzerOutputType,
    ) -> Optional[Path]:
        """Implementation for fetch_analyzer_output."""

        prefix = OutputStorage._file_prefix(analyzer)
        # Pick a human-readable prefix to assist in debugging.
        logger.info(f"Fetching output for {analyzer} of type {output_type} for {input}")
        if output_type == AnalyzerOutputType.json:
            _, cached_path = tempfile.mkstemp(
                suffix=".json", prefix=prefix, dir=self._cache_dir
            )
            logger.info(f"Using path {cached_path}")
            if not self._json_output_store.get(input, analyzer, cached_path):
                # Clean up the file.
                Path(cached_path).unlink()
                return None
            return Path(cached_path)

        elif output_type == AnalyzerOutputType.filesystem:
            with tempfile.NamedTemporaryFile(suffix=".tar.gz") as temp_tgz:
                # Store the archive in a tempfile, then unzip it.
                if not self._filesystem_output_store.get(
                    input, analyzer, temp_tgz.name
                ):
                    return None
                cached_dir = tempfile.mkdtemp(prefix=prefix, dir=self._cache_dir)
                logger.info(f"Using dir {cached_dir}")
                with tarfile.open(name=temp_tgz.name) as tar:
                    tar.extractall(cached_dir)
                return Path(cached_dir)

        else:
            raise RuntimeError(f"Cannot fetch for type {output_type}")

    @staticmethod
    def _file_prefix(analyzer: SpecifiedAnalyzer) -> str:
        random_string = "".join(
            random.choice(string.ascii_letters + string.digits) for _ in range(16)
        )
        return f"{analyzer.versioned_analyzer.name}-{analyzer.versioned_analyzer.version}-{random_string}".replace(
            "/", "__"
        )

    def _json_cache_path(self, analyzer: SpecifiedAnalyzer) -> Path:
        return self._cache_dir / f"{OutputStorage._file_prefix(analyzer)}.json"

    def _filesystem_cache_path(self, analyzer: SpecifiedAnalyzer) -> Path:
        return self._cache_dir / OutputStorage._file_prefix(analyzer)

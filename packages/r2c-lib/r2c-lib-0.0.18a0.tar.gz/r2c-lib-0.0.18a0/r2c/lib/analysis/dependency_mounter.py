#!/usr/bin/env python

import logging
import shutil

import attr

from r2c.lib.analysis.mount_manager import MountManager
from r2c.lib.analysis.output_storage import OutputStorage
from r2c.lib.input import AnalyzerInput
from r2c.lib.manifest import AnalyzerOutputType
from r2c.lib.registry import RegistryData
from r2c.lib.specified_analyzer import SpecifiedAnalyzer

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@attr.s(auto_attribs=True, frozen=True)
class DependencyMounter:
    """Wraps an OutputStorage and MountManager.

    Specifically, this class takes care of computing dependencies, fetching all
    of them, and setting them up in the proper location.
    """

    _registry_data: RegistryData
    _output_storage: OutputStorage
    _mount_manager: MountManager

    def mount_all(self, analyzer: SpecifiedAnalyzer, input: AnalyzerInput) -> None:
        """Mounts all dependencies.

        Raises an exception if a dependency failed to mount.
        """
        logger.info(f"Mounting dependencies for {analyzer} on {input}")

        for dependency in self._registry_data.get_direct_dependencies(
            analyzer.versioned_analyzer
        ):
            if not self._mount(dependency, input):
                raise Exception(f"Error while mounting output of {dependency}")

    def _mount(self, dependency: SpecifiedAnalyzer, input: AnalyzerInput) -> bool:
        """Mounts"""
        logger.info(f"Mounting output of {dependency}")
        output_type = self._registry_data.manifest_for(
            dependency.versioned_analyzer
        ).output_type
        input_dir = self._mount_manager.input_dir()

        if output_type.has_json():
            target = input_dir / f"{dependency.versioned_analyzer.name}.json"
            fetched = self._output_storage.fetch_analyzer_output(
                dependency, input, AnalyzerOutputType.json
            )
            if fetched is not None:
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy(fetched, target)
            else:
                return False

        if output_type.has_filesystem():
            fetched = self._output_storage.fetch_analyzer_output(
                dependency, input, AnalyzerOutputType.filesystem
            )
            if fetched is not None:
                shutil.copytree(
                    fetched / dependency.versioned_analyzer.name,
                    input_dir / dependency.versioned_analyzer.name,
                )
            else:
                return False

        return True

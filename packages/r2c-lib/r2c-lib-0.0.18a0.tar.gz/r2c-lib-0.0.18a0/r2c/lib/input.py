import abc
import hashlib
import json
from enum import Enum
from inspect import signature
from typing import Any, Dict, List, Optional, Type

INPUT_TYPE_KEY = "input_type"


class AnalyzerInput(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __init__(self, *args, **kwargs):
        raise NotImplementedError()

    @classmethod
    def subclass_from_name(cls, input_type: str) -> Optional[Type["AnalyzerInput"]]:
        for class_obj in cls.__subclasses__():
            if class_obj.__name__ == input_type:
                return class_obj
        return None

    @classmethod
    def _input_keys(cls) -> List[str]:
        """
            Returns a list of string keys that this type of input contains. Uses the subclass's __init__ method to find these keys. This will suffice until we support more flexible json schemas.
            When constructing storage keys, Filestore concatenates the values corresponding to these keys in this order, so this ordering determines storage hierarchy.
        """
        sig = signature(cls.__init__)
        return [param.name for param in sig.parameters.values() if param.name != "self"]

    def to_json(self) -> Dict[str, Any]:
        """
            Returns: the json data representing this analyzer input
        """
        d = {k: v for k, v in self.__dict__.items() if k in self._input_keys()}
        d[INPUT_TYPE_KEY] = self.__class__.__name__
        return d

    def hash(self) -> str:
        """
            One way hash function to use as uuid for an AnalyzerInput

            Uses sha1 hash of sorted json keys
        """
        input_json = self.to_json()
        canonical_string = json.dumps(input_json, sort_keys=True)
        m = hashlib.sha1()
        m.update(canonical_string.encode())
        return m.hexdigest()

    @classmethod
    def from_json(cls, json_obj: Dict[str, Any]) -> "AnalyzerInput":
        if INPUT_TYPE_KEY not in json_obj:
            raise InvalidAnalyzerInputException(
                f"Failed to parse json {json_obj} as an instance of AnalyzerInput."
                f"Couldn't find key {INPUT_TYPE_KEY} to determine input type"
            )
        subclass = cls.subclass_from_name(json_obj[INPUT_TYPE_KEY])
        if subclass is None:
            raise InvalidAnalyzerInputException(
                f"Failed to parse json {json_obj} as an instance of {cls}. "
                f"Input type must be one of {AnalyzerInput.__subclasses__()}"
            )

        # Pass through all fields to the subclass's constructor.
        json_obj = {k: v for k, v in json_obj.items() if k != INPUT_TYPE_KEY}
        try:
            return subclass(**json_obj)
        except Exception:
            raise InvalidAnalyzerInputException(
                "Failed to parse json {json_obj} as instance of {subclass}"
            )

    def __repr__(self) -> str:
        return json.dumps(self.to_json())


class GitRepoCommit(AnalyzerInput):
    def __init__(self, repo_url: str, commit_hash: str):
        self.repo_url = repo_url
        self.commit_hash = commit_hash


class GitRepo(AnalyzerInput):
    def __init__(self, repo_url):
        self.repo_url = repo_url


class PackageRepository(Enum):
    NPM = "npm"
    PYPI = "pypi"


class PackageVersion(AnalyzerInput):
    def __init__(
        self, package_name: str, version: str, repository: Optional[str] = None
    ):
        self.repository = PackageRepository(repository) if repository else None
        self.package_name = package_name
        self.version = version

    # Override because of the repository field.
    def to_json(self) -> Dict[str, Any]:
        d = {"package_name": self.package_name, "version": self.version}
        d[INPUT_TYPE_KEY] = self.__class__.__name__
        if self.repository:
            d["repository"] = self.repository.value
        return d


class HttpUrl(AnalyzerInput):
    def __init__(self, url):
        self.url = url


class AuraInput(AnalyzerInput):
    def __init__(self, targets: str, metadata: str):
        self.targets = targets
        self.metadata = metadata


class LocalCode(AnalyzerInput):
    """Represents code stored on disk.

    This generally implies that all the 'fetcher' analyzers will have their
    output overridden.
    """

    def __init__(self, code_dir: str):
        self.code_dir = code_dir


class InvalidAnalyzerInputException(Exception):
    pass


class InvalidStorageKeyException(Exception):
    pass

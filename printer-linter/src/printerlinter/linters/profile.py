import re
from typing import Iterator

from ..diagnostic import Diagnostic
from .linter import Linter
from pathlib import Path
from configparser import ConfigParser

class Profile(Linter):
    MAX_SIZE_OF_NAME = 20
    def __init__(self, file: Path, settings: dict) -> None:
        """ Finds issues in the parent directory"""
        super().__init__(file, settings)
        self._content = self._file.read_text()


    def check(self) -> Iterator[Diagnostic]:
        if self._file.exists() and self._settings["checks"].get("diagnostic-long-profile-names", False):
            for check in self.checklengthofProfileName():
                yield check
        yield


    def checklengthofProfileName(self) -> Iterator[Diagnostic]:

        data = self._isNameSizeBIggerThanThreshhold()
        """ Check if there is a dot in the directory name, MacOS has trouble signing and notarizing otherwise """
        name_of_profile, found = self._getprofileName()
        if len(name_of_profile) > Profile.MAX_SIZE_OF_NAME:
            yield Diagnostic(
                file=self._file,
                diagnostic_name="diagnostic-long-profile-names",
                message=f"Profile name contained is too long, please make it a bit smaller",
                level="Warning",
                offset = found.span(0)[0]
            )
        yield

    def _getprofileName(self) -> dict:
        config = ConfigParser()
        config.read([self._file])
        name_of_profile = config.get("general", "name")
        redefined = re.compile(name_of_profile)
        found = redefined.search(self._content)
        return name_of_profile, found

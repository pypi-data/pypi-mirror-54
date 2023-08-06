"""
Utilities helping compare various data formats in a visual way.
"""

import os
import subprocess
import sys
import tempfile
from abc import ABC
from abc import abstractmethod
from enum import Enum
from pathlib import Path
from typing import Any

import yaml

from ndd_test4p.comparators import TextFileContentComparator


# -------------------------------------------------------------------------------------- DifferencesViewerDelegate -----

class DifferencesViewerDelegate(ABC):
    """
    Base class for all the viewer delegates.
    The role of a viewer delegate is to display differences between two files.
    """

    @abstractmethod
    def view(self, actual_file_path: Path, expected_file_path: Path):
        """
        Display differences between the given files.

        Args:
            actual_file_path (pathlib.Path): The file path of the actual content to compare.
            expected_file_path (pathlib.Path): The file path of the expected content to compare.
        """


class DiffViewerDelegate(DifferencesViewerDelegate):
    """
    Display differences between two files using `diff <https://en.wikipedia.org/wiki/Diff>`_.
    """

    def view(self, actual_file_path: Path, expected_file_path: Path):
        """
        Display differences between two files using `diff <https://en.wikipedia.org/wiki/Diff>`_.

        Args:
            actual_file_path (pathlib.Path): The file path of the actual content to compare.
            expected_file_path (pathlib.Path): The file path of the expected content to compare.
        """
        comparator = TextFileContentComparator(actual_file_path, expected_file_path)
        sys.stdout.writelines(comparator.unified_diff())


class MeldViewerDelegate(DifferencesViewerDelegate):
    """
    Display differences between two files using `Meld <https://meldmerge.org/>`_.
    """

    def view(self, actual_file_path: Path, expected_file_path: Path):
        """
        Display differences between two files using `Meld <https://meldmerge.org/>`_.

        Args:
            actual_file_path (pathlib.Path): The file path of the actual content to compare.
            expected_file_path (pathlib.Path): The file path of the expected content to compare.
        """
        subprocess.call(['meld', expected_file_path, actual_file_path])


# --------------------------------------------------------------------------------------------- DifferencesContext -----

class DifferencesContextMode(Enum):
    """
    The available display modes.
    They are made available through the environment variable named "DIFFERENCES_CONTEXT_MODE".
    """
    #: Differences will never be displayed
    DISABLED = 'disabled'
    #: Differences will always be displayed upon :class:`AssertionError`
    ENABLED_ALWAYS = 'enabled-always'
    #: Differences will be displayed only the first time upon :class:`AssertionError`
    ENABLED_FIRST = 'enabled-first'


class DifferencesContextDelegate(Enum):
    """
    The viewer delegates.
     They are made available through the environment variable named "DIFFERENCES_CONTEXT_DELEGATE".
    """
    #: diff is a data comparison tool between two files
    DIFF = DiffViewerDelegate
    #: Meld is a visual diff and merge tool
    MELD = MeldViewerDelegate


class DifferencesContextSettings:
    """
    A global context used by the the :class:`DifferencesViewer` to store configuration and maintain state across tests.

    - The display mode is set using the environment variable named "DIFFERENCES_CONTEXT_MODE" if specified,
      or to the default value :attr:`DifferencesContextMode.DISABLED` otherwise.
    - The viewer delegate is set using the environment variable named "DIFFERENCES_CONTEXT_DELEGATE" if specified,
      or to the default value :class:`DiffViewerDelegate` otherwise.
    """

    #: The key of the environment variable to set the mode.
    DIFFERENCES_CONTEXT_MODE_KEY = 'DIFFERENCES_CONTEXT_MODE'
    #: The key of the environment variable to set the delegate.
    DIFFERENCES_CONTEXT_DELEGATE_KEY = 'DIFFERENCES_CONTEXT_DELEGATE'

    #: The default mode.
    DEFAULT_DIFFERENCES_CONTEXT_MODE = DifferencesContextMode.DISABLED
    #: The default delegate.
    DEFAULT_VIEWER_DELEGATE = DiffViewerDelegate()

    def __init__(self):
        """
        - The display mode is set using the environment variable named "DIFFERENCES_CONTEXT_MODE" if specified,
          or to the default value :attr:`DifferencesContextMode.DISABLED` otherwise.
        - The viewer delegate is set using the environment variable named "DIFFERENCES_CONTEXT_DELEGATE" if specified,
          or to the default value :class:`DiffViewerDelegate` otherwise.
        """
        self._display_count: int = 0
        self._mode: DifferencesContextMode = DifferencesContextSettings.DEFAULT_DIFFERENCES_CONTEXT_MODE
        self._delegate: DifferencesViewerDelegate = DifferencesContextSettings.DEFAULT_VIEWER_DELEGATE

        environment_mode = os.environ.get(self.DIFFERENCES_CONTEXT_MODE_KEY)
        if environment_mode:
            self._mode = DifferencesContextMode[environment_mode]

        environment_delegate = os.environ.get(self.DIFFERENCES_CONTEXT_DELEGATE_KEY)
        if environment_delegate:
            self._delegate = DifferencesContextDelegate[environment_delegate].value()

    @property
    def display_count(self) -> int:
        """int: The number of times differences have been actually displayed."""
        return self._display_count

    @property
    def mode(self) -> DifferencesContextMode:
        """DifferencesContextMode: The display mode to be used by all the :class:`DifferencesViewer`."""
        return self._mode

    @mode.setter
    def mode(self, mode: DifferencesContextMode):
        self._mode = mode

    @property
    def delegate(self) -> DifferencesViewerDelegate:
        """DifferencesViewerDelegate: The viewer delegate to be used by all the :class:`DifferencesViewer`."""
        return self._delegate

    @delegate.setter
    def delegate(self, delegate: DifferencesViewerDelegate):
        self._delegate = delegate

    def can_display_differences(self) -> bool:
        """
        Returns:
            bool:

            - False if mode is :attr:`DifferencesContextMode.DISABLED`
            - True if mode is :attr:`DifferencesContextMode.ENABLED_ALWAYS`
            - True if mode is :attr:`DifferencesContextMode.ENABLED_FIRST` and `display_count < 1`
            - False otherwise
        """
        if self.mode == DifferencesContextMode.DISABLED:
            return False
        if self.mode == DifferencesContextMode.ENABLED_ALWAYS:
            return True
        if self.mode == DifferencesContextMode.ENABLED_FIRST:
            return self.display_count < 1
        raise ValueError(f'Invalid mode "{self.mode}"')

    def display_differences(self, actual_file_path: Path, expected_file_path: Path):
        """
        Increase the display count by 1 then display the differences using the current context delegate.

        Args:
            actual_file_path (pathlib.Path): The file path of the actual content to compare.
            expected_file_path (pathlib.Path): The file path of the expected content to compare.
        """
        self._display_count += 1
        self._delegate.view(actual_file_path, expected_file_path)

    def reset(self):
        """
        Restore the display count, the display mode and the :class:`ViewerDelegate`.
        """
        self.__init__()


#: The global instance used by all the :class:`DifferencesViewer`.
DIFFERENCES_CONTEXT_SETTINGS = DifferencesContextSettings()


# ---------------------------------------------------------------------------------------------- DifferencesViewer -----

class DifferencesViewer(ABC):
    """
    Base class to display differences between to sets of data.
    """


class AbstractDifferencesViewer(DifferencesViewer, ABC):
    """
    Display differences as text between two pieces of data, according to the current context.
    """

    def __init__(self, actual_data_or_file_path: Any, expected_data_or_file_path: Any, force_display: bool = False):
        """
        Args:
            actual_data_or_file_path (Any): The actual data to compare.
            expected_data_or_file_path (Any): The expected data to compare.
            force_display (bool): True to display differences upon AssertionError disregarding the current context.
        """
        self._actual_data_or_file_path = actual_data_or_file_path
        self._expected_data_or_file_path = expected_data_or_file_path
        self._force_display = force_display

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type == AssertionError:
            if self._force_display or DIFFERENCES_CONTEXT_SETTINGS.can_display_differences():
                self._compare()

    def _compare(self) -> None:
        """
        Called when an :class:`AssertionError` is raised when comparing data with data.
        """
        if isinstance(self._actual_data_or_file_path, Path):
            if isinstance(self._expected_data_or_file_path, Path):
                self._compare_file_with_file(self._actual_data_or_file_path, self._expected_data_or_file_path)
            else:
                self._compare_file_with_data(self._actual_data_or_file_path, self._expected_data_or_file_path)
        else:
            if isinstance(self._expected_data_or_file_path, Path):
                self._compare_data_with_file(self._actual_data_or_file_path, self._expected_data_or_file_path)
            else:
                self._compare_data_with_data(self._actual_data_or_file_path, self._expected_data_or_file_path)

    @abstractmethod
    def _compare_data_with_data(self, actual_data: str, expected_data: str) -> None:
        """
        Called when an :class:`AssertionError` is raised when comparing data with data.
        Two temporary files are created and both data are dumped inside as text.

        Args:
            actual_data (Any): The actual data to compare.
            expected_data (Any): The expected data to compare.
        """

    @abstractmethod
    def _compare_data_with_file(self, actual_data: str, expected_file_path: Path) -> None:
        """
        Called when an :class:`AssertionError` is raised when comparing data with a file content.
        One temporary file is created and the actual data is written inside as text.

        Args:
            actual_data (str): The actual data to compare.
            expected_file_path (pathlib.Path): The file path of the expected content to compare.
        """

    @abstractmethod
    def _compare_file_with_data(self, actual_file_path: Path, expected_data: str) -> None:
        """
        Called when an :class:`AssertionError` is raised when comparing a file content with data.
        One temporary file is created and the expected data is dumped inside as text.

        Args:
            actual_file_path (pathlib.Path): The file path of the actual content to compare.
            expected_data (Any): The expected data to compare.
        """

    @abstractmethod
    def _compare_file_with_file(self, actual_file_path: Path, expected_file_path: Path) -> None:
        """
        Called when an :class:`AssertionError` is raised when comparing two file contents.

        Args:
            actual_file_path (pathlib.Path): The file path of the actual content to compare.
            expected_file_path (pathlib.Path): The file path of the expected content to compare.
        """

    @abstractmethod
    def _file_extension(self) -> str:
        """
        Returns:
             str: The file extension used for creating temporary files.
        """

    def _expected_file_path(self, directory_path: Path) -> Path:
        expected_file_name = 'expected.' + self._file_extension()
        return directory_path.joinpath(expected_file_name)

    def _actual_file_path(self, directory_path: Path) -> Path:
        actual_file_name = 'actual.' + self._file_extension()
        return directory_path.joinpath(actual_file_name)

    @classmethod
    def _write_temporary_file(cls, file_path: Path, data: str) -> Path:
        file_path.write_text(
            '\n'
            + '#####################################################\n'
            + '# This file is temporary, all changes will be lost! #\n'
            + '#####################################################\n'
            + '\n'
            + data
        )
        return file_path


class TextDifferencesViewer(AbstractDifferencesViewer):
    """
    Display differences as text between two pieces of data, according to the current context.
    The display mode and the viewer delegate are set on the current :class:`DifferencesContextSettings`.
    The rules are:

    - if no :class:`AssertionError` is raised, do not display differences
    - if an :class:`AssertionError` is raised:

      - if mode is set to :attr:`DifferencesContextMode.DISABLED`, do not display differences
      - if mode is set to :attr:`DifferencesContextMode.ENABLED_ALWAYS`, display differences
      - if mode is set to :attr:`DifferencesContextMode.ENABLED_FIRST`, display differences the first time only

    :Example:

        Using Meld and the :attr:`DifferencesContextMode.ENABLED_FIRST` mode::

            DIFFERENCES_CONTEXT_SETTINGS.mode = DifferencesContextMode.ENABLED_FIRST
            # or set the environment variable 'DIFFERENCES_CONTEXT_MODE' to 'ENABLED_FIRST'

            DIFFERENCES_CONTEXT_SETTINGS.delegate = DifferencesContextDelegate.MeldViewerDelegate
            # or set the environment variable 'DIFFERENCES_CONTEXT_DELEGATE' to 'MELD'

            # Compare 2 pieces of data.
            # Two temporary files are created and both data are written inside as text.
            with TextDifferencesViewer(actual_data, expected_data):
                expect(actual_data).to(equal(expected_data))

            # Compare a piece of data with the content of a text file.
            # One temporary file is created and the actual data is written inside as text.
            with TextDifferencesViewer(actual_data, expected_file_path):
                expect(actual_data).to(equal(self._test_data_from(expected_file_path)))

            # Compare the content of a text file with a piece of data.
            # One temporary file is created and the expected data is written inside as text.
            with TextDifferencesViewer(actual_file_path, expected_data):
                expect(self._test_data_from(actual_file_path)).to(equal(expected_data))

            # Compare the content of two text files.
            with TextDifferencesViewer(actual_file_path, expected_file_path):
                expect(actual_file_path).to(have_same_content_as(expected_file_path))

            # Compare recursively the content of two directories.
            with TextDifferencesViewer(actual_file_path, expected_file_path):
                expect(actual_file_path).to(have_same_content_recursively_as(expected_file_path))

    """

    def _compare_data_with_data(self, actual_data: str, expected_data: str) -> None:
        """
        Called when an :class:`AssertionError` is raised when comparing data with data.
        Two temporary files are created and both data are dumped inside as text.

        Args:
            actual_data (Any): The actual data to compare.
            expected_data (Any): The expected data to compare.
        """
        with tempfile.TemporaryDirectory() as directory_path:
            directory_path = Path(directory_path)

            actual_file_path = self._actual_file_path(directory_path)
            self._write_text(actual_file_path, actual_data)

            expected_file_path = self._expected_file_path(directory_path)
            self._write_text(expected_file_path, expected_data)

            DIFFERENCES_CONTEXT_SETTINGS.display_differences(actual_file_path, expected_file_path)

    def _compare_data_with_file(self, actual_data: str, expected_file_path: Path) -> None:
        """
        Called when an :class:`AssertionError` is raised when comparing data with a file content.
        One temporary file is created and the actual data is written inside as text.

        Args:
            actual_data (str): The actual data to compare.
            expected_file_path (pathlib.Path): The file path of the expected content to compare.
        """
        with tempfile.TemporaryDirectory() as directory_path:
            directory_path = Path(directory_path)

            actual_file_path = self._actual_file_path(directory_path)
            self._write_text(actual_file_path, actual_data)

            DIFFERENCES_CONTEXT_SETTINGS.display_differences(actual_file_path, expected_file_path)

    def _compare_file_with_data(self, actual_file_path: Path, expected_data: str) -> None:
        """
        Called when an :class:`AssertionError` is raised when comparing a file content with data.
        One temporary file is created and the expected data is dumped inside as text.

        Args:
            actual_file_path (pathlib.Path): The file path of the actual content to compare.
            expected_data (Any): The expected data to compare.
        """
        with tempfile.TemporaryDirectory() as directory_path:
            directory_path = Path(directory_path)

            expected_file_path = self._expected_file_path(directory_path)
            self._write_text(expected_file_path, expected_data)

            DIFFERENCES_CONTEXT_SETTINGS.display_differences(actual_file_path, expected_file_path)

    def _compare_file_with_file(self, actual_file_path: Path, expected_file_path: Path) -> None:
        """
        Called when an :class:`AssertionError` is raised when comparing two file contents.

        Args:
            actual_file_path (pathlib.Path): The file path of the actual content to compare.
            expected_file_path (pathlib.Path): The file path of the expected content to compare.
        """
        if self._force_display or DIFFERENCES_CONTEXT_SETTINGS.can_display_differences():
            DIFFERENCES_CONTEXT_SETTINGS.display_differences(actual_file_path, expected_file_path)

    def _file_extension(self) -> str:
        return 'txt'

    @classmethod
    def _write_text(cls, file_path: Path, data: str):
        AbstractDifferencesViewer._write_temporary_file(file_path, data)


class YamlDifferencesViewer(AbstractDifferencesViewer):
    """
    Display differences as YAML between two pieces of data, according to the current context.
    The data can be any data or a :class:`pathlib.Path`.
    The later must be a file with the content exactly as dumped by :func:`yaml.dump` with `default_flow_style=False`.
    The display mode and the viewer delegate are set on the current :class:`DifferencesContextSettings`.
    The rules are:

    - if no :class:`AssertionError` is raised, do not display differences
    - if an :class:`AssertionError` is raised:

      - if mode is set to :attr:`DifferencesContextMode.DISABLED`, do not display differences
      - if mode is set to :attr:`DifferencesContextMode.ENABLED_ALWAYS`, display differences
      - if mode is set to :attr:`DifferencesContextMode.ENABLED_FIRST`, display differences the first time only

    :Example:

        Using Meld and the :attr:`DifferencesContextMode.ENABLED_FIRST` mode::

            DIFFERENCES_CONTEXT_SETTINGS.mode = DifferencesContextMode.ENABLED_FIRST
            # or set the environment variable 'DIFFERENCES_CONTEXT_MODE' to 'ENABLED_FIRST'

            DIFFERENCES_CONTEXT_SETTINGS.delegate = DifferencesContextDelegate.MeldViewerDelegate
            # or set the environment variable 'DIFFERENCES_CONTEXT_DELEGATE' to 'MELD'

            # Compare 2 pieces of data.
            # Two temporary files are created and both data are dumped inside as YAML.
            with YamlDifferencesViewer(actual_data, expected_data):
                expect(actual_data).to(equal(expected_data))

            # Compare a piece of data with the content of a YAML file.
            # One temporary file is created and the actual data is dumped inside as YAML.
            with YamlDifferencesViewer(actual_data, expected_file_path):
                expect(actual_data).to(equal(self._test_data_from_yaml(expected_file_path)))

            # Compare the content of a YAML file with a piece of data.
            # One temporary file is created and the expected data is dumped inside as YAML.
            with YamlDifferencesViewer(actual_file_path, expected_data):
                expect(self._test_data_from_yaml(actual_file_path)).to(equal(expected_data))

            # Compare the content of two YAML files.
            # Two temporary files are created and both file contents are read then dumped inside as YAML.
            # This is useful to compare normalized YAML data.
            with YamlDifferencesViewer(actual_file_path, expected_file_path):
                expect(self._test_data_from_yaml(actual_file_path)).to(
                    equal(self._test_data_from_yaml(expected_file_path)))

    """

    def _compare_data_with_data(self, actual_data: Any, expected_data: Any) -> None:
        """
        Called when an :class:`AssertionError` is raised when comparing data with data.
        Two temporary files are created and both data are dumped inside as YAML.

        Args:
            actual_data (Any): The actual data to compare.
            expected_data (Any): The expected data to compare.
        """
        with tempfile.TemporaryDirectory() as directory_path:
            directory_path = Path(directory_path)

            actual_file_path = self._actual_file_path(directory_path)
            self._write_yaml(actual_file_path, actual_data)

            expected_file_path = self._expected_file_path(directory_path)
            self._write_yaml(expected_file_path, expected_data)

            DIFFERENCES_CONTEXT_SETTINGS.display_differences(actual_file_path, expected_file_path)

    def _compare_data_with_file(self, actual_data: Any, expected_file_path: Path) -> None:
        """
        Called when an :class:`AssertionError` is raised when comparing data with a file content.
        One temporary file is created and the actual data is dumped inside as YAML.

        Args:
            actual_data (Any): The actual data to compare.
            expected_file_path (pathlib.Path): The file path of the expected content to compare.
        """
        with tempfile.TemporaryDirectory() as directory_path:
            directory_path = Path(directory_path)

            actual_file_path = self._actual_file_path(directory_path)
            self._write_yaml(actual_file_path, actual_data)

            DIFFERENCES_CONTEXT_SETTINGS.display_differences(actual_file_path, expected_file_path)

    def _compare_file_with_data(self, actual_file_path: Path, expected_data: Any) -> None:
        """
        Called when an :class:`AssertionError` is raised when comparing a file content with data.
        One temporary file is created and the expected data is dumped inside as YAML.

        Args:
            actual_file_path (pathlib.Path): The file path of the actual content to compare.
            expected_data (Any): The expected data to compare.
        """
        with tempfile.TemporaryDirectory() as directory_path:
            directory_path = Path(directory_path)

            expected_file_path = self._expected_file_path(directory_path)
            self._write_yaml(expected_file_path, expected_data)

            DIFFERENCES_CONTEXT_SETTINGS.display_differences(actual_file_path, expected_file_path)

    def _compare_file_with_file(self, actual_file_path: Path, expected_file_path: Path) -> None:
        """
        Called when an :class:`AssertionError` is raised when comparing two file contents.
        Two temporary files are created and both file contents are read then dumped inside as YAML.
        This is useful to compare normalized YAML data.

        Args:
            actual_file_path (pathlib.Path): The file path of the actual content to compare.
            expected_file_path (pathlib.Path): The file path of the expected content to compare.
        """
        with tempfile.TemporaryDirectory() as directory_path:
            directory_path = Path(directory_path)

            actual_data = yaml.load(actual_file_path.read_text())
            actual_file_path = self._actual_file_path(directory_path)
            self._write_yaml(actual_file_path, actual_data)

            expected_data = yaml.load(expected_file_path.read_text())
            expected_file_path = self._expected_file_path(directory_path)
            self._write_yaml(expected_file_path, expected_data)

            DIFFERENCES_CONTEXT_SETTINGS.display_differences(actual_file_path, expected_file_path)

    def _file_extension(self) -> str:
        return 'yml'

    @classmethod
    def _write_yaml(cls, file_path: Path, data: Any):
        yaml.Dumper.ignore_aliases = lambda *args: True
        yaml_data = yaml.dump(data, default_flow_style=False)
        AbstractDifferencesViewer._write_temporary_file(file_path, yaml_data)

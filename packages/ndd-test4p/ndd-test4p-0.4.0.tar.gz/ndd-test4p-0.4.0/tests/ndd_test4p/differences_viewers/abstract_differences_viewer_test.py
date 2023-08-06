import os
from abc import ABC
from abc import abstractmethod
from pathlib import Path
from typing import Any
from typing import List

import pytest
from expects import *

from ndd_test4p.differences_viewers import DIFFERENCES_CONTEXT_SETTINGS
from ndd_test4p.differences_viewers import DifferencesContextMode
from ndd_test4p.differences_viewers import DifferencesViewerDelegate
from ndd_test4p.differences_viewers import DiffViewerDelegate
from ndd_test4p.test_cases import AbstractTest


class AbstractDifferencesViewerTest(AbstractTest, ABC):
    _actual_data_or_file_path: Any
    _expected_data_or_file_path: Any
    _delegate: '_RecordingView'

    def setup_method(self):
        self._unset_environment_variable()

        self._actual_data_or_file_path = self._create_actual_data_or_file_path()
        self._expected_data_or_file_path = self._create_expected_data_or_file_path()

        self._delegate = _RecordingView()

    def teardown_method(self):
        self._unset_environment_variable()

    def test_when_mode_is_disabled_and_no_assertion_error_is_raised(self):
        self._configure_settings(DifferencesContextMode.DISABLED)

        self._call_viewer_without_assertion_error()
        self._check_view_has_not_been_called()

        self._call_viewer_without_assertion_error_with_force()
        self._check_view_has_not_been_called()

    def test_when_mode_is_disabled_and_an_assertion_error_is_raised(self):
        self._configure_settings(DifferencesContextMode.DISABLED)

        self._call_viewer_with_assertion_error()
        self._check_view_has_not_been_called()

        self._call_viewer_with_assertion_error_with_force()
        self._check_view_has_been_called_once()

    def test_when_mode_is_enabled_always_and_no_assertion_error_is_raised(self):
        self._configure_settings(DifferencesContextMode.ENABLED_ALWAYS)

        self._call_viewer_without_assertion_error()
        self._check_view_has_not_been_called()

        self._call_viewer_without_assertion_error_with_force()
        self._check_view_has_not_been_called()

    def test_when_mode_is_enabled_always_and_an_assertion_error_is_raised(self):
        self._configure_settings(DifferencesContextMode.ENABLED_ALWAYS)

        self._call_viewer_with_assertion_error()
        self._check_view_has_been_called_once()

        self._call_viewer_with_assertion_error_with_force()
        self._check_view_has_been_called_twice()

    def test_when_mode_is_enabled_first_and_no_assertion_error_is_raised(self):
        self._configure_settings(DifferencesContextMode.ENABLED_FIRST)

        self._call_viewer_without_assertion_error()
        self._check_view_has_not_been_called()

        self._call_viewer_without_assertion_error_with_force()
        self._check_view_has_not_been_called()

    def test_when_mode_is_enabled_first_and_an_assertion_error_is_raised(self):
        self._configure_settings(DifferencesContextMode.ENABLED_FIRST)

        self._call_viewer_with_assertion_error()
        self._check_view_has_been_called_once()

        self._call_viewer_with_assertion_error()
        self._check_view_has_been_called_once()

        self._call_viewer_with_assertion_error_with_force()
        self._check_view_has_been_called_twice()

    def test_default_viewer(self, capsys):
        DIFFERENCES_CONTEXT_SETTINGS.reset()
        DIFFERENCES_CONTEXT_SETTINGS.mode = DifferencesContextMode.ENABLED_ALWAYS
        DIFFERENCES_CONTEXT_SETTINGS.delegate = DiffViewerDelegate()

        with pytest.raises(AssertionError, match='Some fake assertion error') as error_info:
            with self._viewer(self._actual_data_or_file_path, self._expected_data_or_file_path):
                raise AssertionError('Some fake assertion error')

        captured_output = capsys.readouterr().out

        expect(error_info.value.__cause__).to(be_none)
        self._test_default_viewer_output(captured_output)

    @staticmethod
    def _unset_environment_variable():
        if 'DIFFERENCES_CONTEXT_MODE' in os.environ:
            del os.environ['DIFFERENCES_CONTEXT_MODE']

    def _configure_settings(self, mode):
        DIFFERENCES_CONTEXT_SETTINGS.reset()
        DIFFERENCES_CONTEXT_SETTINGS.mode = mode
        DIFFERENCES_CONTEXT_SETTINGS.delegate = self._delegate

    def _call_viewer_without_assertion_error(self):
        with self._viewer(self._actual_data_or_file_path, self._expected_data_or_file_path):
            pass

    def _call_viewer_without_assertion_error_with_force(self):
        with self._viewer(self._actual_data_or_file_path, self._expected_data_or_file_path, True):
            pass

    def _call_viewer_with_assertion_error(self):
        with pytest.raises(AssertionError, match='Some fake assertion error') as error_info:
            with self._viewer(self._actual_data_or_file_path, self._expected_data_or_file_path):
                raise AssertionError('Some fake assertion error')
        expect(error_info.value.__cause__).to(be_none)

    def _call_viewer_with_assertion_error_with_force(self):
        with pytest.raises(AssertionError, match='Some fake assertion error') as error_info:
            with self._viewer(self._actual_data_or_file_path, self._expected_data_or_file_path, True):
                raise AssertionError('Some fake assertion error')
        expect(error_info.value.__cause__).to(be_none)

    def _check_view_has_not_been_called(self):
        self._check_view_has_been_called(0)

    def _check_view_has_been_called_once(self):
        self._check_view_has_been_called(1)

    def _check_view_has_been_called_twice(self):
        self._check_view_has_been_called(2)

    @abstractmethod
    def _create_actual_data_or_file_path(self) -> Any:
        """Create data which must be different from the expected one."""

    @abstractmethod
    def _create_expected_data_or_file_path(self) -> Any:
        """Create data which must be different from the actual one."""

    @abstractmethod
    def _test_default_viewer_output(self, captured_output: str) -> None:
        pass

    @abstractmethod
    def _check_view_has_been_called(self, times):
        pass

    @abstractmethod
    def _viewer(self, actual_data_or_file_path: Any, expected_data_or_file_path: Any, force_display: bool = False):
        pass


class _Record:
    actual_file_path: Path
    expected_file_path: Path
    actual_text: str
    expected_text: str

    def __init__(self, actual_file_path: Path, expected_file_path: Path):
        self.actual_file_path = actual_file_path
        self.expected_file_path = expected_file_path
        self.actual_text = actual_file_path.read_text()
        self.expected_text = expected_file_path.read_text()


class _RecordingView(DifferencesViewerDelegate):
    records: List[_Record]

    def __init__(self):
        self.records = []

    def view(self, actual_file_path: Path, expected_file_path: Path):
        self.records.append(_Record(actual_file_path, expected_file_path))

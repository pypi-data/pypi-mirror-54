import re
from abc import ABC
from pathlib import Path
from typing import Any
from typing import List

from expects import *

from ndd_test4p.differences_viewers import DifferencesViewerDelegate
from ndd_test4p.differences_viewers import YamlDifferencesViewer
from tests.ndd_test4p.differences_viewers.abstract_differences_viewer_test import AbstractDifferencesViewerTest


class AbstractTestYamlDifferencesViewer(AbstractDifferencesViewerTest, ABC):
    # pylint: disable=abstract-method
    _actual_data_or_file_path: Any
    _expected_data_or_file_path: Any
    _delegate: '_RecordingView'

    def _viewer(self, actual_data_or_file_path: Any, expected_data_or_file_path: Any, force_display: bool = False):
        return YamlDifferencesViewer(actual_data_or_file_path, expected_data_or_file_path, force_display)


class TestYamlDifferencesViewer_Data_Data(AbstractTestYamlDifferencesViewer):  # pylint: disable=invalid-name

    def _create_actual_data_or_file_path(self) -> Any:
        return {'key1': 1, 'key2': {'key3': 3}}

    def _create_expected_data_or_file_path(self) -> Any:
        return {'key1': 1, 'key2': {'key3': 999}}

    def _test_default_viewer_output(self, captured_output):
        expect(captured_output).to(match(
            r'--- /.+/actual.yml\n'
            + r'\+\+\+ /.+/expected.yml\n'
            + re.escape(
                '@@ -5,4 +5,4 @@\n'
                + ' \n'
                + ' key1: 1\n'
                + ' key2:\n'
                + '-  key3: 3\n'
                + '+  key3: 999\n'
            )
        ))

    def _check_view_has_been_called(self, times):
        expect(self._delegate.records).to(have_length(times))

        for record in self._delegate.records:
            expect(record.actual_file_path.as_posix()).to(end_with('/actual.yml'))
            expect(record.expected_file_path.as_posix()).to(end_with('/expected.yml'))
            expect(record.actual_text).to(equal(self._test_data_from('expected-actual-temp.yml')))
            expect(record.expected_text).to(equal(self._test_data_from('expected-expected-temp.yml')))


class TestYamlDifferencesViewer_Data_File(AbstractTestYamlDifferencesViewer):  # pylint: disable=invalid-name

    def _create_actual_data_or_file_path(self) -> Any:
        return {'key1': 1, 'key2': {'key3': 3}}

    def _create_expected_data_or_file_path(self) -> Any:
        return self._test_data_file_path('expected.yml')

    def _test_default_viewer_output(self, captured_output):
        expect(captured_output).to(match(
            r'--- /.+/actual.yml\n'
            + re.escape(
                f'+++ {self._expected_data_or_file_path.as_posix()}\n'
                + '@@ -1,8 +1,3 @@\n'
                + '-\n'
                + '-#####################################################\n'
                + '-# This file is temporary, all changes will be lost! #\n'
                + '-#####################################################\n'
                + '-\n'
                + ' key1: 1\n'
                + ' key2:\n'
                + '-  key3: 3\n'
                + '+  key3: 999\n'
            )
        ))

    def _check_view_has_been_called(self, times):
        expect(self._delegate.records).to(have_length(times))

        for record in self._delegate.records:
            expect(record.actual_file_path.as_posix()).to(end_with('/actual.yml'))
            expect(record.expected_file_path).to(equal(self._expected_data_or_file_path))
            expect(record.actual_text).to(equal(self._test_data_from('expected-actual-temp.yml')))
            expect(record.expected_text).to(equal(self._expected_data_or_file_path.read_text()))


class TestYamlDifferencesViewer_File_Data(AbstractTestYamlDifferencesViewer):  # pylint: disable=invalid-name

    def _create_actual_data_or_file_path(self) -> Any:
        return self._test_data_file_path('actual.yml')

    def _create_expected_data_or_file_path(self) -> Any:
        return {'key1': 1, 'key2': {'key3': 999}}

    def _test_default_viewer_output(self, captured_output):
        expect(captured_output).to(match(
            re.escape(
                f'--- {self._actual_data_or_file_path.as_posix()}\n'
            )
            + r'\+\+\+ /.+/expected.yml\n'
            + re.escape(
                '@@ -1,3 +1,8 @@\n'
                + '+\n'
                + '+#####################################################\n'
                + '+# This file is temporary, all changes will be lost! #\n'
                + '+#####################################################\n'
                + '+\n'
                + ' key1: 1\n'
                + ' key2:\n'
                + '-  key3: 3\n'
                + '+  key3: 999\n'
            )
        ))

    def _check_view_has_been_called(self, times):
        expect(self._delegate.records).to(have_length(times))

        for record in self._delegate.records:
            expect(record.actual_file_path).to(equal(self._actual_data_or_file_path))
            expect(record.expected_file_path.as_posix()).to(end_with('/expected.yml'))
            expect(record.actual_text).to(equal(self._actual_data_or_file_path.read_text()))
            expect(record.expected_text).to(equal(self._test_data_from('expected-expected-temp.yml')))


class TestYamlDifferencesViewer_File_File(AbstractTestYamlDifferencesViewer):  # pylint: disable=invalid-name

    def _create_actual_data_or_file_path(self) -> Any:
        return self._test_data_file_path('actual.yml')

    def _create_expected_data_or_file_path(self) -> Any:
        return self._test_data_file_path('expected.yml')

    def _test_default_viewer_output(self, captured_output):
        expect(captured_output).to(match(
            r'--- /.+/actual.yml\n'
            + r'\+\+\+ /.+/expected.yml\n'
            + re.escape(
                '@@ -5,4 +5,4 @@\n'
                + ' \n'
                + ' key1: 1\n'
                + ' key2:\n'
                + '-  key3: 3\n'
                + '+  key3: 999\n'
            )
        ))

    def _check_view_has_been_called(self, times):
        expect(self._delegate.records).to(have_length(times))

        for record in self._delegate.records:
            expect(record.actual_file_path.as_posix()).to(end_with('/actual.yml'))
            expect(record.expected_file_path.as_posix()).to(end_with('/expected.yml'))
            expect(record.actual_text).to(equal(self._test_data_from('expected-actual-temp.yml')))
            expect(record.expected_text).to(equal(self._test_data_from('expected-expected-temp.yml')))


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

import os
import re
import csv
import sys
from pathlib import Path
from typing import Dict, List, Set, Union, Iterable

from Lab6.simple_reporter import SimpleReporter
from functools import reduce
from Lab5.parser import parse_metadata, parse_data
from series_validator import ThresholdDetector, SeriesValidator
from time_series import TimeSeries

filename_pattern = re.compile(r'.*(?P<year>\d{4})_(?P<parameter>.+)_(?P<frequency>[^_]+)\.csv$')


class Measurements:
    path: str
    metadata: Dict[str, str]
    cache_data: Dict[str, List[TimeSeries]]
    cache_length: Dict[str, int]
    cache_stations: Dict[str, List[str]]
    filenames: Set[str]

    def __init__(self, path: Union[str, Path]) -> None:
        path = Path(path)
        self.path = os.path.normpath(path.absolute())
        self.metadata = parse_metadata(self.path + r'\stacje.csv')
        self.cache_data = {}
        self.cache_length = {}
        self.cache_stations = {}
        self.filenames = set()
        for filename in os.listdir(self.path + "\\measurements"):
            self.filenames.add(filename)

    def get_column_count(self, filename: str) -> int:
        if filename not in self.cache_length:
            with open(self.path + '/' + filename, 'r', encoding='UTF-8') as file:
                reader = csv.reader(file)
                self.cache_length[filename] = len(next(reader)) - 1
        return self.cache_length[filename]

    def __len__(self) -> int:
        return reduce(lambda acc, filename: acc + self.get_column_count(filename), self.filenames, 0)

    def __contains__(self, parameter: str) -> bool:
        for filename in self.filenames:
            fileinfo = filename_pattern.match(filename)
            if fileinfo and fileinfo.group('parameter') == parameter:
                if self.get_column_count(filename) > 0:
                    return True
        return False

    def get_file_data(self, filename: str) -> List[TimeSeries]:
        if filename not in self.cache_data:
            datalist = parse_data(self.path + r'\measurements' + '\\' + filename)
            self.cache_stations[filename] = list(map(lambda x: x['Kod stacji'], datalist))
            self.cache_data[filename] = TimeSeries.make_from_list(datalist)
        return self.cache_data[filename]

    def get_stations(self, filename: str) -> List[str]:
        if filename not in self.cache_stations:
            with open(self.path + '\\measurements\\' + filename, 'r', encoding='UTF-8') as file:
                reader = csv.reader(file)
                line = next(reader)
                while line[0] != 'Kod stacji':
                    line = next(reader)
                self.cache_stations[filename] = line[1:]
        return self.cache_stations[filename]

    def get_by_parameter(self, parameter: str) -> List[List[TimeSeries]]:
        result = []
        for filename in self.filenames:
            fileinfo = filename_pattern.match(filename)
            if fileinfo and fileinfo.group('parameter') == parameter:
                result.append(self.get_file_data(filename))
        return result

    def get_by_station(self, station: str) -> List[TimeSeries]:
        result: List[TimeSeries] = []
        for filename in self.filenames:
            if station in self.get_stations(filename):
                for timeseries in self.get_file_data(filename):
                    if timeseries.station_code == station:
                        result.append(timeseries)
        return result

    def detect_all_anomalies(self, validators: Iterable[SeriesValidator], preload: bool = False) -> List[str]:
        result: List[str] = []

        def detect_in_list(series_list: List[TimeSeries]) -> List[str]:
            local_result: List[str] = []
            for timeseries in series_list:
                for validator in validators:
                    local_result.extend(validator.analyze(timeseries))
            return local_result

        if preload:
            for filename in self.filenames:
                result.extend(detect_in_list(self.get_file_data(filename)))
        else:
            for series_list in self.cache_data.values():
                result.extend(detect_in_list(series_list))

        return result


if __name__ == "__main__":
    test = Measurements("../Lab5/data")
    validators : Iterable[SeriesValidator] = [ThresholdDetector(70), SimpleReporter()]
    print(test.get_by_station('DsOsieczow21'))
    print(test.detect_all_anomalies(validators, preload=True))

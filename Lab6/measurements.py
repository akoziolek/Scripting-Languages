import sys
from pathlib import Path
from simple_reporter import SimpleReporter

import csv
import os
import re
from functools import reduce
import time_series

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Lab5.parser import *
from series_validator import *
from time_series import TimeSeries
from typing import Pattern


filename_pattern: Pattern = re.compile(r'.*(?P<year>\d{4})_(?P<parameter>.+)_(?P<frequency>[^_]+)\.csv$')

class Measurements:
    def __init__(self, path):
        path = Path(path)
        self.path = os.path.normpath(path.absolute())
        self.metadata = parse_metadata(self.path + r'\stacje.csv')
        self.cache_data = {}
        self.cache_length = {}
        self.cache_stations = {}
        self.filenames = set()
        for filename in os.listdir(self.path + "\\measurements"):
            self.filenames.add(filename)



    def get_column_count(self,filename):
        if filename not in self.cache_length:
            with open(self.path + '/' + filename, 'r', encoding='UTF-8') as file:
                reader = csv.reader(file)
                self.cache_length.update({filename : len(next(reader)) - 1})
        return self.cache_length[filename]

    def __len__(self):
        reduce(lambda acc, filename : acc + self.get_column_count(filename), self.filenames, 0)

    def __contains__(self, parameter):
        for filename in self.filenames:
            fileinfo = filename_pattern.match(filename)
            if fileinfo.group('parameter') == parameter:
                if self.get_column_count(filename) > 0:
                    return True
        return False

    def get_file_data(self, filename):
        if filename not in self.cache_data:
            datalist = parse_data(self.path + r'\measurements' + '\\' + filename)
            self.cache_stations.update({filename : list(map(lambda x : x['Kod stacji'], datalist))})
            self.cache_data[filename] = TimeSeries.make_from_list(datalist)
        return self.cache_data[filename]

    def get_stations(self, filename):
        if filename not in self.cache_stations:
            with open(self.path + '\\measurements\\' + filename, 'r', encoding='UTF-8') as file:
                reader = csv.reader(file)
                line = next(reader)
                while line[0] != 'Kod stacji':
                    line = next(reader)
                self.cache_stations.update({filename: line[1:]})
        return self.cache_stations[filename]


    def get_by_parameter(self, parameter):
        result = []
        for filename in self.filenames:
            fileinfo = filename_pattern.match(filename)
            if fileinfo.group('parameter') == parameter:
                result.append(self.get_file_data(filename))
        return result

    def get_by_station(self, station):
        result = []
        for filename in self.filenames:
            if station in self.get_stations(filename):
                for timeseries in self.get_file_data(filename):
                    if timeseries.station_code == station:
                        result.append(timeseries)
        return result

    def detect_all_anomalies(self, validators, preload = False):
        result = []
        def detect_in_list(list):
            result = []
            for timeseries in list:
                for validator in validators:
                    result.extend(validator.analyze(timeseries))
            return result

        if preload:
            for filename in self.filenames:
                result.extend(detect_in_list(self.get_file_data(filename)))
        else:
            for list in self.cache_data.values():
                result.extend(detect_in_list(list))

        return result


if __name__ == "__main__":
    test = Measurements("../Lab5/data")
    validators = [ThresholdDetector(70), SimpleReporter()]
    # print(test.get_by_station('DsOsieczow21'))
    print(test.detect_all_anomalies(validators, preload=True))
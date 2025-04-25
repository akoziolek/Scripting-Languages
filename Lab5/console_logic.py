import os
import random
import re
import statistics
from datetime import datetime
import console_logger, logging
import parser


logger = logging.getLogger(__name__)

def getFiles(args):
    begin_date = datetime.strptime(args.begin, '%Y-%m-%d')
    end_date = datetime.strptime(args.end, '%Y-%m-%d')

    def validate_path(path):
        pattern = r'.*(?P<year>\d{4})_(?P<parameter>.+)_(?P<frequency>[^_]+)\.csv$'
        pattern = re.compile(pattern)
        match = pattern.match(path)
        return (match and match.group('parameter') == args.parameter and match.group('frequency') == args.frequency and
                begin_date.year <= int(match.group('year')) <= end_date.year)

    files = list(filter(validate_path, os.listdir('./data/measurements')))
    if not files:
        logger.warning(f"No files found for parameter '{args.parameter}' and frequency '{args.frequency}' in the given date range.")
    return files


def handle_random(args):
    begin_date = datetime.strptime(args.begin, '%Y-%m-%d')
    end_date = datetime.strptime(args.end, '%Y-%m-%d')
    def isCorrect(station):
        for date in station['Pomiary'].keys():
            dateAsDate = datetime.strptime(date, '%m/%d/%y %H:%M')
            if begin_date <= dateAsDate <= end_date and station['Pomiary'][date] is not None and station['Pomiary'][
                date] != 0:
                return True
        return False

    def getMetaData(code):
        metadata = parser.parse_metadata('./data/stacje.csv')
        for station in metadata:
            if station['Kod stacji'] == code:
                return station

    filelist = getFiles(args)

    if not filelist:
        logger.warning("No files available for the given parameters.")
        return
    
    random_file = filelist[random.randint(0, len(filelist) - 1)]
    data = parser.parse_data('./data/measurements/' + random_file)
    filtered_data = list(filter(isCorrect, data))
    
    if not filtered_data:
        logger.warning("No stations found with the appropriate data.")
        return
    
    random_station = filtered_data[random.randint(0, len(data) - 1)]['Kod stacji']
    info = getMetaData(random_station)
    if not info:
        logger.warning(f"Station metadata not found for station code '{random_station}'.")
        return
    
    print(info['Kod stacji'])
    print(info['Miejscowość'] + (", " + info['Adres'] if info['Adres'] != info['Miejscowość'] else ""))

def handle_average(args):
    filelist = getFiles(args)
    if not filelist:
        logger.warning("No files available for the given parameters.")
        return
    
    begin_date = datetime.strptime(args.begin, '%Y-%m-%d')
    end_date = datetime.strptime(args.end, '%Y-%m-%d')
    pomiary = []
    for file in filelist:
        data = parser.parse_data('./data/measurements/' + file)
        checkedStation = None
        for station in data:
            if station['Kod stacji'] == args.station:
                checkedStation = station
                break
        if checkedStation is not None:
            values = [float(v) for k, v in checkedStation['Pomiary'].items() if
                      begin_date <= datetime.strptime(k, '%m/%d/%y %H:%M') <= end_date]
            pomiary.extend(values)
        else:
            logger.warning(f"Station '{args.station}' does not support the given parameter or frequency.")
    
    if not pomiary:
        logger.warning(f"No measurements found for station '{args.station}' in the given date range.")
        return
    
    print("Średnia pomiarów: " + str(statistics.mean(pomiary)) + ", odchylenie standardowe: " + str(
        statistics.stdev(pomiary)))
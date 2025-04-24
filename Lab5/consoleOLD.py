import argparse
import os
import random
import re
import statistics
from datetime import datetime
import console_logger, logging
import parser


logger = logging.getLogger(__name__)

arg_parser = argparse.ArgumentParser()
subparser = arg_parser.add_subparsers(dest = 'command')
subparser.add_parser('random')
sub = subparser.add_parser('average')
sub.add_argument('station')
arg_parser.add_argument('parameter', help = 'Szukana mierzona wielkość')
arg_parser.add_argument('frequency', help = 'Szukana częstotliwość')
arg_parser.add_argument('begin', help = 'Początek szukanego przedziału czasowego')
arg_parser.add_argument('end', help = 'Koniec szukanego przedziału czasowego')

args = arg_parser.parse_args()

begin_date = datetime.strptime(args.begin, '%Y-%m-%d')
end_date = datetime.strptime(args.end, '%Y-%m-%d')

def validate_path(path):
    pattern = r'.*(?P<year>\d{4})_(?P<parameter>.+)_(?P<frequency>[^_]+)\.csv$'
    pattern = re.compile(pattern)
    match = pattern.match(path)
    return (match and match.group('parameter') == args.parameter and match.group('frequency') == args.frequency and
    begin_date.year <= int(match.group('year')) <= end_date.year)

def isCorrect(station):
    for date in station['Pomiary'].keys():
        dateAsDate = datetime.strptime(date, '%m/%d/%y %H:%M')
        if begin_date <= dateAsDate <= end_date and station['Pomiary'][date] is not None and station['Pomiary'][date] != 0:
            return True
        
    logger.warning(f'No measurements available for station {station} in the {begin_date}-{end_date}')
    return False

def getMetaData(code):
    metadata = parser.parse_metadata('./data/stacje.csv')
    for station in metadata:
        if station['Kod stacji'] == code:
            return station

filelist = list(filter(validate_path, os.listdir('./data/measurements')))
print(filelist)

if args.command == 'random':
    random_file = filelist[random.randint(0, len(filelist) - 1)]
    data = parser.parse_data('./data/measurements/' + random_file, True)
    filtered_data = list(filter(isCorrect, data))
    print('s')
    if not filtered_data: 
        print('fs')
        logger.debug('No stations found with the appropriate data')
        

    random_station = filtered_data[random.randint(0, len(data) - 1)]['Kod stacji']
    info = getMetaData(random_station)

    if info is None:
        logger.warning('No metadata found for the selected station.')
    else:
        print(info['Kod stacji'])
        print(info['Miejscowość'] + (", " + info['Adres'] if info['Adres']!=info['Miejscowość'] else ""))

elif args.command == 'average':
    pomiary = []
    for file in filelist:
        data = parser.parse_data('./data/measurements/' + file, True)
        checkedStation = None
        for station in data:
            if station['Kod stacji'] == args.station:
                checkedStation = station
                break

        if checkedStation is not None:
            if args.parameter not in checkedStation['Wskaźnik']:
                logging.warning(f'Parameter "{args.parameter}" is not supported by {args.station}.')
                continue

            if args.frequency != checkedStation['Czas uśredniania']:
                logging.warning(f'Frequency "{args.frequency}" is not supported by {args.station}.')
                continue

            values = [float(v) for k, v in checkedStation['Pomiary'].items() if begin_date <= datetime.strptime(k, '%m/%d/%y %H:%M') <= end_date]
            if not values:
                logging.warning(f'No measurements for station {args.station} in the {begin_date}-{end_date}')
            pomiary.extend(values)
        else:
            logging.warning(f'Station {args.station} was not found {file}')

    print("Średnia pomiarów: " + str(statistics.mean(pomiary)) + ", odchylenie standardowe: " + str(statistics.stdev(pomiary)))
import argparse
import os
import random
import re
from datetime import datetime
import parser
import console_logger, logging

logger = logging.getLogger(__name__)


arg_parser = argparse.ArgumentParser()
subparser = arg_parser.add_subparsers(dest = 'command')
subparser.add_parser('random')
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
    print(path)
    match = pattern.match(path)
    print(match.group('year'), match.group('parameter'), match.group('frequency'))
    return (match and match.group('parameter') == args.parameter and match.group('frequency') == args.frequency and
    begin_date.year <= int(match.group('year')) <= end_date.year)


if args.command == 'random':
    filelist = list(filter(validate_path, os.listdir('./data/measurements')))
    if not filelist: logger.warning('No measurement files matching the criteria.')
    
    random_file = filelist[random.randint(0, len(filelist) - 1)]
    data = parser.parse_data('./data/measurements/' + random_file, True, True)
    random_station = data[random.randint(0, len(data) - 1)]
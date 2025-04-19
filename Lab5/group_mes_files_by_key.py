from pathlib import Path
import sys
import re
from pprint import pprint

def get_measurement_by_key(dir_path):
    path = Path(dir_path)
    if not path.is_dir(): raise ValueError('Expected directory path in <get_measurment_by_key')

    csv_files = list(path.glob('*.csv'))
    files = {} 
    pattern = r'((?P<yr>\d{4})_(?P<type>[a-zA-Z0-9\(\)]+)_(?P<fq>\d+[a-zA-Z]).[a-zA-Z]+$)'
    #skompilowac??, z dolarem?

    for file in csv_files:
        matched = re.match(pattern, file.name)
        if matched: files[(matched.group('yr'), matched.group('type'), matched.group('fq'))] =  file.resolve()

    pprint(files)
    return files
#czy powinno być z WindowsPath ?
if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise Exception('Expected one argument.')

    get_measurement_by_key(sys.argv[1])
import csv
import console_logger, logging
import os
from pathlib import Path
from os import listdir
import io


logger = logging.getLogger(__name__)

metanames = ["Nr",
             "Kod stacji",
             "Kod międzynarodowy",
             "Nazwa stacji",
             "Stary Kod stacji",
             "Data uruchomienia",
             "Data zamknięcia",
             "Typ stacji",
             "Typ obszaru",
             "Rodzaj stacji",
             "Województwo",
             "Miejscowość",
             "Adres",
             "Długość geograficzna",
             "Szerokość geograficzna"]


def validate_path(file_path, format, enable_logging=False):
    if not os.path.exists(file_path):
        if enable_logging: logger.error(f'Path "{file_path}" doesn\'t exist')
        raise FileNotFoundError(f'Path {file_path} doesn\'t exist')
    
    if not os.path.isfile(file_path):
        if enable_logging: logger.error(f'"{file_path}" is not a file')
        raise FileNotFoundError(f'"{file_path}" is not a file')
    
    if os.path.splitext(file_path)[1] != format:
        if enable_logging: logger.error(f'"{file_path}" is not an excepted type of: {type}')
        raise FileExistsError(f'"{file_path}" is not an excepted type of: {type}')

def log_read_bytes(line, enable_logging=False):
    if enable_logging:
        logger.debug(f'Read line bytes: {len(line)}')

def convert_to_csv_line(row):
    return (','.join(row) + '\n').encode('utf-8')

def parse_data(path, enable_logging=False):
    validate_path(path, '.csv', True)

    try:
        with open (path, 'r', encoding='UTF-8') as file:
            if enable_logging: logger.info(f'File "{file.name}" has been opened')

            reader = csv.reader(file)
            loglist = []
            line = next(reader)

            for i in range(1, len(line)):
                loglist.append({line[0] : line[i]})

            log_read_bytes(convert_to_csv_line(line), enable_logging)

            for i in range(5):
                line = next(reader)
                log_read_bytes(convert_to_csv_line(line), enable_logging)
                for j in range(1,len(line)):
                    loglist[j-1].update({line[0] : line[j]})

            for dic in loglist:
                dic.update({'Pomiary' : {}})

            for line in reader:
                log_read_bytes(convert_to_csv_line(line), enable_logging)

                for i in range(1,len(line)):
                    loglist[i-1]['Pomiary'].update({line[0] : line[i]})
            

    except:
        if enable_logging: logger.error(f'An error occured while reading "{path}" file')

    finally:
        if enable_logging: logger.info(f'File :{file.name}" has been closed')


    return loglist
    # Lista słowników, z czego każdy słownik zawiera dane jednej stacji - klucz nazwa zmiennej wartość wartość,
    # pomiary są jedną z tych zmiennych o nazwie "Pomiary", wartość jest słownikiem klucz data wartość wynik pomiaru

def parse_metadata(path, enable_logging=False, as_dict=False,) -> dict | list:
    validate_path(path, '.csv', enable_logging)

    try:
        with open(path, 'r', encoding='UTF-8') as file:
            if enable_logging:
                logger.info(f'File "{file.name}" has been opened')

            reader = csv.DictReader(file)
            skip_keys = ['Nr', 'Kod stacji']
            result = {} if as_dict else []

            for row in reader:
                log_read_bytes(convert_to_csv_line(row.values()), enable_logging)
                if as_dict:
                    station_code = row.get('Kod stacji')
                    if station_code:
                        filtered_row = {k: v for k, v in row.items() if k not in skip_keys}
                        result[station_code] = filtered_row
                else:
                    result.append(row)

            return result

    except Exception as e:
        if enable_logging:
            logger.error(f'An error occurred while reading "{path}" file: {e}')
        raise 

    finally:
        if enable_logging:
            logger.info(f'File "{path}" has been closed')


def parse(metadata: Path, measurements: Path):
    result = parse_metadata(metadata, as_dict=True) # dict of station code - other info
    files = listdir(measurements)
    
    for file in files: # measurements files
    
        reader = parse_data(f"{measurements}/{file}")  # list of dict

        for station_data in reader: # process each station in the measurement file
            station_code = station_data.get('Kod stacji') 

            if not station_code: continue

            station_metadata = result.setdefault(station_code, {}) # ensure the station exists in the metadata
            pomiary = station_metadata.setdefault('Pomiary', {})
            stanowisko_code = station_data.get('Kod stanowiska', 'Unknown')

            pomiary.setdefault(stanowisko_code, {}).update(station_data['Pomiary'])

    return result # dict of stations with data and Pomiary for different Kod stanowiska

if __name__ == '__main__':
    # print(parse_data('data/measurements/2023_As(PM10)_24g.csv')[0])
    # print()
    # print(parse_metadata('data/stacje.csv')[0])
    
    result = parse('data/stacje.csv', 'data/measurements')

    for i, (key, value) in enumerate(result.items()):
        if i >= 10:  # Display only the first 10 entries
            break
        print(f"Entry {i + 1}:")
        print(f"Key: {key}")
        print(f"Value: {value}")
        print("-" * 40)
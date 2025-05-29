import csv
import re

import Lab5.console_logger, logging
import os
from pathlib import Path
import datetime

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
        with open(path, 'r', encoding='UTF-8') as file:
            if enable_logging: logger.info(f'File "{file.name}" has been opened')

            reader = csv.reader(file)
            loglist = []
            line = next(reader)

            for i in range(1, len(line)):
                loglist.append({line[0]: line[i]})

            log_read_bytes(convert_to_csv_line(line), enable_logging)

            line = next(reader)
            datepattern = re.compile(r'^\d{2}/\d{2}/\d{2} \d{2}:\d{2}$')
            while not re.match(datepattern, line[0]):
                log_read_bytes(convert_to_csv_line(line), enable_logging)
                for j in range(1, len(line)):
                    loglist[j - 1].update({line[0]: line[j]})
                line = next(reader)

            for dic in loglist:
                dic.update({'Pomiary': {}})

            def handle_measurements_line(line):
                log_read_bytes(convert_to_csv_line(line), enable_logging)
                date = line[0]
                if date in loglist[0]['Pomiary']:
                    date = datetime.strptime(date, '%m/%d/%y %H:%M')
                    date += datetime.timedelta(hours=12)
                    date = date.strftime('%m/%d/%y %H:%M')
                for i in range(1, len(line)):
                    loglist[i - 1]['Pomiary'].update({date: line[i]})

            handle_measurements_line(line)
            for line in reader:
                handle_measurements_line(line)

            for line in reader:
                log_read_bytes(convert_to_csv_line(line), enable_logging)

                for i in range(1, len(line)):
                    loglist[i - 1]['Pomiary'].update({line[0]: line[i]})


    except:
        if enable_logging: logger.error(f'An error occured while reading "{path}" file')

    finally:
        if enable_logging: logger.info(f'File :{file.name}" has been closed')

    return loglist
    # Lista słowników, z czego każdy słownik zawiera dane jednej stacji - klucz nazwa zmiennej wartość wartość,
    # pomiary są jedną z tych zmiennych o nazwie "Pomiary", wartość jest słownikiem klucz data wartość wynik pomiaru


def parse_metadata(path, enable_logging=False, as_dict=False, ):
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


if __name__ == '__main__':
    print(parse_data('data/measurements/2023_As(PM10)_24g.csv')[0])
    # print()
    # print(parse_metadata('data/stacje.csv')[0])

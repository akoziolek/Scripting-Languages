import os
import random
import re
import statistics
from datetime import datetime
import console_logger, logging
import parser
from itertools import groupby

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
    info = parser.parse_metadata('./data/stacje.csv', as_dict=True)[random_station]
    if not info:
        logger.warning(f"Station metadata not found for station code '{random_station}'.")
        return
    
    print(random_station)
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
            values = [0 if v=='' else float(v) for k, v in checkedStation['Pomiary'].items() if
                      begin_date <= datetime.strptime(k, '%m/%d/%y %H:%M') <= end_date]
            pomiary.extend(values)
        else:
            logger.warning(f"Station '{args.station}' does not support the given parameter or frequency.")
    
    if not pomiary:
        logger.warning(f"No measurements found for station '{args.station}' in the given date range.")
        return
    
    print("Średnia pomiarów: " + str(statistics.mean(pomiary)) + ", odchylenie standardowe: " + str(
        statistics.stdev(pomiary)))
    
def anomalies(args):
    # Znajdujemy pliki z podanym parametrem i częstotliwością
    filelist = getFiles(args)
    if not filelist:
        logger.warning("No files available for the given parameters.")
        return
    
    begin_date = datetime.strptime(args.begin, '%Y-%m-%d')
    end_date = datetime.strptime(args.end, '%Y-%m-%d')
    measurements = []
    
    for file in filelist:
        data = parser.parse_data('./data/measurements/' + file) # Wczytujemy dane
        checkedStation = None

        for station in data: # Wczytuja sie jako lista słowników, więc iterujemy i szukamy
            if station['Kod stacji'] == args.station:
                checkedStation = station
                break

        if checkedStation is not None: # Jeśli znaleźliśmy to możemy pobrać pomiary
            values = []
            for time, value in checkedStation['Pomiary'].items():
                if begin_date <= datetime.strptime(time, '%m/%d/%y %H:%M') <= end_date:
                    values.append((time, value, args.station, args.parameter))
            measurements.extend(values)
        else:
            logger.warning(f"Station '{args.station}' does not support the given parameter or frequency.")

    return anomalies_analysis(measurements)

# Dla każdego pomiaru mogły by być inne granice
ANOMALIES_CHANGE = 'change'
ANOMALIES_THRESHOLD = 'alarm_threshold'
ANOMALIES_NONE = 'none_ratio'

ANOMALIES = {
   ('SO2'): {
       ANOMALIES_CHANGE: 2.0,
       ANOMALIES_THRESHOLD: 3.8,
       ANOMALIES_NONE: 0.5
   },
   ('As(PM10)'): {
       ANOMALIES_CHANGE: 2.0,
       ANOMALIES_THRESHOLD: 9.2,
       ANOMALIES_NONE: 0.2
   },
}

# lista pomiarów (czas, wartość, stacja, wielkość)
def anomalies_analysis(measurements):
    # Zakładam że moga byc to pomiary z różnych stacji o różnych wartościach
    measurements.sort(key=lambda x:(x[2], x[3]))
    grouped_mes = groupby(measurements, key=lambda x: (x[2], x[3]))
    anomalies = {} # Klucz - para stacja - parametr, wartość - tablica anomalii

    # Pomiary posortowane według parametru i stacji
    for key, group in grouped_mes:
        current_anomalies = []
        none_count = 0

        prev_value = None

        # Pobieramy granice dla danych parametrów
        max_change = ANOMALIES[key[1]][ANOMALIES_CHANGE]
        max_value = ANOMALIES[key[1]][ANOMALIES_THRESHOLD]

        for time, value, station, parameter in group:
            if value is None or value == '' or float(value) <= 0:
                none_count += 1
                continue

            value = float(value)

            if prev_value is not None and abs(value - prev_value) > max_change:
                current_anomalies.append(f'Sudden jump: {prev_value} -> {value} (delta: {abs(prev_value - value):.2f})')

            prev_value = value

            if value > max_value:
                current_anomalies.append(f'{time}: Value {value} over the alarm threshold ({max_value})')

        none_ratio = none_count / len(list(group))
        if none_ratio > ANOMALIES[key[1]][ANOMALIES_NONE]: 
            current_anomalies.append(f"Too many none/inccorect values: {none_ratio:.1%}")

        if current_anomalies: anomalies[(key[0], key[1])] = current_anomalies
    
    for station_value, anomaly_list in anomalies.items():
        print(station_value)
        for anomaly in anomaly_list:
            print(anomaly)

    return anomalies
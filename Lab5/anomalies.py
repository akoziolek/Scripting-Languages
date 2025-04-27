from datetime import datetime
import argparse
from pathlib import Path
import parser as my_parser
import console_logic
import re
import os 
import logging

logger = logging.getLogger(__name__)

def detect_anomalies(measurements, delta_threshold=200, none_threshold=0.2, alarm_threshold=500):
    if not measurements:
        print("No data.")
        return

    none_count = 0
    alarm_count = 0
    sudden_jumps = []

    prev_value = None
    anomalies = []
    for m in measurements:
        val = m["value"]
        time = m["time"]

        # None / ujemne / 0
        if val is None or val == '' or float(val) <= 0:
            none_count += 1
            continue

        val = float(val)

        if prev_value is not None and abs(val - prev_value) > delta_threshold:
            sudden_jumps.append((time, val, prev_value))

        if float(val) > alarm_threshold:
            alarm_count += 1
            anomalies.append(f"Analyzing {m['station']}  -  {m['parameter']}")
            anomalies.append(f"{time}: Value {val} over the alarm threshold ({alarm_threshold})")

        prev_value = val

    none_ratio = none_count / len(measurements)
    
    if none_ratio > none_threshold:
        anomalies.append(f"Analyzing {m['station']}  -  {m['parameter']}")
        anomalies.append(f"Too many none/inccorect values: {none_ratio:.1%}")

    for t, v, p in sudden_jumps:
        anomalies.append(f"Analyzing {m['station']}  -  {m['parameter']}")
        anomalies.append(f"{t}: Rapid jumps: {p} → {v} (delta = {abs(v - p):.2f})")
    
    return anomalies


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')

    detect_parser = subparsers.add_parser("detect-anomalies")
    detect_parser.add_argument("--delta", "-d", type=float, default=20)
    detect_parser.add_argument("--nones", "-n", type=float, default=0.1)
    detect_parser.add_argument("--alarm", "-a", type=float, default=200)

    args = parser.parse_args()

    if args.command == "detect-anomalies":
        def validate_path(path):
            pattern = r'.*(?P<year>\d{4})_(?P<parameter>.+)_(?P<frequency>[^_]+)\.csv$'
            pattern = re.compile(pattern)
            match = pattern.match(path)
            return match

        files = list(filter(validate_path, os.listdir('./data/measurements')))


    anomalies = []

    for file in files:
        file_path = os.path.join('./data/measurements', file)
        stations_data = my_parser.parse_data(file_path) # dict

        for column in stations_data:
            all_measurements = []
            for date, value in column['Pomiary'].items():
                all_measurements.append({
                                "time": date,
                                "value": value,
                                "station": column['Kod stacji'],
                                "parameter": column['Wskaźnik']
                            })
                
                
            current_anomalies = detect_anomalies(
                all_measurements,
                delta_threshold=args.delta,
                none_threshold=args.nones,
                alarm_threshold=args.alarm
            )

            if current_anomalies: anomalies.append(current_anomalies)

            print(anomalies[-1][:10])

           


 
""" if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')

    detect_parser = subparsers.add_parser("detect-anomalies")
    detect_parser.add_argument("--delta", "-d", type=float, default=50)
    detect_parser.add_argument("--nones", "-n", type=float, default=0.1)
    detect_parser.add_argument("--alarm", "-a", type=float, default=200)

    args = parser.parse_args()

    if args.command == "detect-anomalies":
        data = my_parser.parse(Path("data/stacje.csv"), Path("data/measurements"))

        for station_code, station_data in data.items():
            for stanowisko, pomiary in station_data.get("Pomiary", {}).items():
                for parameter, value in pomiary.items():
                    if parameter == "Jednostka":
                        continue

                    all_measurements = []
                    try:
                        for date, val in value.items():
                            dt = datetime.strptime(date, "%m/%d/%y %H:%M")
                            fv = float(val) if val != "" else None
                            all_measurements.append({
                                "time": dt,
                                "value": fv,
                                "station": station_code,
                                "parameter": parameter
                            })
                    except Exception as e:
                        continue

                    print("\n" + "=" * 40)
                    print(f"Analyzing {station_code} - {parameter}")
                    detect_anomalies(
                        all_measurements,
                        delta_threshold=args.delta,
                        none_threshold=args.nones,
                        alarm_threshold=args.alarm
                    )

 """

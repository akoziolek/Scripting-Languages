from datetime import datetime
import argparse
from pathlib import Path
import parser as my_parser


def detect_anomalies(measurements, delta_threshold=200, none_threshold=0.2, alarm_threshold=500):
    if not measurements:
        print("No data.")
        return

    station = args.station
    parameter = args.parameter

    print(f"Anomalies analysis: {station} - {parameter}")

    none_count = 0
    alarm_count = 0
    sudden_jumps = []

    prev_value = None

    for m in measurements:
        val = m["value"]
        time = m["time"]

        # None / ujemne / 0
        if val is None or val <= 0:
            none_count += 1
            continue

        if prev_value is not None and abs(val - prev_value) > delta_threshold:
            sudden_jumps.append((time, val, prev_value))

        if val > alarm_threshold:
            alarm_count += 1
            print(f"{time}: Value {val} over the alarm threshold ({alarm_threshold})")

        prev_value = val

    none_ratio = none_count / len(measurements)
    
    if none_ratio > none_threshold:
        print(f"Too many none/inccorect values: {none_ratio:.1%}")

    for t, v, p in sudden_jumps:
        print(f"{t}: Rapid jumps: {p} → {v} (delta = {abs(v - p):.2f})")

    if not sudden_jumps and alarm_count == 0 and none_ratio <= none_threshold:
        print("No anomalies")

if __name__ == "__main__":
    data = parse(Path("data/stacje.csv"), Path("data/measurements"))

    for station_code, station_data in data.items():
        pomiary_data = station_data.get("Pomiary", {})

        for stanowisko, param_data in pomiary_data.items():
            for param_name in param_data:
                if param_name == "Jednostka":
                    continue

                all_measurements = []

                for date_str, val in param_data[param_name].items():
                    try:
                        dt = datetime.strptime(date_str, "%m/%d/%y %H:%M")
                        fv = float(val) if val != "" else None
                        all_measurements.append({
                            "time": dt,
                            "value": fv,
                            "station": station_code,
                            "parameter": param_name
                        })
                    except:
                        continue

                print(f"\n--- Analyzing: Station={station_code}, Param={param_name}, Stanowisko={stanowisko} ---")
                detect_anomalies(
                    all_measurements,
                    delta_threshold=50,  # or set custom thresholds
                    none_threshold=0.1,
                    alarm_threshold=200
                )



if __name__ == "__main__":
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


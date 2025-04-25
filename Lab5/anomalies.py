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
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')

    detect_parser = subparsers.add_parser("detect-anomalies")
    detect_parser.add_argument("station")
    detect_parser.add_argument("parameter")
    detect_parser.add_argument("--delta", "-d", type=float, default=50)
    detect_parser.add_argument("--nones", "-n", type=float, default=0.1)
    detect_parser.add_argument("--alarm", "-a", type=float, default=200)

    args = parser.parse_args()

    if args.command == "detect-anomalies":
        data = my_parser.parse(Path("data/stacje.csv"), Path("data/measurements"))
        station_data = data.get(args.station)

        if station_data is None:
            print(f"Station {args.station} hasn't been found.")
            exit()

        all_measurements = []

        for stanowisko, values in station_data.get("Pomiary", {}).items():
            if args.parameter not in stanowisko:
                continue
            for date, val in values.items():
                if date == "Jednostka":
                    continue
                try:
                    dt = datetime.strptime(date, "%m/%d/%y %H:%M")
                    fv = float(val) if val != "" else None
                    all_measurements.append({
                        "time": dt,
                        "value": fv,
                        "station": args.station,
                        "parameter": args.parameter
                    })
                except:
                    continue

        detect_anomalies(
            all_measurements,
            delta_threshold=args.delta,
            none_threshold=args.nones,
            alarm_threshold=args.alarm
        )

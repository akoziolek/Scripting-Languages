import argparse
import os
import csv
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from create_sqlalchemy import Base, Station, Rental

def convert_to_timestamp(date_str):
    dt = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    return dt.timestamp()

def get_or_create_station(session, station_name):
    station = session.query(Station).filter_by(station_name=station_name).first()
    if station:
        return station
    station = Station(station_name=station_name)
    session.add(station)
    session.commit()
    return station

def load_data_into_database(data_file, database_name):
    if not os.path.exists(data_file):
        raise FileNotFoundError(f"Data file '{data_file}' not found")
    if not os.path.isfile(data_file):
        raise FileNotFoundError(f"'{data_file}' is not a file")
    if not database_name.endswith('.sqlite3'):
        raise ValueError("Database name should end with '.sqlite3'")

    db_url = f'sqlite:///{database_name}'
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    session = Session()

    with open(data_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for line in reader:
            rental_station_name = line['Stacja wynajmu']
            return_station_name = line['Stacja zwrotu']

            rental_station = get_or_create_station(session, rental_station_name)
            return_station = get_or_create_station(session, return_station_name)

            rental_id = int(line['UID wynajmu'])
            bike_number = int(line['Numer roweru'])
            start_time = convert_to_timestamp(line['Data wynajmu'])
            end_time = convert_to_timestamp(line['Data zwrotu'])
            duration = int(line['Czas trwania'])

            # Avoid duplicate IDs - Insert or ignore strategy
            exists = session.query(Rental).filter_by(id=rental_id).first()
            if exists:
                continue

            rental = Rental(
                id=rental_id,
                bike_number=bike_number,
                start_time=start_time,
                end_time=end_time,
                rental_station=rental_station.id,
                return_station=return_station.id,
                duration=duration
            )
            session.add(rental)
        session.commit()
    session.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Load CSV data into SQLAlchemy DB')
    parser.add_argument('data_file', help='CSV file with rental data')
    parser.add_argument('database_name', help='SQLite database filename (with .sqlite3 extension)')
    args = parser.parse_args()

    load_data_into_database(args.data_file, args.database_name)

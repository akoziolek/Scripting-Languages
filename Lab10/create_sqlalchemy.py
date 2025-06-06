import argparse
import os
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

class Station(Base):
    __tablename__ = 'Stations'
    id = Column(Integer, primary_key=True)
    station_name = Column(String, unique=True, nullable=False)

class Rental(Base):
    __tablename__ = 'Rentals'
    id = Column(Integer, primary_key=True)
    bike_number = Column(Integer, nullable=False)
    start_time = Column(Float, nullable=False)  # Unix timestamp float
    end_time = Column(Float)
    rental_station_id = Column(Integer, ForeignKey('Stations.id'), nullable=False)
    return_station_id = Column(Integer, ForeignKey('Stations.id'))
    duration = Column(Integer)

    rental_station = relationship('Station', foreign_keys=[rental_station_id])
    return_station = relationship('Station', foreign_keys=[return_station_id])

def init_database(db_url, force=False):
    # db_url like 'sqlite:///yourdb.sqlite3'
    db_path = db_url.replace('sqlite:///', '')
    if os.path.exists(db_path):
        if not force:
            print("Database exists. Use --force to overwrite.")
            return
        else:
            os.remove(db_path)

    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    print(f'Database created at {db_path}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create database schema with SQLAlchemy.')
    parser.add_argument('database_name', help='SQLite DB filename, e.g. rentals.sqlite3')
    parser.add_argument('--force', '-f', action='store_true', help='Force overwrite if exists')
    args = parser.parse_args()

    db_url = f'sqlite:///{args.database_name}'
    init_database(db_url, args.force)

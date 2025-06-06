import sqlite3
import argparse
import os

def init_database(database_name, force=False):
    database_name = os.path.splitext(database_name)[0] + '.sqlite3'
    
    if os.path.exists(database_name):
        if not force:
            print("Database creation aborted. Database with this name already exists.")
            return
        else:
            os.remove(database_name)
        
    conn = sqlite3.connect(database_name)
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()
    
    c.execute('''CREATE TABLE Rentals
              (id INTEGER PRIMARY KEY, 
              bike_number INTEGER NOT NULL,
              start_time REAL NOT NULL, 
              end_time REAL,
              rental_station INTEGER NOT NULL,
              return_station INTEGER,
              duration INTEGER,
              
              FOREIGN KEY (rental_station) REFERENCES Stations(id),
              FOREIGN KEY (return_station) REFERENCES Stations(id))''')
    
    c.execute('''CREATE TABLE Stations
              (id INTEGER PRIMARY KEY, 
              station_name TEXT NOT NULL UNIQUE)''')
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Initialize SQLite database for bike rentals.')
    parser.add_argument('database_name', help='Name of the SQLite database file.')
    parser.add_argument('--force', '-f', action='store_true', help='Force overwrite if database already exists')
    args = parser.parse_args()
    init_database(args.database_name, args.force)
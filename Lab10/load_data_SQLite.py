import argparse
import os
import csv
import sqlite3
from datetime import datetime 

def validate_path(file_path, format):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f'Path {file_path} doesn\'t exist')

    if not os.path.isfile(file_path):
        raise FileNotFoundError(f'"{file_path}" is not a file')

    if os.path.splitext(file_path)[1] != format:
        raise FileExistsError(f'"{file_path}" is not an excepted type of: {type}')
    

def get_or_add_station(conn, station_name):
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM Stations WHERE station_name = ?', (station_name,))
    row = cursor.fetchone()
    
    if row: return row[0]
    
    cursor.execute('INSERT INTO Stations (station_name) VALUES (?)', (station_name,))
    conn.commit()
    return cursor.lastrowid

def convert_to_timestamp(date_str):
    date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    return date.timestamp()
    
def load_data_into_database(data_file, database_name):
    database_name = os.path.splitext(database_name)[0] + '.sqlite3'
        
    validate_path(data_file, '.csv')
    validate_path(database_name, '.sqlite3')
    
    conn = sqlite3.connect(database_name)
    conn.execute("PRAGMA foreign_keys = 1")
    cursor = conn.cursor()
    
    try:
        with open(data_file, 'r', encoding='UTF-8') as file:
            reader = csv.DictReader(file)
            for line in reader:
                rental_station = line['Stacja wynajmu']
                rental_station_id = get_or_add_station(conn, rental_station)
                
                return_station = line['Stacja zwrotu']
                return_station_id = get_or_add_station(conn, return_station)
                
                #można też REPLACE, zależy od strategii dodawania nowych rekordów
                cursor.execute('''INSERT OR IGNORE INTO Rentals (id, bike_number, start_time, end_time, rental_station, return_station, duration)
                          VALUES(?, ?, ?, ?, ?, ?, ?)''', 
                          (int(line['UID wynajmu']), int(line['Numer roweru']),\
                              convert_to_timestamp(line['Data wynajmu']), convert_to_timestamp(line['Data zwrotu']),\
                                  rental_station_id, return_station_id, int(line['Czas trwania'])))
                
        conn.commit()
        conn.close()
              
    except:
        raise Exception('An error occured during loading the data.')
        


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Load history of rentals into given database.')
    parser.add_argument('data_file', help='Name of file with data to be inputted into database')
    parser.add_argument('database_name', help='Name of the SQLite database file.')
    args = parser.parse_args()
    
    load_data_into_database(args.data_file, args.database_name)
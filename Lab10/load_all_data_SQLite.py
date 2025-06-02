import subprocess
import argparse

def add_all_data(database_name):
    for i in range(1, 13):
        index = f'{i:02}'
        filename = f'data/historia_przejazdow_2021-{index}.csv'
        subprocess.run(['python',b'load_data.py', filename, f'{database_name}',], check=True)
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Load history of all rentals into given database.')
    parser.add_argument('database_name', help='Name of the SQLite database file.')
    args = parser.parse_args()
    
    add_all_data(args.database_name)
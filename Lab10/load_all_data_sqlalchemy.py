import argparse
import subprocess

def add_all_data(database_name):
    for i in range(1, 13):
        index = f'{i:02}'
        filename = f'data/historia_przejazdow_2021-{index}.csv'
        subprocess.run(['python', 'load_data_sqlalchemy.py', filename, database_name], check=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Load all rental CSV files into database.')
    parser.add_argument('database_name', help='SQLite database filename (with .sqlite3 extension)')
    args = parser.parse_args()

    add_all_data(args.database_name)

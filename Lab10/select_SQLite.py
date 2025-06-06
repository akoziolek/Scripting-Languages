from datetime import datetime
import sqlite3

def query_avg_duration(database_name, column_name, station_id):
    if column_name not in ('rental_station', 'return_station'):
        raise ValueError('Invalid column name')
    
    conn = sqlite3.connect(database_name)
    conn.execute('PRAGMA foreign_keys = 1')
    cursor = conn.cursor()

    sql = f'''
        SELECT AVG(duration)
        FROM Rentals
        WHERE {column_name} = ?
    '''
    cursor.execute(sql, (station_id,))
    result = cursor.fetchone()[0]
    conn.close()

    if result is not None:
        return round(result, 2)
    else:
        return None


def logs_by_station(db_path, station_name):
    query = """
            SELECT r.id, r.bike_number, \
                   datetime(r.start_time, 'unixepoch') as start_time, \
                   datetime(r.end_time, 'unixepoch')   as end_time, \
                   rs.station_name                     as rental_station_name, \
                   ret_s.station_name                  as return_station_name
            FROM Rentals r
                     JOIN Stations rs ON r.rental_station = rs.id
                     JOIN Stations ret_s ON r.return_station = ret_s.id
            WHERE rs.station_name = ? \
               OR ret_s.station_name = ?
            ORDER BY start_time \
            """

    try:
        with sqlite3.connect(db_path) as conn:
            conn.execute("PRAGMA foreign_keys = 1")
            cursor = conn.cursor()
            cursor.execute(query, (station_name, station_name))

            
            logs = []
            for row in cursor.fetchall():
                logs.append((
                    row[0],
                    row[1],
                    datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S'),
                    datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S'),
                    row[4],
                    row[5]
                ))
            return logs

    except sqlite3.Error:
        raise Exception(f'Error connecting to database: {sqlite3.Error}')
    
    
    
def average_duration_rental_stat(database_name, rental_station_id):
    return query_avg_duration(database_name, 'rental_station', rental_station_id)

def average_duration_return_stat(database_name, return_station_id):
    return query_avg_duration(database_name, 'return_station', return_station_id)

    
def num_of_diff_bikes(database_name, station_id):
    conn = sqlite3.connect(database_name)
    conn.execute("PRAGMA foreign_keys = 1")
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT COUNT(DISTINCT bike_number)
        FROM Rentals
        WHERE return_station = ?
    ''', (station_id,))
    
    result = cursor.fetchone()[0]
    conn.close()
    
    if result is not None: return round(result, 2)
    else: return None


def top_used_stations(database_name, column_name, limit=10):
    if column_name not in ('rental_station', 'return_station'):
        raise ValueError('Invalid column name')
    
    conn = sqlite3.connect(database_name)
    conn.execute("PRAGMA foreign_keys = 1")
    cursor = conn.cursor()
     
     
    #numery    
    cursor.execute(f'''
        SELECT {column_name}, COUNT(*) AS trips_count
        FROM Rentals
        GROUP BY {column_name}
        ORDER BY trips_count DESC
        LIMIT ?
    ''', (limit,))
    
    # nazwy stacji
    
    # cursor.execute(f'''
    #     SELECT s.station_name, COUNT(*) AS trips_count
    #     FROM Rentals r
    #     JOIN Stations s ON r.{column_name} = s.id
    #     GROUP BY s.station_name
    #     ORDER BY trips_count DESC
    #     LIMIT ?
    # ''', (limit,))
    
    results = cursor.fetchall()
    conn.close()
    return results


def get_all_station_names(database_name):
    try:
        with sqlite3.connect(database_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT station_name FROM Stations ORDER BY station_name")
            return [row[0] for row in cursor.fetchall()]
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []

def get_all_stations(database_name):
    try:
        with sqlite3.connect(database_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Stations ORDER BY station_name")
            return [(row[1], row[0]) for row in cursor.fetchall()]
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []

def top_rental_stations(database_name, limit=10):
    return top_used_stations(database_name, 'rental_station', limit)

def top_return_stations(database_name, limit=10):
    return top_used_stations(database_name, 'return_station', limit)

def most_common_return_station(database_name, rental_station_id):
    try:
        with sqlite3.connect(database_name) as conn:
            cursor = conn.cursor()
            cursor.execute('PRAGMA foreign_keys = 1')

            query = '''
                SELECT s.station_name, COUNT(*) as count
                FROM Rentals r
                JOIN Stations s ON r.return_station = s.id
                WHERE r.rental_station = ?
                GROUP BY r.return_station
                ORDER BY count DESC
                LIMIT 1
            '''
            cursor.execute(query, (rental_station_id,))
            result = cursor.fetchone()
            return result[0] if result else None

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

if __name__ == '__main__':
    print(average_duration_rental_stat('rentals.sqlite3', 12))
    print(average_duration_return_stat('rentals.sqlite3', 12))
    print(average_duration_return_stat('rentals.sqlite3', 1232142314))
    print(num_of_diff_bikes('rentals.sqlite3', 12))
    print(num_of_diff_bikes('rentals.sqlite3', 1453465752))
    print(top_rental_stations('rentals.sqlite3'))
    print(top_return_stations('rentals.sqlite3'))
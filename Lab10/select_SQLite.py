import sqlite3

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


def top_rental_stations(database_name, limit=10):
    return top_used_stations(database_name, 'rental_station', limit)

def top_return_stations(database_name, limit=10):
    return top_used_stations(database_name, 'return_station', limit)


print(average_duration_rental_stat('rentals.sqlite3', 12))
print(average_duration_return_stat('rentals.sqlite3', 12))
print(average_duration_return_stat('rentals.sqlite3', 1232142314))
print(num_of_diff_bikes('rentals.sqlite3', 12))
print(num_of_diff_bikes('rentals.sqlite3', 1453465752))
print(top_rental_stations('rentals.sqlite3'))
print(top_return_stations('rentals.sqlite3'))
from sqlalchemy import create_engine, func, distinct, or_
from sqlalchemy.orm import sessionmaker, aliased
from create_sqlalchemy import Station, Rental
from datetime import datetime

def get_session(database_name):
    db_url = f'sqlite:///{database_name}'
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    return Session()

def average_duration_rental_stat(database_name, rental_station):
    session = get_session(database_name)
    avg_duration = session.query(func.avg(Rental.duration))\
        .filter(Rental.rental_station_id == rental_station).scalar()
    session.close()
    return round(avg_duration, 2) if avg_duration else None

def average_duration_return_stat(database_name, return_station_id):
    session = get_session(database_name)
    avg_duration = session.query(func.avg(Rental.duration))\
        .filter(Rental.return_station_id == return_station_id).scalar()
    session.close()
    return round(avg_duration, 2) if avg_duration else None

def num_of_diff_bikes(database_name, station_id):
    session = get_session(database_name)
    count = session.query(func.count(distinct(Rental.bike_number)))\
        .filter(Rental.return_station_id == station_id).scalar()
    session.close()
    return count if count else None

def logs_by_station(database_name, station_name):
    session = get_session(database_name)

    # Aliases for Stations to join twice for rental and return stations
    rs_alias = aliased(Station)
    ret_alias = aliased(Station)

    results = session.query(
        Rental.id,
        Rental.bike_number,
        Rental.start_time,
        Rental.end_time,
        rs_alias.station_name.label('rental_station_name'),
        ret_alias.station_name.label('return_station_name'),
    ).join(rs_alias, Rental.rental_station_id == rs_alias.id)\
     .join(ret_alias, Rental.return_station_id == ret_alias.id)\
     .filter(or_(rs_alias.station_name == station_name, ret_alias.station_name == station_name))\
     .order_by(Rental.start_time).all()

    logs = []
    for row in results:
        logs.append((
            row[0],
            row[1],
            datetime.fromtimestamp(row[2]),
            datetime.fromtimestamp(row[3]),
            row[4],
            row[5]
        ))
    session.close()
    return logs

def top_used_stations(database_name, column_name, limit=10):
    if column_name not in ('rental_station', 'return_station'):
        raise ValueError('Invalid column name')

    session = get_session(database_name)

    from sqlalchemy import desc
    col = getattr(Rental, column_name)

    result = session.query(col, func.count().label('trips_count'))\
        .group_by(col)\
        .order_by(desc('trips_count'))\
        .limit(limit).all()

    session.close()
    return result

def get_all_station_names(database_name):
    session = get_session(database_name)
    result = session.query(Station.station_name).order_by(Station.station_name).all()
    session.close()
    return [r[0] for r in result]

def get_all_stations(database_name):
    session = get_session(database_name)
    result = session.query(Station.station_name, Station.id).order_by(Station.station_name).all()
    session.close()
    return [(r[0], r[1]) for r in result]

def top_rental_stations(database_name, limit=10):
    return top_used_stations(database_name, 'rental_station', limit)

def top_return_stations(database_name, limit=10):
    return top_used_stations(database_name, 'return_station', limit)

def most_common_return_station(database_name, rental_station_id):
    session = get_session(database_name)
    from sqlalchemy import desc

    res = session.query(
        Station.station_name,
        func.count(Rental.id).label('count')
    ).join(Rental, Rental.return_station_id == Station.id)\
     .filter(Rental.rental_station_id == rental_station_id)\
     .group_by(Rental.return_station_id)\
     .order_by(desc('count'))\
     .limit(1).first()
    session.close()
    return res[0] if res else None


if __name__ == '__main__':
    db = 'rentals.sqlite3'
    print(average_duration_rental_stat(db, 12))
    print(average_duration_return_stat(db, 12))
    print(average_duration_return_stat(db, 1232142314))
    print(num_of_diff_bikes(db, 12))
    print(num_of_diff_bikes(db, 1453465752))
    print(top_rental_stations(db))
    print(top_return_stations(db))

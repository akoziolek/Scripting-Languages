from datetime import datetime

class Station:
    def __init__(self, code: str, international_code: str, name: str, old_code: str, start_date: datetime, closing_date: datetime, station_type: str, area_type: str, station_kind: str, voivodeship: str, city: str, address: str, latitude: float, longitude: float) -> None:
        self.code = code
        self.international_code = international_code
        self.name = name
        self.old_code = old_code
        self.start_date = start_date
        self.closing_date = closing_date
        self.station_type = station_type
        self.area_type = area_type
        self.station_kind = station_kind
        self.voivodeship = voivodeship
        self.city = city
        self.address = address
        self.latitude = latitude
        self.longitude = longitude

    def __str__(self) -> str:
        return (
            f'Station code: {self.code}\n'
            f'Station international code: {self.international_code}\n'
            f'Station name: {self.name}\n'
            f'Station old code: {self.old_code}\n'
            f'Start date: {self.start_date}\n'
            f'End date: {self.closing_date}\n'
            f'Station type: {self.station_type}\n'
            f'Area type: {self.area_type}\n'
            f'Station kind: {self.station_kind}\n'
            f'Voivodeship: {self.voivodeship}\n'
            f'City: {self.city}\n'
            f'Address: {self.address}\n'
            f'Latitude: {self.latitude}\n'
            f'Longitude: {self.longitude}\n'
        )

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({', '.join(f'{k}={v!r}' for k, v in vars(self).items())})'

    def __eq__(self, value: object) -> bool:
        if isinstance(value, Station):
            return self.code == value.code
        return False

if __name__ == '__main__':
    station1 = Station('DsBialka', '', 'Białka', '', datetime(1990, 1, 3), datetime(2005, 12, 31), 'przemysłowa', 'podmiejski', 'kontenerowa stacjonarna', 'DOLNOŚLĄSKIE', 'Białka', '', 51.197783, 16.117390)
    print(station1.__str__())
    print(station1.__repr__())
    station2 = Station('DsBialka', '', 'Białka', '', datetime(1990, 1, 3), datetime(2005, 12, 31), 'przemysłowa', 'podmiejski', 'kontenerowa stacjonarna', 'DOLNOŚLĄSKIE', 'Białka', '', 51.197783, 16.117390)
    print(station1.__eq__(station2))
    station3 = Station('DsBielGrot', '', 'Bielawa - ul. Grota Roweckiego', '', datetime(1994, 1, 2), datetime(2003, 12, 31), 'tło', 'miejski', 'w budynku', 'DOLNOŚLĄSKIE', 'Bielawa', 'ul. Grota Roweckiego 6', 50.682510, 16.617348)
    print(station3.__repr__())
    print(station2.__eq__(station3))
    print(station3.__eq__(2))
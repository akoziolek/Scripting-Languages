import re
from pprint import pprint
import parser
 
POLISH_TO_LATIN_NO_SPACES = {
    'ą': 'a',
    'ć': 'c',
    'ę': 'e',
    'ł': 'l',
    'ń': 'n',
    'ó': 'o',
    'ś': 's',
    'ź': 'z',
    'ż': 'z',
    'Ą': 'A',
    'Ć': 'C',
    'Ę': 'E',
    'Ł': 'L',
    'Ń': 'N',
    'Ó': 'O',
    'Ś': 'S',
    'Ź': 'Z',
    'Ż': 'Z',
    " ": "_"   
}

def get_dates(csv_file_path):
    stations = parser.parse_metadata(csv_file_path)
    dates = []
    pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')

    for station in stations:
        current_dates = []
        for date in station['Data uruchomienia'], station['Data zamknięcia']:
            if pattern.match(date): current_dates.append(date)

        dates.append(current_dates)

    return dates

def get_latitude_and_longitude(csv_file_path):
    stations = parser.parse_metadata(csv_file_path)
    coordinates = []
    pattern = re.compile(r'^\d{1,3}.\d{6}$')

    for station in stations:
        current_coordinates = []
        for coordinate in station['Długość geograficzna'], station['Szerokość geograficzna']:
            if pattern.match(coordinate): current_coordinates.append(coordinate)
        
        coordinates.append(current_coordinates)

    return coordinates

def get_names_with_two_parts(csv_file_path):
    stations = parser.parse_metadata(csv_file_path)
    pattern = re.compile(r'^[^-,]+\s*-\s*[^-,]+$') #(r'^[^-,]+\s*-\s*[^-,]+$')
    
    return [station['Nazwa stacji'] for station in stations if pattern.match(re.sub(r'\(.*?\)|".*?"', '', station['Nazwa stacji']))] #nie bierzemy pod uwage myślników w () i ""

def rename_stations_names(csv_file_path):
    stations = parser.parse_metadata(csv_file_path)
    pattern = re.compile('|'.join(POLISH_TO_LATIN_NO_SPACES.keys()))

    for station in stations:
        station['Nazwa stacji'] = pattern.sub(lambda c: POLISH_TO_LATIN_NO_SPACES[c.group()], station['Nazwa stacji'])

    return stations

def are_MOB(csv_file_path):
    stations = parser.parse_metadata(csv_file_path)
    pattern_code = re.compile(r'.*MOB$')
    pattern_type = re.compile(r'^mobilna$')
    return [station for station in stations if pattern_code.match(station['Kod stacji']) and not pattern_type.match(station['Rodzaj stacji'])]


#dla lokalizacji nie ma wiecej niz 1 -, wiec zakladam ze chodzi o nazwe stacji
def three_part_locations(csv_file_path):
    stations = parser.parse_metadata(csv_file_path)
    # pattern = re.compile(r'^(?:[^-,]+(?: - [^-,]+){2}|[^-,]+(?:-[^-,]+){2})$')
    pattern = re.compile(r'^(?:[^-,]+(?:\s*-\s*[^-,]+){2})$')

    return [station['Nazwa stacji'] for station in stations if pattern.match(re.sub(r'\(.*?\)', '', station['Nazwa stacji']))] #usuwam nawiasy, bo tam tez sa mysliniki 


def get_streets(csv_file_path):
    stations = parser.parse_metadata(csv_file_path)
    pattern = re.compile(r'^(?:ul\.|al\.)\s*[a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ\s]+,\s*.+$')
    return [station['Adres'] for station in stations if pattern.match(station['Adres'])]


if __name__ == '__main__':

    # pprint(get_dates('./data/stacje.csv'))
    # pprint(get_latitude_and_longitude('./data/stacje.csv'))
    # pprint(get_names_with_two_parts('./data/stacje.csv'))
    # pprint(are_MOB('./data/stacje.csv'))
    # pprint(get_names_with_two_parts('./data/stacje.csv'))
    # pprint(rename_stations_names('./data/stacje.csv')[:10])
    # pprint(three_part_locations('./data/stacje.csv'))
    pprint(get_streets('./data/stacje.csv'))

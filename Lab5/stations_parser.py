import sys
import pandas as pd
from itertools import islice
import re
from pprint import pprint
#zostawiam w spokoju

#narazie wczytywanie w kazdej funkcji pliku, ale po skończeniu pierwszego zadania mozna je tu uzyc
#jesli byloby w stanie dane pola wyluskac to byloby juz latwiej 

def get_dates(csv_file):
    dates = []
    with open(csv_file, 'r', encoding='utf-8') as file:
        for line in islice(file, 2, None): #skipping first line
            dates.append(re.findall(r'\b\d{4}-\d{2}-\d{2}\b', line))
            #print(line)
            #print(dates[-1])

    pprint(dates)
    return dates

def get_latitude_and_longitude(csv_file):
    coordinates = []
    with open(csv_file, 'r', encoding='utf-8') as file:
        for line in islice(file, 2, None):
            coordinates.append(re.findall(r'\b\d{1,3}.\d{6}\b', line))
            print(coordinates[-1])
            print(line)

    #pprint(coordinates)
    return coordinates

#zakladam ze chodzi o nazwy, w ktorych - jest otoczony spacjami, bo inaczej to idk za duzo mozliwosci wychodzi
#^-poczatek, .+dowolny ciag znakow, \s-\s myslnik otoczony spacjami.+dowolny ciag po myslniku, $ koniec linii
#tutaj zwracam juz jedynie stacje z myślnikami, a nie wszytskie
def get_names_with_two_parts(csv_file):
    names = []
    with open(csv_file, 'r', encoding='utf-8') as file:
        for line in islice(file, 3, None):
            matched = re.findall(r'\b^.+\s-\s.+$\b', line) #ewentualnie bez tych spacji
            if matched:
                names.append(matched)
            
            print(names[-1])
            print(line)

    pprint(names)
    print(len(names))

if __name__ == '__main__':
    #get_dates(sys.argv[1])
    #get_latitude_and_longitude(sys.argv[1])
    get_names_with_two_parts(sys.argv[1])

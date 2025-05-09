from typing import List
from datetime import datetime, date
import numbers
from statistics import mean, stdev

class TimeSeries():
    def __init__(self, station_code: str, indicator: str, avg_time:str , unit:str, mes_dates: List[datetime] = [], mes_values: List[float | None] = []):
        if len(mes_dates) != len(mes_values):
            raise ValueError('Number of measured values and dates is different.')
        self.station_code = station_code
        self.indicator = indicator
        self.avg_time = avg_time
        self.unit = unit
        self.mes_dates = mes_dates
        self.mes_values = mes_values

    @classmethod
    def make_from_list(cls, valuelist):
        return list(map((lambda x : TimeSeries(x['Kod stacji'], x['Wskaźnik'], x['Czas uśredniania'], x['Jednostka'], list(x['Pomiary'].keys()), list(map(lambda y: 0 if y == '' or y is None else float(y), x['Pomiary'].values())))), valuelist))

    def __getitem__(self, key):
        if isinstance(key, int):
            if key < 0 or key >= len(self.mes_values):
                raise IndexError(f'Index {key} is out of range.')
            return self.mes_dates[key], self.mes_values[key]
        elif isinstance(key, slice):
            return list(zip(self.mes_dates[key], self.mes_values[key]))
        elif isinstance(key, datetime):
            return self.mes_values[self.mes_dates.index(key)]
        elif isinstance(key, date):
            results = []
            for d, v in zip(self.mes_dates, self.mes_values):
                if not isinstance(d, date):
                    continue
                if d == key:
                    results.append(v)
                elif d.date() > key:
                    break
            return results
        else:
            raise TypeError(f'Invalid argument type {type(key)}')
        
    def __getitem__(self, key: int | slice | datetime | date):
        if isinstance(key, int):
            if key < 0 or key >= len(self.mes_values):
                raise IndexError(f'Index {key} is out of range.')
            return self.mes_dates[key], self.mes_values[key]
        
        elif isinstance(key, slice):
            return list(zip(self.mes_dates[key], self.mes_values[key]))
        
        elif isinstance(key, datetime):
            return self.mes_values[self.mes_dates.index(key)]
        
        elif isinstance(key, date):
            results = []
            for d, v in zip(self.mes_dates, self.mes_values):
                if not isinstance(d, date):
                    continue
                if d.date() == key:
                    results.append(v)
                elif d.date() > key:
                    break
            return results
        else:
            raise TypeError(f'Invalid argument type {type(key)}')
        
    @property
    def mean(self):
        filtered = [v for v in self.mes_values if isinstance(v, numbers.Number)]
        return mean(filtered)

    @property
    def stddev(self):
        filtered = [v for v in self.mes_values if isinstance(v, numbers.Number)]
        return stdev(filtered)


if __name__ == '__main__':
    dates = [datetime(2001, 2, 4, 4, 32), datetime(2001, 2, 4), datetime(2001, 2, 5), datetime(2001, 2, 6), datetime(2001, 2, 8)]
    measurments = [2.1, 4.2, 1.2, 2, 6]
    series1 = TimeSeries('DsOsieczow21', 'Jony_PM25', '24g', 'ug/m3', dates, measurments)
    print(series1.__getitem__(slice(9, 4, 2)))
    print(series1.__getitem__(date(2001, 2, 4)))
    print(series1.__getitem__(datetime(2001, 2, 5)))
    print(series1.mean)
    print(series1.stddev)
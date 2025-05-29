from typing import List
from datetime import datetime, date
import numbers
from statistics import mean, stdev
from typing import List, Sequence, Union, Tuple, Dict, ClassVar

mes_values_type = Union[float, str, None]

class TimeSeries():
    def __init__(self, station_code: str, indicator: str, avg_time:str , unit:str, mes_dates: Sequence[Union[datetime, str]] = [], mes_values: Sequence[Union[mes_values_type, str]] = []) -> None:
        if len(mes_dates) != len(mes_values):
            raise ValueError('Number of measured values and dates is different.')
        self.station_code = station_code
        self.indicator = indicator
        self.avg_time = avg_time
        self.unit = unit
        self.mes_dates = mes_dates
        self.mes_values = mes_values


# tutaj jeszzcze

    @classmethod
    def make_from_list(cls, valuelist: List[Dict[str, Union[str, Dict[str, str]]]]): #meausurements(parse_data)
        return list(map((lambda x : TimeSeries(x['Kod stacji'], x['Wskaźnik'], x['Czas uśredniania'], x['Jednostka'], list(x['Pomiary'].keys()), list(map(lambda y: 0 if y == '' or y is None else float(y), x['Pomiary'].values())))), valuelist))
    
    @classmethod
    # def make_from_list(cls, valuelist: List[Dict[str, Union[str, Dict[str, str]]]]) -> List['TimeSeries']:
    #     result = []
    #     for x in valuelist:
    #         pomiary_raw = x["Pomiary"]

    #         if isinstance(pomiary_raw, dict):
    #             dates = list(pomiary_raw.keys())
    #             values = [0.0 if v == "" or v is None else float(v) for v in pomiary_raw.values()]
    #         else:
    #             dates = []
    #             values = []

    #         result.append(cls(str(x["Kod stacji"]), str(x["Wskaźnik"]), str(x["Czas uśredniania"]), str(x["Jednostka"]), dates, values))

    #     return result
 
    def __getitem__(self, key: Union[int, slice, datetime, date]) -> Union[Tuple[datetime, mes_values_type], List[Tuple[datetime, mes_values_type]], mes_values_type, List[mes_values_type]]:
        if isinstance(key, int):
            if key < 0 or key >= len(self.mes_values):
                raise IndexError(f'Index {key} is out of range.')
            return self.mes_dates[key], self.mes_values[key]
        
        elif isinstance(key, slice):
            return list(zip(self.mes_dates[key], self.mes_values[key]))
        
        elif isinstance(key, datetime):
            return self.mes_values[self.mes_dates.index(key)]
        
        elif isinstance(key, date):
            results : List[float | None] = []
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
    def mean(self) -> float:
        filtered : List[float] = [v for v in self.mes_values if v is not None]
        return mean(filtered)

    @property
    def stddev(self) -> float:
        filtered : List[float] = [v for v in self.mes_values if v is not None]
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

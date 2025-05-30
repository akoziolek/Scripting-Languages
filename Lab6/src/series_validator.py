from abc import ABC, abstractmethod
from time_series import TimeSeries
from typing import List
from datetime import datetime
import numbers
from enum import Enum
import re
from typing import List, Tuple, Optional, Union
from statistics import StatisticsError


class SeriesValidator(ABC):
    @abstractmethod
    def analyze(self, series: TimeSeries) -> List[str]:
        pass

class OutlierDetector(SeriesValidator):
    def __init__(self, k: float) -> None:
        if k < 0: raise ValueError('Parameter k must be non-negative')
        self.k = k

    def analyze(self, series: TimeSeries) -> List[str]:
        if not isinstance(series, TimeSeries):
            raise ValueError('Unexpected type of series argument')
        
        try:
            threshold: float = series.mean + self.k * series.stddev
        except StatisticsError:
            return []
        
        return [f'Measurement {series.indicator} {series.avg_time} with value {val} on {series.mes_dates[idx]} exceeded standard deviation' 
                for idx, val in enumerate(series.mes_values) if isinstance(val, numbers.Number) and val > threshold]

class ZeroSpikeDetector(SeriesValidator):
    def analyze(self, series:TimeSeries)-> List[str]:
        if not isinstance(series, TimeSeries):
            raise ValueError('Unexpected type of series argument')
        null_count: int = 0
        anomalies: List[str] = []

        def assert_anomaly(end_idx: int) -> None:
            if null_count >= 3:
                invalid_values: List[Tuple[Union[datetime, str], Optional[Union[float, int, str]]]] = \
                    list(zip(series.mes_dates[end_idx - null_count:end_idx], series.mes_values[end_idx - null_count:end_idx]))
                formatted_values: str = ", ".join([f"({d}, {v})" for d, v in invalid_values])
                anomalies.append(f"Consecutive invalid values: {formatted_values}")

        for idx, val in enumerate(series.mes_values):
            if isinstance(val, str):
                try:
                    val = float(val)
                except ValueError:
                    val = None
                    
            if val is None or val == 0:
                null_count += 1
            elif isinstance(val, (float, int)):
                assert_anomaly(idx)
                null_count = 0

        assert_anomaly(len(series.mes_values))
        return anomalies


class ThresholdDetector(SeriesValidator):
    def __init__(self, threshold: float) -> None:
        if threshold < 0: raise ValueError('Threshold must be non-negative')
        self.threshold = threshold

    def analyze(self, series:TimeSeries)-> List[str]:
        if not isinstance(series, TimeSeries):
            raise ValueError('Unexpected type of series argument')
      
        return [f'Measurement {series.indicator} {series.avg_time} with value {val} on {series.mes_dates[idx]} exceeded threshold {self.threshold}' 
                for idx, val in enumerate(series.mes_values) if isinstance(val, numbers.Number) and val > self.threshold]

class CompositeValidator(SeriesValidator):
    class LogicMode(Enum):
        AND = 'and'
        OR = 'or'

    def __init__(self, validators:List[SeriesValidator], logic_mode:LogicMode = LogicMode.OR) -> None:
        if not isinstance(logic_mode, CompositeValidator.LogicMode) or not all(isinstance(x, SeriesValidator) for x in validators):
            raise ValueError('Unexpected arguments types')
        self.validators = validators
        self.mode = logic_mode

       
    def analyze(self, series:TimeSeries) -> List[str]:
        all_messages: List[str] = []

        if self.mode == CompositeValidator.LogicMode.OR:
            for validator in self.validators:
                all_messages.extend(validator.analyze(series))
        elif self.mode == CompositeValidator.LogicMode.AND:
            for validator in self.validators:
                current_messages: List[str] = validator.analyze(series)
                if not current_messages:
                    return []
                all_messages.extend(current_messages)

        return all_messages 



if __name__ == '__main__':
    dates = [datetime(2001, 2, 4, 4), datetime(2001, 2, 4, 4, 3), datetime(2001, 2, 5), datetime(2001, 2, 6), datetime(2001, 2, 8), datetime(2001, 2, 10), datetime(2001, 2, 11), datetime(2001, 2, 12), datetime(2001, 2, 18)]
    measurments = [2.1, 4.2, 1.2, 2, 0, None, 0, None, 0]
    series = TimeSeries('DsOsieczow21', 'Jony_PM25', '24g', 'ug/m3', dates, measurments)
 
    print(OutlierDetector(0.5).analyze(series))
    print(ZeroSpikeDetector().analyze(series)) 
    

    print(OutlierDetector(1.85).analyze(series))
    print(OutlierDetector(0.2).analyze(series))
    print(OutlierDetector(0.1).analyze(series))

    print(CompositeValidator([OutlierDetector(0.85), OutlierDetector(0.2), OutlierDetector(0.1)], CompositeValidator.LogicMode.OR).analyze(series))


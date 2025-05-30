from abc import ABC, abstractmethod
from time_series import TimeSeries
from typing import List, Union
from datetime import datetime
import numbers
from enum import Enum
import re
from collections import deque
import heapq

class SeriesValidator(ABC):
    @abstractmethod
    def analyze(self, series: TimeSeries) -> List[str]:
        pass

class OutlierDetector(SeriesValidator):
    def __init__(self, k):
        if k < 0: raise ValueError('Parameter k must be non-negative')
        self.k = k

    def analyze(self, series:TimeSeries)-> List[str]:
        if not isinstance(series, TimeSeries):
            raise ValueError('Unexpected type of series argument')
        
        threshold = series.mean + self.k * series.stddev
        return [f'Measurement {series.indicator} {series.avg_time} with value {val} on {series.mes_dates[idx]} exceeded standard deviation' 
                for idx, val in enumerate(series.mes_values) if isinstance(val, numbers.Number) and val > threshold]

class ZeroSpikeDetector(SeriesValidator):
    def analyze(self, series:TimeSeries)-> List[str]:
        if not isinstance(series, TimeSeries):
            raise ValueError('Unexpected type of series argument')
        null_count = 0
        anomalies = []

        def assert_anomaly(end_idx):
            if null_count >= 3:
                invalid_values = list(zip(series.mes_dates[end_idx - null_count:end_idx], series.mes_values[end_idx - null_count:end_idx]))
                formatted_values = ", ".join([f"({d}, {v})" for d, v in invalid_values])
                anomalies.append(f"Consecutive invalid values: {formatted_values}")

        for idx, val in enumerate(series.mes_values):
            if val is None or val == 0:
                null_count += 1
            else:
                assert_anomaly(idx)
                null_count = 0

        assert_anomaly(len(series.mes_values))
        return anomalies


class ThresholdDetector(SeriesValidator):
    def __init__(self, threshold):
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

    def __init__(self, validators:List[SeriesValidator], logic_mode:LogicMode = LogicMode.OR):
        if not isinstance(logic_mode, CompositeValidator.LogicMode) or not all(isinstance(x, SeriesValidator) for x in validators):
            raise ValueError('Unexpected arguments types')
        self.validators = validators
        self.mode = logic_mode

    """     
    # Version where OR return all anomalies, AND return anomalies only if they occured on all validators
    def analyze(self, series:TimeSeries) -> List[str]:
        all_messages = []

        if self.mode == CompositeValidator.LogicMode.OR:
            for validator in self.validators:
                messages = validator.analyze(series)
                all_messages.extend(messages)
        elif self.mode == CompositeValidator.LogicMode.AND:
            for validator in self.validators:
                current_messages = validator.analyze(series)
                if not current_messages:
                    return []
                all_messages.extend(current_messages)

        return all_messages 
        """

    def __get_all_messages(self, series: TimeSeries):
        all_messages : List[deque] = []
        date_pattern = re.compile(r'^.*(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*$')

        for val_idx in range(len(self.validators)):
            messages = self.validators[val_idx].analyze(series)
            # Deque of the date, message, index of source validator
            all_messages.append(deque())

            for m in messages:
                dates = date_pattern.findall(m)
                if dates:
                    # Assuming the start of the anomaly is the most important
                    latest = min(datetime.strptime(d, "%Y-%m-%d %H:%M:%S") for d in dates)
                    all_messages[-1].append((latest, m, val_idx))

        return all_messages

    def analyze(self, series:TimeSeries)-> List[str]:
        result : List[str] = []
        heap : List[tuple] = []
        all_messages = self.__get_all_messages(series)

        if self.mode == CompositeValidator.LogicMode.AND:
            current_date = None
            date_messages = {}

            # Adding first messages from each validator to the priority queue
            for message_queue in all_messages:
                if message_queue:
                    date, message, validator_index = message_queue.popleft()
                    heapq.heappush(heap, (date, message, validator_index))

            while heap:
                # Poping the message with the earliest date
                date, message, validator_index = heapq.heappop(heap)

                # Keeping just one message for each validator
                if current_date == date:
                    date_messages[validator_index] = message
                else:
                    current_date = date
                    date_messages = {validator_index: message}

                # All validator have an anomaly
                if len(date_messages) == len(self.validators):
                    result.extend(date_messages.values()) #TU IDK CZY DOBRZE DAJE
                    current_date = None
                    date_messages = {}

                # Add next message from the same validator
                if len(all_messages[validator_index]) > 0:
                    next_message = all_messages[validator_index].popleft()
                    heapq.heappush(heap, next_message)  # Push the correct next message        
                
        elif self.mode == CompositeValidator.LogicMode.OR:
            # Adding first messages from each validator to the priority queue
            for message_queue in all_messages:
                if message_queue:
                    date, message, validator_index = message_queue.popleft()
                    heapq.heappush(heap, (date, message, validator_index))

            while heap:
                date, message, validator_index = heapq.heappop(heap)
                
                if len(all_messages[validator_index]) > 0:
                    heapq.heappush(heap, all_messages[validator_index].popleft())
                
                result.append(str(date) + " " + message)

        else:
            raise ValueError('Unsupported mode {self.mode}')
        
        return result 



if __name__ == '__main__':
    dates = [datetime(2001, 2, 4, 4), datetime(2001, 2, 4, 4, 3), datetime(2001, 2, 5), datetime(2001, 2, 6), datetime(2001, 2, 8), datetime(2001, 2, 10), datetime(2001, 2, 11), datetime(2001, 2, 12), datetime(2001, 2, 18)]
    measurments = [2.1, 4.2, 1.2, 2, 0, None, 0, None, 0]
    series = TimeSeries('DsOsieczow21', 'Jony_PM25', '24g', 'ug/m3', dates, measurments)
 
    """ 
    print(OutlierDetector(0.5).analyze(series))
    print(ZeroSpikeDetector().analyze(series)) 
    """

    print(OutlierDetector(1.85).analyze(series))
    print(OutlierDetector(0.2).analyze(series))
    print(OutlierDetector(0.1).analyze(series))

    print(CompositeValidator([OutlierDetector(0.85), OutlierDetector(0.2), OutlierDetector(0.1)], CompositeValidator.LogicMode.OR).analyze(series))

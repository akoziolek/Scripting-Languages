from series_validator import ThresholdDetector
from time_series import TimeSeries
import pytest
from datetime import datetime

@pytest.fixture
def setup_empty_time_series():
    return TimeSeries(
        station_code='DsJelGorSoko',
        indicator="BaP(PM10)",
        avg_time="24g",
        unit="mg/m3",
        mes_dates=[],
        mes_values=[]
    )
    
@pytest.fixture
def setup_zero_time_series():
    return TimeSeries(
        station_code='PrekursoryZielonka',
        indicator="135trimetylobenzen",
        avg_time="1g",
        unit="ug/m3",
        mes_dates=[datetime(2025, 5, 1, hour=i) for i in range(10)],
        mes_values=[0 for _ in range(10)],
    )
    
@pytest.fixture
def setup_time_series():
    return TimeSeries(
        station_code='PrekursoryZielonka',
        indicator="135trimetylobenzen",
        avg_time="1g",
        unit="ug/m3",
        mes_dates=[datetime(2025, 5, 1, hour=i) for i in range(5)],
        mes_values=[10 + 2*i  for i in range(5)],
    )
  
@pytest.fixture
def detector1():
    return ThresholdDetector(0.25)

@pytest.fixture
def detector2():
    return ThresholdDetector(14)

@pytest.fixture
def detector3():
    return ThresholdDetector(20)


def test_threshold_detector_empty_series(setup_empty_time_series, detector1):
    assert detector1.analyze(setup_empty_time_series) == []

def test_threshold_detector_no_outliers(setup_zero_time_series, detector1):
    assert detector1.analyze(setup_zero_time_series) == []
    
def test_threshold_detector_with_outliers1(setup_time_series, detector1):
    expected = [
        'Measurement 135trimetylobenzen 1g with value 10 on 2025-05-01 00:00:00 exceeded threshold 0.25',
        'Measurement 135trimetylobenzen 1g with value 12 on 2025-05-01 01:00:00 exceeded threshold 0.25',
        'Measurement 135trimetylobenzen 1g with value 14 on 2025-05-01 02:00:00 exceeded threshold 0.25',
        'Measurement 135trimetylobenzen 1g with value 16 on 2025-05-01 03:00:00 exceeded threshold 0.25',
        'Measurement 135trimetylobenzen 1g with value 18 on 2025-05-01 04:00:00 exceeded threshold 0.25',
    ]
    assert detector1.analyze(setup_time_series) == expected
    
def test_threshold_detector_with_outliers2(setup_time_series, detector3):
    assert detector3.analyze(setup_time_series) == []

def test_threshold_detector_with_outliers3(setup_time_series, detector2):
    expected = [
        'Measurement 135trimetylobenzen 1g with value 16 on 2025-05-01 03:00:00 exceeded threshold 14',
        'Measurement 135trimetylobenzen 1g with value 18 on 2025-05-01 04:00:00 exceeded threshold 14',
    ]
    assert detector2.analyze(setup_time_series) == expected

def test_threshold_detector_wrong_input_type(detector1):
    with pytest.raises(ValueError):
        detector1.analyze("not a time series")

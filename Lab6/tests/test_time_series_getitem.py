from time_series import TimeSeries # btw działa, bo jest konfiguracja pytest.ini
import pytest
from datetime import datetime

@pytest.fixture
def setup_time_series():
    return TimeSeries(
        station_code='DsJelGorSoko',
        indicator="BaP(PM10)",
        avg_time="24g",
        unit="mg/m3",
        mes_dates=[
            datetime(2025, 1, 1, 12, 0),
            datetime(2025, 1, 2, 11, 1),
            datetime(2025, 2, 3, 10, 2),
            datetime(2025, 2, 4, 9, 3),
            datetime(2025, 3, 5, 8, 4),
            datetime(2025, 3, 5, 8, 4),
        ],
        mes_values=[0, 0.5, 5, 0.1, 142.5, 1000]
    )
    
def test_getitem_index1(setup_time_series):
    assert setup_time_series[1] == (datetime(2025, 1, 2, 11, 1), 0.5)
    
def test_getitem_index2(setup_time_series):
    assert setup_time_series[2] == (datetime(2025, 2, 3, 10, 2), 5) 
    
def test_getitem_index_out_of_range1(setup_time_series):
    with pytest.raises(IndexError):
        setup_time_series[10]

def test_getitem_index_out_of_range2(setup_time_series):
    with pytest.raises(IndexError):
        setup_time_series[-1]
    
def test_getitem_slice1(setup_time_series):
    result = setup_time_series[1:4]
    expected = [
        (datetime(2025, 1, 2, 11, 1), 0.5),
        (datetime(2025, 2, 3, 10, 2), 5),
        (datetime(2025, 2, 4, 9, 3), 0.1),
    ]
    assert result == expected

def test_getitem_slice2(setup_time_series):
    result = setup_time_series[:-2]
    expected = [
        (datetime(2025, 1, 1, 12, 0), 0),
        (datetime(2025, 1, 2, 11, 1), 0.5),
        (datetime(2025, 2, 3, 10, 2), 5),
        (datetime(2025, 2, 4, 9, 3), 0.1),
    ]
    assert result == expected
 
def test_getitem_slice3(setup_time_series):
    result = setup_time_series[0:100]
    expected = list(zip(setup_time_series.mes_dates[0:], setup_time_series.mes_values[0:]))
    assert result == expected   
    
 
def test_getitem_slice4(setup_time_series):
    result = setup_time_series[1:7:2]
    expected = [
        (datetime(2025, 1, 2, 11, 1), 0.5),
        (datetime(2025, 2, 4, 9, 3), 0.1),
        (datetime(2025, 3, 5, 8, 4), 1000)
    ]
    assert result == expected

def test_getitem_slice_out_of_range1(setup_time_series):
    result = setup_time_series[-1:4]
    expected = []
    assert result == expected
    
def test_getitem_slice_out_of_range2(setup_time_series):
    result = setup_time_series[3:2]
    expected = []
    assert result == expected
    
def test_getitem_datetime1(setup_time_series):
    assert setup_time_series[datetime(2025, 1, 2, 11, 1)] == 0.5
    
def test_getitem_datetime2(setup_time_series):
    assert setup_time_series[datetime(2025, 3, 5, 8, 4)] == 142.5
    
def test_getitem_datetime_not_found(setup_time_series):
    with pytest.raises(ValueError):
        setup_time_series[datetime(2025, 1, 3, 11, 1)]
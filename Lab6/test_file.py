from datetime import datetime

import pytest

from series_validator import ZeroSpikeDetector, OutlierDetector, ThresholdDetector
from time_series import TimeSeries
from station import Station


def test_a():
    Station1 = Station("DsOsieczow21",'','','','','','','','','','','','','')
    Station2 = Station("DsOsieczow21", 'fwfe ', 'rgergwfc', 'wegwgre', '', '', '', '', '', '', '', '', '', '')
    Station3 = Station("DsOsieczow21 ", 'rehergw', 'rjetj', 'sddfds', '', '', '', '', '', '', '', '', '', '')

    assert Station1 == Station2
    assert Station1 != Station3
    assert Station2 != Station3

def test_c():
    dates = [datetime.now() for i in range(20)]
    values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    expected = 10.5
    series1 = TimeSeries('','','','', dates, values)
    assert series1.mean == expected
    for i in range(len(values)):
        if i % 3 == 0:
            values[i] = None
    non_nones = [v for v in values if v is not None]
    expected = sum(non_nones) / len(non_nones)
    series2 = TimeSeries('', '', '', '', dates, values)
    assert series2.mean == expected


def test_e():
    dates1 = [datetime(2023, 1, 1), datetime(2023, 1, 2), datetime(2023, 1, 3),
              datetime(2023, 1, 4), datetime(2023, 1, 5)]
    values1 = [1.0, 0, 0, 0, 2.0]
    series1 = TimeSeries("test", "indicator", "avg", "unit", dates1, values1)

    detector = ZeroSpikeDetector()
    result1 = detector.analyze(series1)
    assert len(result1) == 1
    assert "Consecutive invalid values" in result1[0]
    assert "(2023-01-02 00:00:00, 0), (2023-01-03 00:00:00, 0), (2023-01-04 00:00:00, 0)" in result1[0]

    dates2 = [datetime(2023, 1, 1), datetime(2023, 1, 2), datetime(2023, 1, 3),
              datetime(2023, 1, 4), datetime(2023, 1, 5)]
    values2 = [1.0, None, None, None, 2.0]
    series2 = TimeSeries("test", "indicator", "avg", "unit", dates2, values2)

    result2 = detector.analyze(series2)
    assert len(result2) == 1
    assert "Consecutive invalid values" in result2[0]
    assert "(2023-01-02 00:00:00, None), (2023-01-03 00:00:00, None), (2023-01-04 00:00:00, None)" in result2[0]

    dates3 = [datetime(2023, 1, 1), datetime(2023, 1, 2), datetime(2023, 1, 3),
              datetime(2023, 1, 4), datetime(2023, 1, 5)]
    values3 = [1.0, 0, None, 0, 2.0]
    series3 = TimeSeries("test", "indicator", "avg", "unit", dates3, values3)

    result3 = detector.analyze(series3)
    assert len(result3) == 1
    assert "Consecutive invalid values" in result3[0]
    assert "(2023-01-02 00:00:00, 0), (2023-01-03 00:00:00, None), (2023-01-04 00:00:00, 0)" in result3[0]

    dates4 = [datetime(2023, 1, 1), datetime(2023, 1, 2), datetime(2023, 1, 3)]
    values4 = [1.0, 0, None]
    series4 = TimeSeries("test", "indicator", "avg", "unit", dates4, values4)

    result4 = detector.analyze(series4)
    assert len(result4) == 0


# Sample test data
@pytest.fixture
def sample_time_series():
    dates = [datetime(2023, 1, 1), datetime(2023, 1, 2), datetime(2023, 1, 3),
             datetime(2023, 1, 4), datetime(2023, 1, 5), datetime(2023, 1, 6)]
    values = [1.0, 100.0, 0, 0, 0,
              50.0]  # Contains outlier (100), threshold exceed (50 if threshold=30), and zero spike
    return TimeSeries("test", "indicator", "avg", "unit", dates, values)


# Define test cases for parametrized test
test_cases = [
    (
        [OutlierDetector(k=1)],
        ["Measurement indicator avg with value 100.0 on 2023-01-02 00:00:00 exceeded standard deviation"]
    ),
    (
        [ZeroSpikeDetector()],
        ["Consecutive invalid values: (2023-01-03 00:00:00, 0), (2023-01-04 00:00:00, 0), (2023-01-05 00:00:00, 0)"]
    ),
    (
        [ThresholdDetector(threshold=30.0)],
        [
            "Measurement indicator avg with value 100.0 on 2023-01-02 00:00:00 exceeded threshold 30.0",
            "Measurement indicator avg with value 50.0 on 2023-01-06 00:00:00 exceeded threshold 30.0"
        ]
    ),
    (
        [OutlierDetector(k=1), ZeroSpikeDetector(), ThresholdDetector(threshold=30.0)],
        [
            "Measurement indicator avg with value 100.0 on 2023-01-02 00:00:00 exceeded standard deviation",
            "Consecutive invalid values: (2023-01-03 00:00:00, 0), (2023-01-04 00:00:00, 0), (2023-01-05 00:00:00, 0)",
            "Measurement indicator avg with value 100.0 on 2023-01-02 00:00:00 exceeded threshold 30.0",
            "Measurement indicator avg with value 50.0 on 2023-01-06 00:00:00 exceeded threshold 30.0"
        ]
    )
]


@pytest.mark.parametrize("validators,expected_messages", test_cases)
def test_g(sample_time_series, validators, expected_messages):
    all_messages = []
    for validator in validators:
        messages = validator.analyze(sample_time_series)
        all_messages.extend(messages)
    for expected in expected_messages:
        assert expected in all_messages
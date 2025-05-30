from typing import List

from series_validator import SeriesValidator


class SimpleReporter(SeriesValidator):
    def analyze(self, series) -> List[str]:
        return [f"Info: {series.indicator} at {series.station_code} has mean = {series.mean}"]
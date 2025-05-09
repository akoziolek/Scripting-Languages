class SimpleReporter:
    def analyze(self, series):
        return [f"Info: {series.indicator} at {series.station_code} has mean = {series.mean}"]
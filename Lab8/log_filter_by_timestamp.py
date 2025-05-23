from datetime import datetime


def get_entries_by_timestamp(log, begin_timestamp, end_timestamp):
    return [row for row in log if begin_timestamp < float(row[0]) < end_timestamp]
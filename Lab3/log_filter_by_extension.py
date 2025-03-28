def get_entries_by_extension(log, extension):
    return [row for row in log if isinstance(row[9], str) and row[9].endswith(extension)]

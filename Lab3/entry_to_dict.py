from log_parser import COLUMN_TYPES

names = list(map(lambda x: x[0], COLUMN_TYPES))

def entry_to_dict(entry):
    return dict(zip(names, entry))
import sys
import re
from datetime import datetime 

# list of column names and their types
COLUMN_TYPES = [
    ('ts', 'datetime'),
    ('uid', 'str'),
    ('id.orig_h', 'str'),
    ('id.orig_p', 'int64'),
    ('id.resp_h', 'str'),
    ('id.resp_p', 'int64'),
    ('trans_depth', 'int64'),
    ('method', 'str'),
    ('host', 'str'),
    ('uri', 'str'),
    ('referrer', 'str'),
    ('user_agent', 'str'),
    ('request_body_len', 'int64'),
    ('response_body_len', 'int64'),
    ('status_code', 'float64'),
    ('status_msg', 'str'),
    ('info_code', 'float64'),
    ('info_msg', 'str'),
    ('filename', 'float64'),
    ('tags', 'str'),
    ('username', 'str'),
    ('password', 'float64'),
    ('proxied', 'str'),
    ('orig_fuids', 'str'),
    ('orig_mime_types', 'str'),
    ('resp_fuids', 'str'),
    ('resp_mime_types', 'str')
]

#CZY CHCEMY WCZYTAC TYLKO 10 PIERWSZYCH

def parse_log():
    rows = []
    for line in sys.stdin:
        current = line.split('\t')
        if len(current) == len(COLUMN_TYPES): #accept rows of expected length
            for i in range(len(current)):
                current[i] = convert_to_type(current[i], COLUMN_TYPES[i][1])
            rows.append(tuple(current))
    return rows

def convert_to_type(value, type):
    if value == '' or value == '-' or value is None:
        return None
    try:
        if type == 'int64':
            return int(value)
        elif type == 'float64':
            return float(value)
        elif type == 'str':
            return str(value)
        elif type == 'datetime':
            return datetime.fromtimestamp(float(value))
        else:
            return None

    except ValueError:
        return value
    

def is_white_spece(char):
    return char in [' ', '\t', '\n']

def is_line_end(char):
    return char in ['\n']
  
def print_log():
    for line in sys.stdin:
        print(repr(line))
    
if __name__ == '__main__':
    parse_log()

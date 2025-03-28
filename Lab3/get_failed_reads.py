import log_parser


def get_failed_reads(log):
    fours,fives = [], []
    for row in log:
        tag = row[14]
        if tag is not None and 400 <= tag < 600:
            (fours, fives)[tag >= 500].append(row)
    return fours, fives

if __name__ == '__main__':
    log = log_parser.parse_log()
    fours, fives = get_failed_reads(log)
    print(list(map(lambda x: x[14], fours)),
          "\n\n\n--------------------------------------------------------------------------------------------\n\n\n",
          list(map(lambda x: x[14], fives)))
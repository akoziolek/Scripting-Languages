import ipaddress

import log_parser


def get_entries_by_addr(log, ip):
    try:
        ipaddress.ip_address(ip)
    except ValueError:
        raise(ValueError("Invalid IP address"))
    return list(filter(lambda row: row[2] == ip, log))

if __name__ == '__main__':
    log = log_parser.parse_log()
    print(get_entries_by_addr(log, '192.168.202.79'))
import log_parser
import log_to_dict
import itertools

def groupedby(recs, string):
    return itertools.groupby(sorted(recs, key=lambda x: x[string]), key=lambda x: x[string])

def print_dict_entry_dates(dic):
    ipaddresses = set()
    records_list = list(itertools.chain.from_iterable(dic.values()))

    for record in records_list:
        ipaddresses.add(record['id.orig_h'])
        ipaddresses.add(record['id.resp_h'])
    print(f"included ip addresses: {ipaddresses}")

    for ipaddress, records in groupedby(records_list, 'id.orig_h'):
        records = list(records)
        print(f"{ipaddress}: ")
        record_dates = list(map(lambda x: x['ts'], records))
        print(f"first request date: {min(record_dates)}, last: {max(record_dates)}")
        total = len(records)
        print(f"\ttotal requests: {total}\n\tmethod distribution:")
        methoded_recs = list(filter(lambda x: x['method'] is not None, records))
        for command, recs in groupedby(methoded_recs, 'method'):
            print(f"\t\t{command}: {len(list(recs))/total*100}%")
        number_of_2xx = sum(1 for elem in records if elem['status_code'] is not None and 300 > elem['status_code'] >= 200)
        print(f"\tpercentage of 2xx: {number_of_2xx*100/total}%\n")
    print()

if __name__ == "__main__":
    dic = log_to_dict.log_to_dict(log_parser.parse_log())
    print_dict_entry_dates(dic)
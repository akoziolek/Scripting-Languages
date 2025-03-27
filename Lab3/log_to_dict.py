from entry_to_dict import entry_to_dict

def entry_to_dict(log):
    result = []

    for entry in log:
        result[entry[1]] = entry_to_dict(entry)

    return result  
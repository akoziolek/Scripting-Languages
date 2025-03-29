from entry_to_dict import entry_to_dict


def log_to_dict(log_entries):
    log_dict = {}

    for entry in log_entries:
        uid = entry[1]
        if uid not in log_dict:
            log_dict[entry[1]] = []
        log_dict[entry[1]].append(entry_to_dict(entry))

    return log_dict
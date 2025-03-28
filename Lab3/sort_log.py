def sort_log(current_log, index):
    try:
        current_log.sort(key=lambda x : x[index])
    except TypeError:
        raise(TypeError("Cannot sort by selected index - type not comparable"))
    except IndexError:
        raise(IndexError("Index out of range"))
    return current_log


if __name__ == '__main__':
    log = [(1,2,3,4), (4,2,3,1), (3,1,4,2), (2,1,3,4)]
    print(sort_log(log, int(input())))
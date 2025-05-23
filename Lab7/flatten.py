from functools import reduce


def flatten(arg):
    if not isinstance(arg, list):
        return arg
    return reduce(
        lambda acc, elem: acc + (elem if isinstance(elem, list) else [elem]),
        list(map(lambda elem: flatten(elem), arg)),
        [])

if __name__ == '__main__':
    print(flatten([1, 2, [3,4, [5,[6],7]]]))
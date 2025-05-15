from functools import reduce


def forall(pred, thing):
    return reduce(lambda acc, elem: acc and pred(elem), thing, True)

def exists(pred, thing):
    return reduce(lambda acc, elem: acc or pred(elem), thing, False)

def at_least(n, pred, thing):
    return reduce(lambda acc, elem: acc + (1 if pred(elem) else 0), thing, 0) >= n

def at_most(n, pred, thing):
    return reduce(lambda acc, elem: acc + (1 if pred(elem) else 0), thing, 0) <= n
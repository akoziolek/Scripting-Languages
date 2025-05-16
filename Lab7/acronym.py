from functools import reduce


def acronym(wordlist):
    return reduce(lambda acc, elem: acc + elem[0], wordlist, '')

if __name__ == '__main__':
    print(acronym(['hello', 'world']))
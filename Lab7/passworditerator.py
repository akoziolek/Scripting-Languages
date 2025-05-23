import random
import string


class PasswordIterator:
    def __init__(self, length, charset, count):
        self.length = length
        self.charset = list(set(charset))
        self.count = count

    def __iter__(self):
        return self

    def __next__(self):
        self.count -= 1
        if self.count < 0:
            raise StopIteration
        password = ''
        for i in range(self.length):
            password += random.choice(self.charset)
        return password


if __name__ == '__main__':
    iter = PasswordIterator(10, string.ascii_letters, 10)
    for password in iter:
        print(password)
    for password in iter:
        print(password)
    print(next(iter))
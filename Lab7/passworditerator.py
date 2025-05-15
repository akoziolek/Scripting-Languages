import random
import string


class PasswordIterator:
    def __init__(self, length, charset, count):
        self.length = length
        self.charset = list(set(charset))
        self.count = count

    def __iter__(self):
        for i in range(self.count):
            yield self.generate_password()

    def generate_password(self):
        password = ''
        for i in range(self.length):
            password += random.choice(self.charset)
        return password


if __name__ == '__main__':
    for password in PasswordIterator(10, string.ascii_letters, 10):
        print(password)
def root(number, epsilon = 0.0000001):
    def better_answer(guess):
        return (guess + number/guess) / 2

    def proceed(guess = number/2):
        return guess if abs(number-guess*guess) < epsilon else proceed(better_answer(guess))

    return proceed()

if __name__ == '__main__':
    print(root(2))
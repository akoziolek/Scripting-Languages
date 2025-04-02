from os import environ
import sys

def print_env_variables1():
    arg = sys.argv[1:]
    print(sorted(filter(lambda env: any(f in env[0] for f in arg), environ.items())))

def print_env_variables():
    arguments = sys.argv[1:]
    found_env = []

    for arg in arguments:
        if arg in environ:
            found_env.append((arg, environ[arg]))
    print(sorted(found_env))

def print_all_env():
    for env in environ:
        print(f"{env} = {environ[env]}")

#przetestiwac wywolanie funkcji z potokowaniem (wypisania wszystkich zmiennych)

if __name__ == '__main__':
    print_all_env()
    print()
    print_env_variables()
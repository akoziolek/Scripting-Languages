from os import environ
import sys
from pprint import pprint

def print_env_variables():
    arg = sys.argv[1:]
    pprint(sorted(filter(lambda env: env[0] in arg, environ.items())))

def print_all_env():
    for env in environ.items():
        print(env)

if __name__ == '__main__':
    print_all_env()
    print()
    print_env_variables()

#LOCALAPPDATA, OS, TMP, LANG, PROMPT, APPDATA
import sys
from itertools import pairwise

sys.stdin.reconfigure(encoding="utf-8")
sys.stdout.reconfigure(encoding="utf-8")

END_OF_CONTENTS_SYMBOL = "-----"
PREAMBLE_MAX_SIZE = 10
DEFAULT_UTF = "iso-8859-2"

def is_sentence_end(sign):
    return sign == '.' or sign == '?' or sign == '!'

def is_white_sign(sign):
    return sign == ' ' or sign == '\n' or sign == '\t' or sign == '\r' or sign == '\v' or sign == '\f'

def print_text(*args):
    for el in args:
        try:
            sys.stdout.write(str(el) + '\n')
        except TypeError:
            sys.stdout.write("Wrong value type given")


#reading texts from file with option to choose the encoding
#default utf-8 set on the sys couldnt read the polish chars, but after specyfying the utf-8 problem is gone


#proccesing text without lists (split function)

def read_txt_contents(file_encoding=DEFAULT_UTF):
    
    try:
        text = ""
        idx_line = 0
        was_prev_line_empty = False
        was_Preambule = False

        for line in sys.stdin:
            line = line.strip()
            if line == END_OF_CONTENTS_SYMBOL:
                break

            elif line == '':

                if idx_line < PREAMBLE_MAX_SIZE and was_prev_line_empty and not was_Preambule:
                    text = ""
                    was_prev_line_empty = False
                    was_Preambule = True
                else:
                    if not was_prev_line_empty: text += '\n'
                    was_prev_line_empty = True

            else:
                nextLine = line[0]
                for chars in pairwise(line):
                    if chars != (' ', ' '):
                        nextLine+= chars[1]
                    if chars[0] == ' ' and is_sentence_end(chars[1]):
                        nextLine = nextLine[:-1] + chars[1]

                nextLine += '\n'
                was_prev_line_empty = False
                text += nextLine

            idx_line += 1

        if text: text = text[:-1] 

    finally:
        sys.stdin = original_stdin

    return text



def print_text(*args):
    for el in args:
        try:
            sys.stdout.write(str(el) + '\n')
        except TypeError:
            sys.stdout.write("Wrong value type given")

#sprawdzenie czy moduł uruchamiany jest bezpośrednio czy jako importowany moduł w innym skrypcie
if __name__ == '__main__':
    print_text(read_txt_contents())

    
    
    
    
    
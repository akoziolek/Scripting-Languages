from itertools import pairwise
import  text_parser

def countParagraphs():
    text = text_parser.read_txt_contents()
    betweenParagraphs = False
    paragraphCount = 0
    for chars in pairwise(text):
        if chars == ('\n','\n'):
            if not betweenParagraphs:
                paragraphCount += 1
                betweenParagraphs = True
        else:
            betweenParagraphs = False
    return paragraphCount

if __name__ == '__main__':
    print(countParagraphs())
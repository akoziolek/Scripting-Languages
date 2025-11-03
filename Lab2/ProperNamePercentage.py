from itertools import pairwise
import  text_parser
import Bin.text_parser as text_parser


def countPercentage():
    text = text_parser.read_txt_contents()

    properNameCount = 0
    sentenceCount = 0

    sentenceJustEnded = False

    wasProperName = False

    for prevChar, char in pairwise(text):
        if text_parser.is_sentence_end(char) and not sentenceJustEnded:
            if wasProperName:
                properNameCount += 1

            sentenceCount += 1
            wasProperName = False
            sentenceJustEnded = True

        elif sentenceJustEnded:
            if not text_parser.is_white_sign(char) and not text_parser.is_sentence_end(char):
                sentenceJustEnded = False

        elif char.isupper() and not sentenceJustEnded and text_parser.is_white_sign(prevChar):
            wasProperName = True

    return int(properNameCount / sentenceCount * 100)

if __name__ == '__main__':
    print(countPercentage())
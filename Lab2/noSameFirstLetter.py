from itertools import pairwise
import  text_parser


def sentences():
    text = text_parser.read_txt_contents()
    lastLetter = text[0].lower()
    currentSentence = text[0]
    result = ""

    inQuote = False

    sentenceHasEnded = False

    longest = 0

    isGood = True

    for prevchar, char in pairwise(text):
        if char == "\"" or char == "„" or char == "”":
            inQuote = not inQuote

        if text_parser.is_sentence_end(char) and not inQuote:
            currentSentence += char
            sentenceHasEnded = True
            lastLetter = ''

        else:
            if sentenceHasEnded:
                if isGood and len(currentSentence) > longest:
                    result = currentSentence
                    longest = len(currentSentence)
                sentenceHasEnded = False
                currentSentence = ""
                isGood = True
            else:
                currentSentence += char
                if text_parser.is_white_sign(prevchar):
                    if lastLetter.lower() == char.lower():
                        isGood = False
                    lastLetter = char
                    
    if isGood and len(currentSentence) > longest:
        result = currentSentence
    return result

if __name__ == "__main__":
    print(sentences())


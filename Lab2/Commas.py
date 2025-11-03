import  text_parser


def firstCommaSentence():
    text = text_parser.read_txt_contents()
    commaCounter = 0
    currentSentence = ""
    
    for char in text:
        currentSentence += char
        if char == ',':
            commaCounter += 1
        elif text_parser.is_sentence_end(char):
            if commaCounter > 1:
                return currentSentence
            commaCounter = 0
            currentSentence = ""


if __name__ == '__main__':
    print(firstCommaSentence())
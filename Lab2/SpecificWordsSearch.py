import  text_parser


def sentences():
    text = text_parser.read_txt_contents()
    currentWord = ""
    currentSentence = ""
    result = ""

    sentenceHasEnded = False
    wordCounter = 0
    for char in text:
        if text_parser.is_sentence_end(char):
            currentSentence += char
            sentenceHasEnded = True
            if currentWord == "i" or currentWord == "oraz" or currentWord == "ale" or currentWord == "że" or currentWord == "lub":
                wordCounter += 1
            currentWord = ""
        else:
            if sentenceHasEnded:
                if wordCounter >= 2:
                    result += "\n" + currentSentence
                sentenceHasEnded = False
                currentSentence = ""
                wordCounter = 0
            else:
                currentSentence += char
                if text_parser.is_white_sign(char):
                    if currentWord == "i" or currentWord == "oraz" or currentWord == "ale" or currentWord == "że" or currentWord == "lub":
                        wordCounter += 1
                    currentWord = ""

                else:
                    currentWord += char
    return result

if __name__ == "__main__":
    print(sentences())


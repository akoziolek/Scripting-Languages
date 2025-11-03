import  text_parser, sys

def sentences():
    text = text_parser.read_txt_contents()
    lastWord = ""
    currentWord = ""
    currentSentence = ""
    result = ""

    inQuote = False

    sentenceHasEnded = False

    isSorted = True

    for char in text:
        if char == "\"" or char == "„" or char == "”":
            inQuote = not inQuote
        if text_parser.is_sentence_end(char) and not inQuote:
            if lastWord.lower() > currentWord.lower():
                isSorted = False
            currentSentence += char
            sentenceHasEnded = True
            lastWord = ""
            currentWord = ""
        else:
            if sentenceHasEnded:
                if isSorted:
                    result += "\n" + currentSentence
                sentenceHasEnded = False
                currentSentence = ""
                isSorted = True
            else:
                currentSentence += char
                if text_parser.is_white_sign(char):
                    if lastWord.lower() > currentWord.lower():
                        isSorted = False
                    lastWord = currentWord
                    currentWord = ""

                else:
                    currentWord += char
    if isSorted:
        result += "\n" + currentSentence
    return result

if __name__ == "__main__":
    print(sentences())
    #sys.stdout.buffer.write(sentences().encode("utf-8"))


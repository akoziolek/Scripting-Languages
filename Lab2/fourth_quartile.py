import  text_parser
def length_fourth_quartile():
    text = text_parser.read_txt_contents()
    sentences = []
    sentence = ""
    counter = 0
    was_end = False
 
    for char in text:
        if was_end and char.isspace(): continue

        if char != '\n':
            sentence += char
            counter += 1
            was_end = False

        if text_parser.is_sentence_end(char):
            was_end = True
            sentences.append((counter, sentence))
            sentence = ""
            counter = 0

    sentences.sort(key=lambda sen: sen[0], reverse=True)
    sentences = sentences[:len(sentences)//4]

    return '\n'.join(sen[1] for sen in sentences)


if __name__ == "__main__":
    text_parser.print_text(length_fourth_quartile())
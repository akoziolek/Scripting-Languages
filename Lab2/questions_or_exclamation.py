import  text_parser

def question_or_exclamation_sen():
    sentences = ""
    current_sentence = ""
    text = text_parser.read_txt_contents()
    was_end = False

    for char in text:
       if was_end and char.isspace(): continue #skipping the space after the end of sentence

       if char != '\n':
            current_sentence += char
            was_end = False

       if text_parser.is_sentence_end(char):
           if char == '?' or char == '!' and len(current_sentence) > 2 and current_sentence[-2].isalpha():
                current_sentence += '\n'
                sentences += current_sentence
           was_end = True
           current_sentence = ""
          
    return sentences

if __name__ == "__main__":
    text_parser.print_text(question_or_exclamation_sen())
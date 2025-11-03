import  text_parser
import sys

MAX_WORD_NUMBER = 4

def filter_max_word_count(max_words_num = MAX_WORD_NUMBER):
    if max_words_num < 0: raise Exception("Can't filter for negative number of words.")
    text = text_parser.read_txt_contents()
    sentence = ''
    result = ''
    counter = 0
    was_word = False

    for letter in text:
        if was_word and not letter.isalpha(): #next word
            counter += 1
            sentence += letter
            was_word = False

        elif letter.isalpha(): 
            sentence += letter
            was_word = True
       
        if text_parser.is_sentence_end(letter):
            if (counter <= max_words_num):
                if sentence: result += sentence.strip() + '\n'
            sentence = ''
            counter = 0
        
    return result

if __name__ == "__main__":
    #sys.stdout.buffer.write(filter_max_word_count().encode("utf-8"))
    text_parser.print_text(filter_max_word_count())

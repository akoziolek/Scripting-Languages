import  text_parser

SENTENCES_LIMIT = 20

def first_n_sentences(n = SENTENCES_LIMIT):
    if n < 0: raise Exception("Can't return a negative number of sentences")
    
    text = text_parser.read_txt_contents()
    sentences = ""
    current_sentence = ""
    was_end = False

    for char in text:
       if was_end and char.isspace(): continue #skipping the space after the end of sentence
       
       if char != '\n': #skipping empty lines\ sentence endings
            current_sentence += char
            was_end = False

       if text_parser.is_sentence_end(char):
           was_end = True
           current_sentence += '\n'
           n -= 1
           sentences += current_sentence
           current_sentence = ""
        
       if n == 0: break
    
    if n != 0: raise Exception("Not enough sentences in text.")

    return sentences

if __name__ == "__main__":
    text_parser.print_text(first_n_sentences())
import  text_parser

def find_longest_sentence():
    text = text_parser.read_txt_contents()
    longest_sentence = ""
    current_sentence = ""
    was_end = False
    
    for char in text:
       if was_end and char.isspace(): continue #skipping the space after the end of sentence
       
       if char != '\n':
            current_sentence += char
            was_end = False

       if text_parser.is_sentence_end(char):
           was_end = True
           if(len(current_sentence) > len(longest_sentence)): 
                longest_sentence = current_sentence
           current_sentence = ""

    return longest_sentence

if __name__ == "__main__":
    text_parser.print_text(find_longest_sentence())

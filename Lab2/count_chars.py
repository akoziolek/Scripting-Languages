import  text_parser


def count_chars():
    text = text_parser.read_txt_contents()
    count = 0

    for char in text:
        if not text_parser.is_white_sign(char): count += 1            

    return count


if __name__ == "__main__":
    text_parser.print_text(count_chars())
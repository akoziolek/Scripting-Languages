import sys
import time
import os
from collections import deque
from datetime import datetime
import traceback

#defining accepcet tail arguments and if they require an argument
TAIL_ARGS = {
    '--follow': None,
    '--lines': int,
    'file_path': str
}

DEFAULT_LINES = 10
    
def parse_args():
    parsed_args = {}
    file_path = None
    last_idx = 0
    args = sys.argv[1:]

    for index, arg in enumerate(args):
        option, value, expected_type = None, None, None

        if arg.startswith('--'):
            if '=' in arg: option, value = arg.split('=', 1)
            else: option = arg

            if not option in TAIL_ARGS: raise ValueError('Unknown type of argument')
            expected_type = TAIL_ARGS.get(option)
        else:
            option = arg

        if expected_type == None and value != None: raise ValueError(f'Argument {option} does not take any values')
        if expected_type != None and value == None: raise ValueError(f'Argument {arg} should have a defined value of type {expected_type}')
        if option in parsed_args: raise ValueError(f'Repetition of the same argument {option}')          

        if value != None:
            #checking if the type is proper
            try:
                parsed_args[option] = expected_type(value)
            except(ValueError):
                raise ValueError(f'Value = {value} does not correspond to the expected one for {option} argument')
                
        elif option.startswith('--'):
            parsed_args[option] = True
        else:
            file_path = arg
            last_idx = index
            break #stopping after finding first non "option" argument

    #if there was sth after the path name
    if last_idx + 1 < len(sys.argv[1:]): raise ValueError('Too many arguments')
        
    return file_path, parsed_args
    

#follow only for files
#sprawdzanie czy dlugosc dodatnia?

def tail():
    file_name, args = parse_args()
    lines_number = args.get('--lines', DEFAULT_LINES)
    if lines_number < 0: raise ValueError('Cannot display negative number of lines.')
    tail_lines = deque(maxlen = lines_number)

    if file_name != None: #skipping the standard input if there is a path name provided
        #with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as process:
        if not '--follow' in args:
            from_file(tail_lines, file_name)
        else:
            from_file_follow(tail_lines, file_name)    
        
    elif not sys.stdin.isatty(): #data source from standard input (sys)
        if '--follow' in args: raise Exception(f'Unable to perform follow option for the standard input.')
        from_sys(tail_lines)    
    else:
        raise Exception(f'No standard input or file path have been provided.')
    
    print_deque(tail_lines)


def from_file(tail_deque, file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        for line in file:
            tail_deque.append(line)

#NIE DZIALA GDY ODEJMUJEMY LINIJKI, ale w poleceniu jest ze mamy sledzic dodawanie 
def from_file_follow(tail_lines, file_name):
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            file.seek(0)
            was_outputted = False

            while(True):
                current_position = file.tell() #finding the current positon of the stream
                line = file.readline()

                if not line:
                    if not was_outputted:
                        print_deque(tail_lines)
                        was_outputted = True

                    time.sleep(0.1) #waiting if no new line has been appended
                    current_size = os.stat(file_name).st_size

                    if current_size != current_position: 
                        file.seek(0) #returning to the beginning of the file if there are new lines
                        sys.stdout.write(f'\n{datetime.now().strftime('%H:%M:%S')} - Contents of the {file_name} have changed\n')
                        was_outputted = False
                        tail_lines.clear()
                else:
                    tail_lines.append(line)
    except KeyboardInterrupt: 
        print("\n[Stopped following the file]")

def from_sys(tail_deque):
    for line in sys.stdin:
        tail_deque.append(line) 

def print_deque(deq):
    while deq:
        sys.stdout.write(deq.popleft())
        sys.stdout.flush()

if __name__ == '__main__':
    try:
        tail()
    except Exception as e:
        traceback.print_exc()


# cat plik.txt | python tail.py
# type text.txt | python tail.py {--}
# python tail.py {--} plik.txt
# cat plik.txt | python tail.py {--} plik2.txt  MAMY IGNOROWAC WEJSCIE STANDARDOWE (cat/type) i wyswietlać z argumentu


#type text.txt | python tail.py   --  1 argument
#type text.txt | python tail.py d  2 argument
import sys
import time
import os

def tail_f(filename):
    with open(filename, 'r') as file:
        file.seek(0) #finding start of the file

        while(True):
            current_position = file.tell() #finding the current positon of the stream
            line = file.readline()

            if not line:
                time.sleep(0.1) #waiting if no new line has been appended
                current_size = os.stat(filename).st_size

                if current_size > current_position: 
                    file.seek(0) #returning to the beginning of the file if there are new lines
                    sys.stdout.write('\n\n')
            else:
                sys.stdout.write(line)
                sys.stdout.flush()


#defining accepcet tail arguments and if they require an argument
TAIL_ARGS = {
    '--follow': None,
    '--lines': int,
    'file_path': str
}


def parse_args2():
    parsed_args = {}
    file_path = None
    last_idx = 0
    args = sys.argv[1:]

    for index, arg in enumerate(args):
        if arg.startswith('--'):
            if not arg in TAIL_ARGS: raise Exception('Unknown type of argument')
            expected_type = TAIL_ARGS.get(arg)

            #key\value arguments
            if '=' in arg:
                key, value = arg.split('=', 1)

                #checking if the type is proper
                try:
                    if expected_type!= None: parsed_args[key] = expected_type(value)
                    else: raise Exception(f'Argument {key} does not take any values')
                    
                except(ValueError):
                    raise ValueError(f'Value = {value} does not correspond to the expected one for {key} argument')
            else:
                #option does not take any arguments
                if expected_type == None: parse_args[arg] = None
                else: raise Exception(f'Argument {arg} should have a defined value of type {expected_type}')
        else:
            file_path = arg
            last_idx = index
            break #stopping after finding first non "option" argument
    
    if last_idx + 1 < len(sys.argv[1:]): raise Exception('Too many arguments')

    print(file_path)
    print(parsed_args)
            
    return file_path, parsed_args
    

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

            if not option in TAIL_ARGS: raise Exception('Unknown type of argument')
            expected_type = TAIL_ARGS.get(option)
        else:
            option = arg

        print(option)
        print(value)

        if expected_type == None and value != None: raise Exception(f'Argument {option} does not take any values')
        if expected_type != None and value == None: raise Exception(f'Argument {arg} should have a defined value of type {expected_type}')
        if option in parsed_args: raise Exception(f'Repetition of the same argument {optiond}')          

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

    
    if last_idx + 1 < len(sys.argv[1:]): raise Exception('Too many arguments')

    print(file_path)
    print(parsed_args)
            
    return file_path, parsed_args
    

def tail():
    args = parse_args()


if __name__ == '__main__':
    tail()


# cat plik.txt | python tail.py
# type text.txt | python tail.py {--}
# python tail.py {--} plik.txt
# cat plik.txt | python tail.py {--} plik2.txt  MAMY IGNOROWAC WEJSCIE STANDARDOWE (cat/type) i wyswietlać z argumentu
 



#type text.txt | python tail.py   --  1 argument
#type text.txt | python tail.py d  2 argument
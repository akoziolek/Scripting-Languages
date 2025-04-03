import sys
import os
import time

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

import sys
from pathlib import Path
from subprocess import Popen, PIPE
import json
from pprint import pprint

def run_analysis(dir_path):
    path = Path(dir_path)
    if not path.is_dir(): raise Exception(f"Error {path} is not a directory")
    
    text_files = list(path.glob('*.txt'))
    statistics = []

    for file in text_files:
        #invoking subprocess, capturing stdout, stderr
        process = Popen(['java', 'FileAnalyzer', str(file)], stdout=PIPE, stderr=PIPE, text=True)
        stdout, stderr = process.communicate()
        if process.returncode == 0:
            statistics.append(json.loads(stdout))
        else:
            print(f"Error processing {file.name}: {stderr}")

    return statistics

def analysis_stats(statistics):
    result = {
        'number of read files': 0,
        'total characters count': 0,
        'total words count': 0,
        'total verses count': 0,
        'most common char': ('', 0),
        'most common word': ('', 0)
    }

    for stat in statistics:
        result['number of read files'] += 1
        result['total characters count'] += stat['total_characters']
        result['total words count'] += stat['total_words']
        result['total verses count'] += stat['total_lines']

        if result['most common char'][1] < stat['most_common_character_count']:
            result['most common char'] = (stat['most_common_character'], stat['most_common_character_count'])

        if result['most common word'][1] < stat['most_common_word_count']:
            result['most common word'] = (stat['most_common_word'], stat['most_common_word_count'])

    pprint(result)
    return result


if __name__ == '__main__':    
    if len(sys.argv) < 1:
        raise Exception('Too little arguments')
    analysis_stats(run_analysis(sys.argv[1]))
import argparse
import subprocess
import os
from datetime import datetime
import utils
import sys

def convert_file(input_path, output_format, output_path, program):
    """Converts file from input path into output format using the designated program"""
    output_filename = utils.output_filename(input_path, output_format)

    os.makedirs(output_path, exist_ok=True)

    output_path = os.path.join(output_path, output_filename)

    if program == 'ffmpeg':
        cmd = ['ffmpeg', '-i', input_path, output_path]
    elif program == 'magick':
        cmd = ['magick', 'convert', input_path, output_path]
    else:
        raise ValueError(f"Unsupported program: {program}")

    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print(f"Error converting {input_path}: \n{e.stderr.decode()}", file=sys.stderr)
        return None
    except FileNotFoundError as e:
        print(f"File not found: {e.filename}", file=sys.stderr)
        return None

    return output_path

def main():
    parser = argparse.ArgumentParser(description='Convert media files.')
    parser.add_argument('input_path', help='Directory containing media files')
    parser.add_argument('format', help='Target format (e.g., webm, png)')
    args = parser.parse_args()

    files = utils.get_files(args.input_path)
    if not files:
        print("No files found in input directory.", file=sys.stderr)
        return

    output_path = utils.get_output_path()
    os.makedirs(output_path, exist_ok=True)

    history_path = os.path.join(output_path, 'history.csv')

    for file_path in files:
        file_type = utils.get_file_type(file_path)
        if not file_type:
            print(f"Skipping {file_path}: unsupported file type.", file=sys.stderr)
            continue

        program = 'magick' if file_type == 'image' else 'ffmpeg'
        output_path = convert_file(file_path, args.format, output_path, program)
        if not output_path:
            continue

        entry = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'original_path': file_path,
            'output_format': args.format,
            'output_path': output_path,
            'program': program
        }
        utils.log_conversion(history_path, entry, formatting='csv')

if __name__ == '__main__':
    main()
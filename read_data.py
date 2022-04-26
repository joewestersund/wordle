import re
from os.path import abspath, expanduser

def get_file_path(filename):
    return abspath(expanduser("~/") + '/python_projects/wordle/' + filename)

def read_word_file(filename, word_length):
    # reads a data file from the downloads folder
    # filename should include file type suffix
    file_contents = []
    filepath = get_file_path(filename)
    print('Opening file', filepath)
    with open(filepath, 'r') as fh:
        for line in fh:
            line_str = line.strip().lower() # remove whitespace & make lower case
            #if len(line_str) == word_length and
            if bool(re.fullmatch('^[a-z]{5}',line_str)):  # 5 lowercase characters only
                file_contents.append(line_str)
        fh.close()
    print('file closed')
    print(f'found {len(file_contents)} words of length {word_length}')
    return file_contents
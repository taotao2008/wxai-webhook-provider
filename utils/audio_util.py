
import os
import requests


def download_file(url, filename_or_dir):

    r = requests.get(url)

    if not os.path.isdir(filename_or_dir):
        os.mkdir(filename_or_dir)

    filename = get_filename_from_url(url)
    filepath = filename_or_dir + '/' + filename
    print(filepath)
    with open(filepath, "wb") as code:
         code.write(r.content)

    return filepath

def get_filename_from_url(content):
    filename_start = str(content).rfind('/') + 1
    filename_sub_str = content[filename_start:]
    filename_end = 0
    filename_pos = str(filename_sub_str).rfind('?')
    if (filename_pos != -1):
        filename_end = filename_pos
    else:
        filename_end = len(filename_sub_str)

    filename = filename_sub_str[: int(filename_end)]
    return filename

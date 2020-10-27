import os
import json

"""
    Was made for aknerin by alekal in fiverr.com
    ---------------------------------------------
    PLACE ALL YOUR FILE INTO 'texts' DIRECTORY!
"""

INFO = {}  # Dictionary to store the info from file


def read_file(filename):
    """
    Reads file and extracts task data from it.

    :param filename: name of file to be extracted
    """
    INFO[filename] = []
    with open(f'texts/{filename}') as file:
        lines = file.readlines()
        for line in lines:
            if line.find("Task") > 0:
                line_row = line.split("(")[1].split(")")
                if len(line_row) != 0:
                    splited_line_row = line_row[0].split(',')
                    name = splited_line_row[4]
                    type1 = splited_line_row[5]
                    try:
                        type2 = splited_line_row[6]
                        type3 = splited_line_row[7]
                    except IndexError:
                        type2 = ""
                        type3 = ""
                    temp = {
                        "name": name.replace("\"", '').replace("\\n", ""),
                        "type1": type1.replace("\"", '').replace("\\n", ""),
                        "type2": type2.replace("\"", ''),
                        "type3": type3.replace("\"", ''),
                    }
                    INFO[filename].append(temp)


def run():
    """
    Main method. Runs and save extracted data into json format.

    """
    for filename in os.listdir('texts'):
        read_file(filename)
    with open('res.json', 'w') as fp:
        st = json.dumps(INFO, indent=4)
        fp.write(st)


if __name__ == '__main__':
    run()

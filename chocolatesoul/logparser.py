import os
import logging
from datetime import datetime

"""

Script to pull out lines that include certain strings, such as error codes or keywords.

Made for chocolatesoul by alekal

"""


def extract_log_data(file, keywords):
    """
    Main function to extract data by keyword.
    Keyword should be separated by commas and NO SPACE! Like: exiting,failed,zero,run,main.

    :param file: Log file to parse
    :param keywords: Words to find in file
    """
    with open(f'./logs/{file}', 'r', encoding='utf-8') as f:  # Open a file
        lines = f.readlines()   # Read lines from file
        for string in lines:  # For every line in file
            find_keyword(string, keywords)  # Find matches


def find_keyword(line_string, keywords):
    """
    Function to find keywords in log file.

    :param line_string: line from log file
    :param keywords: keywords to search
    """
    for word in keywords:
        if word.lower() in line_string.lower():  # If we find match
            print(line_string)  # Uncomment if you need to see an output in terminal
            save_to_file(line_string)  # Saving file


def save_to_file(output):
    """
    Function to save output to log file.

    :param output: Matched result
    :param keyword: keyword to search
    """
    now = datetime.now()  # Get current time
    log_dir = f'logfile_{now.hour}_{now.minute}_{now.second}.log'
    logging.basicConfig(handlers=[logging.FileHandler(filename=log_dir,
                                                      encoding='utf-8', mode='a+')],
                        level=logging.INFO)
    os.chmod(log_dir, 0o0777)
    logging.info(output)


if __name__ == '__main__':
    """
    To start the main function.
    """
    print('Files available:')
    for filename in os.listdir('logs'):  # Prints all files in logs folder
        print(filename)
    file_to_extract = input("File name (like sample.txt): ")  # Choose file to work with
    keywords = input("What are you looking for? (separate by commas): ").split(",")  # Get user input
    extract_log_data(file_to_extract, keywords)

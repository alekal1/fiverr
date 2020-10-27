import os
import csv

"""
Was created for whereas by alekal on fiverr.com

Make sure that the files, output folder and script are in the same directory!
For multiple file parsing place all your files into files directory and code will do the rest.

"""

FILE_DIR = ""
NUM_KEYS = ""
KEY_LENGTH = ""
USING_KEY_OF_LENGTH = ""
benchmark_counter = 0

BENCHMARK_TESTS = [
    [
        "Benchmark",
        "KEY_LENGTH",
        "USING_KEY_OF_LENGTH",
        "NUM_KEYS",
        "Items",
        "Latency(ms)",
        "hw_cpu_instructions",
        "hw_cpu_cycles",
        "hw_cache_misses",
        "hw_cache_references",
        "Cache miss rate",
        "Ipc"
    ]
]


def read_file(filename):
    global benchmark_counter
    with open(f'files/{filename}') as file:
        lines = file.readlines()
        for index, line in enumerate(lines):
            extract_global_attribute(line)
            if "BEGIN" in line:
                benchmark_counter += 1
                extract_benchmark_info(lines[index:], line.split(":")[2].strip())


def extract_global_attribute(line):
    """
    Extract global attributes

    :param line:
    :return:
    """
    global KEY_LENGTH, FILE_DIR, NUM_KEYS, USING_KEY_OF_LENGTH

    if "file_dir" in line:
        FILE_DIR = line.split(":")[1].strip()
    if "num_keys" in line:
        NUM_KEYS = line.split(":")[1].strip()
    if "key_length" in line:
        KEY_LENGTH = line.split(":")[1].strip()
    if "using keys of length" in line:
        USING_KEY_OF_LENGTH = line.split(":")[1].strip()


def extract_benchmark_info(lines, benchmark_name):
    """
    Extract benchmark info

    :param lines: list of lines after BEGIN:
    :param benchmark_name: benchamrk name
    :return:
    """
    check = 0
    for temp_line in lines:
        if "hw_cpu_instructions" in temp_line:
            cpu_instructions = temp_line.split(":")[1].strip()
            check += 1
        if "hw_cpu_cycles" in temp_line:
            cpu_cycles = temp_line.split(":")[1].strip()
            check += 1
        if "hw_cache_misses" in temp_line:
            cache_misses = temp_line.split(":")[1].strip()
            check += 1
        if "hw_cache_references" in temp_line:
            cache_references = temp_line.split(":")[1].strip()
            check += 1
        if "items" in temp_line:
            items = temp_line.split(":")[1].strip()
        if "latency(ms)" in temp_line:
            latency = temp_line.split(":")[1].strip()
            check += 1
        if check == 5:
            benchmark_info = [
                benchmark_name,
                KEY_LENGTH,
                USING_KEY_OF_LENGTH,
                NUM_KEYS,
                items,
                latency,
                cpu_instructions,
                cpu_cycles,
                cache_misses,
                cache_references,
            ]
            BENCHMARK_TESTS.append(benchmark_info)
            break


def save_data_to_excel():
    """
    Saves data into csv file.

    :param data: all parsed countries with their airports
    :return:
    """
    # t = time.localtime()
    # curr_time = time.strftime("%H-%M-%S", t)
    with open(f'output/benchmarks.csv', 'w', encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(BENCHMARK_TESTS)
    print("Done! All data was saved")


if __name__ == '__main__':
    for filename in os.listdir('files'):
        read_file(filename)
    save_data_to_excel()

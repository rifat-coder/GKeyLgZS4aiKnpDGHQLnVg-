#
#   compare.py
#   🐲 DuplicheckPy script
#   System Design Task
#
#   Created by Rifat Murtazin on 8.01.2023.
#

import ast
import re
import os
import argparse

class FileReader:
    def __init__(self, file_path):
        # print(file_path)
        self.file_path = file_path

    def read(self):
        try:
            with open(self.file_path, 'r') as f:
                return f.read().strip()
        except FileNotFoundError:
            print('Error: the file was not found.')

class FileWriter:
    def __init__(self, file_path):
        self.file_path = file_path

    def write(self, data):
        try:
            with open(self.file_path, 'r+') as f:
                f.seek(0, os.SEEK_END)
                f.write(data)
        except OSError:
            print('Error: there was a problem writing to the file.')

class Duplicheck:

    def __init__(self, file1, file2):
        self.file1 = file1
        self.file2 = file2

    def levenstein(self, str_1, str_2):
        n, m = len(str_1), len(str_2)
        if n > m:
            str_1, str_2 = str_2, str_1
            n, m = m, n

        current_row = range(n + 1)
        for i in range(1, m + 1):
            previous_row, current_row = current_row, [i] + [0] * n
            for j in range(1, n + 1):
                add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
                if str_1[j - 1] != str_2[i - 1]:
                    change += 1
                current_row[j] = min(add, delete, change)

        return current_row[n]



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compare two files.')
    parser.add_argument('input_files', help='the list of input files')
    parser.add_argument('output_file', help='the output file')
    args = parser.parse_args()

    try:
        with open(args.input_files, 'r') as input_files:
            input_files = list(map(lambda s: s.strip().split(), input_files.readlines()))
            # print(input_files)

    except FileNotFoundError:
        print('Error: the file was not found.')

    else:
        for i in range(len(input_files)):
            reader1 = FileReader(input_files[i][0])
            file1 = reader1.read()
            reader2 = FileReader(input_files[i][1])
            file2 = reader2.read()

            compare = Duplicheck(file1, file2)
            ratio = 1 - compare.levenstein(compare.file1, compare.file2) / max(len(file1), len(file2))

            writer = FileWriter(args.output_file)
            writer.write(str(ratio) + '\n')
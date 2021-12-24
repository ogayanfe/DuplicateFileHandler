import os
import sys
import hashlib
try:
    directory = sys.argv[1]
except IndexError:
    print('Directory is not specified')
    quit()


class FileHandler:
    def __init__(self, file_type, option):
        self.file_type = file_type
        self.option = option
        self.all_files = {}
        self.hash_value_pairs = {}
        self.hash_values = []
        self.duplicate_list = []

    def scan_files(self):
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(self.file_type):
                    path = os.path.join(root, file)
                    size = os.path.getsize(path)
                    if size in self.all_files:
                        self.all_files[size].append(path)
                    else:
                        self.all_files[size] = [path]

    def print_result(self):
        if self.option == 1:
            sorted_keys = sorted(self.all_files, reverse=True)
        else:
            sorted_keys = sorted(self.all_files)
        for key in sorted_keys:
            print()
            print(key, "bytes")
            value = self.all_files[key]
            for v in value:
                print(v)

    def check_file_hash(self):
        for size in self.all_files:
            self.hash_value_pairs[size] = {}
            for file in self.all_files[size]:
                md5 = hashlib.md5()
                with open(file, 'rb') as _file:
                    content = _file.read()
                    md5.update(content)
                    _hash = md5.hexdigest()
                    if _hash in self.hash_value_pairs[size].keys():
                        self.hash_value_pairs[size][_hash].append(file)
                    else:
                        self.hash_value_pairs[size][_hash] = [file]

    def print_duplicate_hash(self):
        index = 0
        if self.option == 1:
            descending = True
        else:
            descending = False
        for size in sorted(self.hash_value_pairs, reverse=descending):
            print()
            print(size, 'bytes')
            for hash_values in self.hash_value_pairs[size]:
                if len(self.hash_value_pairs[size][hash_values]) > 1:
                    print('Hash:', hash_values)
                    for file in self.hash_value_pairs[size][hash_values]:
                        index += 1
                        print(f'{index}. {file}')
                        self.duplicate_list.append((size, index, file))

    def delete_duplicates(self):
        run = True
        values_to_delete = []
        while True and run is True:
            try:
                indexes = [lst[1] for lst in self.duplicate_list]
                values_to_delete = [int(x) for x in input('Enter file numbers to delete:\n').split()]
                if len(values_to_delete) > 0:
                    for x in values_to_delete:
                        if x not in indexes:
                            print('Wrong format')
                        else:
                            run = False
                    else:
                        break
                else:
                    print('Wrong format')
            except ValueError:
                print('Wrong format')
        cleared_space = 0
        for size, index, file in self.duplicate_list:
            if index in values_to_delete:
                cleared_space += size
                os.remove(file)
        print(f'\nTotal freed up space: {cleared_space}')

    def main(self):
        self.scan_files()
        self.print_result()
        print()
        check_for_duplicates = input('Check for duplicates?\n')
        while True:
            if check_for_duplicates == 'yes':
                self.check_file_hash()
                self.print_duplicate_hash()
                break
            elif check_for_duplicates == 'no':
                quit()
            else:
                print('Wrong option')

        while True:
            prompt = input('\nDelete files?\n')
            if prompt == 'yes':
                self.delete_duplicates()
                break
            elif prompt == 'no':
                break
            else:
                print('Wrong option')


def call_class():
    file_format = input("\nEnter file format:\n")
    print("Size sorting options:\n1. Descending\n2. Ascending")
    while True:
        sort = input("\nEnter a sorting option:\n")
        if sort in ['1', '2']:
            break
        else:
            print('Wrong option')
    summoned = FileHandler(file_format, int(sort))
    summoned.main()


call_class()

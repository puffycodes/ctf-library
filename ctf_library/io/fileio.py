# file: fileio.py

import os

class FileIO:

    @staticmethod
    def read_text_data(filename, dirname='.', encoding='utf-8'):
        full_filename = os.path.join(dirname, filename)
        with open(full_filename, 'r', encoding=encoding) as fd:
            lines = fd.readlines()
        return lines

    @staticmethod
    def read_binary_data(filename, dirname='.'):
        full_filename = os.path.join(dirname, filename)
        with open(full_filename, 'rb') as fd:
            data = fd.read()
        return data

    @staticmethod
    def write_binary_data(data, filename, dirname='.'):
        full_filename = os.path.join(dirname, filename)
        with open(full_filename, 'wb') as fd:
            fd.write(data)
        return

# --- end of file --- #

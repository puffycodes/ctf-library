# file: file_format.py

# Base class for FileFormat class.
# Contains some common functions.

import argparse

class FileFormat:

    # Dummy, default parse function
    @staticmethod
    def parse(data, offset=0, max_length=-1):
        print(f'=== default parse function:')
        print(f'      please call the parse function of subclass.')
        return

    @staticmethod
    def compute_end_position(data, offset=0, max_length=-1):
        end_of_data_pos = len(data)
        if max_length > 0:
            end_of_data_pos = min(end_of_data_pos, offset + max_length)
        return end_of_data_pos

    @staticmethod
    def error_insufficient_data(data, length, pos=0):
        remaining_data = data[pos:]
        remaining_data_length = len(remaining_data)
        print(f'  *** insufficent data at {pos} (0x{pos:x}). need {length} (0x{length:x})')
        print(f'  *** remaining data: {remaining_data}')
        print(f'  *** remaining data length: {remaining_data_length} (0x{remaining_data_length:x})')
        return pos + remaining_data_length
    
    @staticmethod
    def main(params):
        prog = params.get('prog', 'parse_file')
        description = params.get('description',
                                 'Parse and list content of files.')
        file_arg_name = params.get('file_arg_name', 'file')
        file_arg_name_help = params.get(
            'file_arg_name_help', 'file to parse'
        )
        file_parse_function = params.get('file_parse_function', FileFormat.parse)

        parser = argparse.ArgumentParser(
            prog=prog, description=description
        )
        parser.add_argument(file_arg_name, nargs='+',
                            help=file_arg_name_help)
        args = parser.parse_args()

        args_dict = vars(args)
        files = args_dict[file_arg_name]
        for file in files:
            print(f'=== parsing file "{file}":')
            with open(file, 'rb') as fd:
                data = fd.read()
                file_parse_function(data)

        return

# --- end of file --- #

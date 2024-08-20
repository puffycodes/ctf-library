# file: file_format.py

# Base class for FileFormat class.
# Contains some common functions.

import sys
import argparse

from common_util.hexdump import HexDump

class FileFormat:

    class BlockInfo:

        def __init__(self, start=0, end=0):
            self.start = start
            self.end = end
            self.compute_length()
            return
        
        def set_start(self, start):
            self.start = start
            self.compute_length()
            return
        
        def set_end(self, end):
            self.end = end
            self.compute_length()
            return
        
        def compute_length(self):
            self.length = self.end - self.start
            return

        def show_block_info(self, tag='data', indent=0, fout=sys.stdout):
            indentation = ' ' * indent
            block_info_str = self.format_block_info()
            print(
                f'{indentation}- {tag}: {block_info_str}',
                file=fout
            )
            return
        
        def format_block_info(self):
            result = f'start: {self.start} (0x{self.start:x});' \
                f' end: {self.end} (0x{self.end:x});' \
                f' length: {self.length} (0x{self.length:x})'
            return result
    
    # --- Common functions

    @staticmethod
    def compute_end_position(data, offset=0, max_length=-1):
        end_of_data_pos = len(data)
        if max_length > 0:
            end_of_data_pos = min(end_of_data_pos, offset + max_length)
        return end_of_data_pos

    @staticmethod
    def error_insufficient_data(data, length, pos=0, fout=sys.stdout):
        remaining_data = data[pos:]
        remaining_data_length = len(remaining_data)
        print(f'  *** insufficent data at {pos} (0x{pos:x}). need {length} (0x{length:x})', file=fout)
        print(f'  *** remaining data: {remaining_data}', file=fout)
        print(
            f'  *** remaining data length: {remaining_data_length} (0x{remaining_data_length:x})',
            file=fout
        )
        return pos + remaining_data_length
    
    # --- Functions related to main()
    
    # Dummy, default parse function
    @staticmethod
    def parse(data, offset=0, max_length=-1):
        print(f'=== default parse function:')
        print(f'      please provide the parse function of subclass.')
        return offset

    @staticmethod
    def main(params, debug=False):
        prog = params.get('prog', 'parse_file')
        description = params.get(
            'description', 'Parse and list content of files.'
        )
        file_arg_name = params.get('file_arg_name', 'file')
        file_arg_name_help = params.get(
            'file_arg_name_help', 'file to parse'
        )
        file_actions = params.get('file_actions', {})
        if len(file_actions) <= 0:
            file_actions['parse'] = FileFormat.parse
        if debug:
            for curr_action in file_actions.keys():
                print(f'{curr_action}: {file_actions[curr_action]}')

        parser = argparse.ArgumentParser(
            prog=prog, description=description
        )
        parser.add_argument('action', choices=file_actions.keys(),
                            help='action to perform on file')
        parser.add_argument(file_arg_name, nargs='+',
                            help=file_arg_name_help)
        args = parser.parse_args()

        args_dict = vars(args)
        files = args_dict.get(file_arg_name, [])
        curr_action = args.action
        for file in files:
            print(f'=== parsing file "{file}" with action "{curr_action}":')
            with open(file, 'rb') as fd:
                data = fd.read()
            if curr_action in file_actions:
                result = file_actions[curr_action](data)
                if type(result) == int:
                    end_pos = result
                    print(f'data length: {len(data)}; parsing ends at {end_pos}')
                elif type(result) == bytes:
                    result_length = len(result)
                    result_hexdump = HexDump.hexdump_start_and_end(result)
                    print(f'result length: {result_length}')
                    HexDump.print_hexdump(result_hexdump)
                else:
                    print(f'result: {result}')
            else:
                print(f'unknown action {curr_action}')
            print()

        return

# --- end of file --- #

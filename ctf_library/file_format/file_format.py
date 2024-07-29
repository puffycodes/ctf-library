# file: file_format.py

# Base class for FileFormat class.
# Contains some common functions.

class FileFormat:

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

# --- end of file --- #

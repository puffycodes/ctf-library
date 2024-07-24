# file: file_format.py

# Base class for FileFormat class.
# Contains some common functions.

class FileFormat:

    @staticmethod
    def error_insufficient_data(data, length, pos=0):
        remaining_data = data[pos:]
        print(f'  *** insufficent data at {pos} ({pos:x}). need {length} ({length:x})')
        print(f'  *** remaining data: {remaining_data}')
        print(f'  *** remaining data length: {len(remaining_data)}')
        return pos + length

# --- end of file --- #

# file: pngfile_format.py

from common_util.bytes_util import BytesUtility
from ctf_library.file_format.file_format import FileFormat

# Reference:
# - https://en.wikipedia.org/wiki/PNG
# Free Sample PNG Files:
# - https://file-examples.com/index.php/sample-images-download/sample-png-download/
# - https://sample-videos.com/download-sample-png-image.php

class PNGFileFormat(FileFormat):

    PNGHeader = b'\x89\x50\x4e\x47\x0d\x0a\x1a\x0a'
    PNGHeaderLength = len(PNGHeader)

    @staticmethod
    def parse(data, offset=0, max_length=-1, with_header=True):
        # data_length = len(data) - offset
        # print(f'data length: {data_length}')

        end_of_data_pos = len(data)
        if max_length > 0:
            end_of_data_pos = min(end_of_data_pos, offset + max_length)

        data_length = end_of_data_pos - offset
        print(f'data length: {data_length}')

        curr_pos = offset

        if with_header:
            header_data = BytesUtility.extract_bytes(
                data, 0, PNGFileFormat.PNGHeaderLength, curr_pos
            )
            print(f'offset: {curr_pos}; header: {header_data}')
            curr_pos += PNGFileFormat.PNGHeaderLength

            if header_data != PNGFileFormat.PNGHeader:
                return curr_pos

        while curr_pos < end_of_data_pos:
            chunk_length = BytesUtility.extract_integer(data, 0, 4, pos=curr_pos, endian='big')
            chunk_type = BytesUtility.extract_bytes(data, 4, 4, pos=curr_pos)
            chunk_data = BytesUtility.extract_bytes(data, 8, chunk_length, pos=curr_pos)
            chunk_crc = BytesUtility.extract_bytes(data, 8 + chunk_length, 4, pos=curr_pos)
            print(f'offset: {curr_pos}; type: {chunk_type}; length: {chunk_length}; crc: {chunk_crc}')
            curr_pos += 12 + chunk_length

            if chunk_type == b'IEND':
                break

        return curr_pos
    
    @staticmethod
    def extract_png_data(data, offset=0, max_length=-1, with_header=True):
        end_of_data_pos = len(data)
        if max_length > 0:
            end_of_data_pos = min(end_of_data_pos, offset + max_length)

        extracted_data = b''
        curr_pos = offset
        if with_header:
            curr_pos += PNGFileFormat.PNGHeaderLength

        while curr_pos < end_of_data_pos:
            chunk_length = BytesUtility.extract_integer(data, 0, 4, pos=curr_pos, endian='big')
            chunk_type = BytesUtility.extract_bytes(data, 4, 4, pos=curr_pos)
            if chunk_type == b'IDAT':
                chunk_data = BytesUtility.extract_bytes(data, 8, chunk_length, pos=curr_pos)
                extracted_data += chunk_data
            curr_pos += 12 + chunk_length

            if chunk_type == b'IEND':
                break

        return extracted_data

# --- end of file --- #

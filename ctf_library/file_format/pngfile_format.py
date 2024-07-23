# file: pngfile_format.py

from common_util.bytes_util import BytesUtility

# Reference:
# - https://en.wikipedia.org/wiki/PNG
# Free Sample PNG Files:
# - https://file-examples.com/index.php/sample-images-download/sample-png-download/
# - https://sample-videos.com/download-sample-png-image.php

class PNGFileFormat:

    PNGHeader = b'\x89\x50\x4e\x47\x0d\x0a\x1a\x0a'

    @staticmethod
    def parse(data, offset=0, max_length=-1, with_header=True):
        data_length = len(data) - offset
        print(f'data length: {data_length}')

        curr_pos = offset

        if with_header:
            header_data = BytesUtility.extract_bytes(data, 0, 8, curr_pos)
            print(f'offset: {curr_pos}; header: {header_data}')
            curr_pos += 8

            if header_data != PNGFileFormat.PNGHeader:
                return curr_pos

        while curr_pos < len(data):
            chunk_length = BytesUtility.extract_integer(data, 0, 4, pos=curr_pos, endian='big')
            chunk_type = BytesUtility.extract_bytes(data, 4, 4, pos=curr_pos)
            chunk_data = BytesUtility.extract_bytes(data, 8, chunk_length, pos=curr_pos)
            chunk_crc = BytesUtility.extract_bytes(data, 8 + chunk_length, 4, pos=curr_pos)
            print(f'offset: {curr_pos}; type: {chunk_type}; length: {chunk_length}; crc: {chunk_crc}')
            curr_pos += 12 + chunk_length

            if chunk_type == b'IEND':
                break

        return curr_pos

# --- end of file --- #

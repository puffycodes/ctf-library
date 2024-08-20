# file: pngfile_format.py

from common_util.bytes_util import BytesUtility
from common_util.hexdump import HexDump
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
        end_of_data_pos = PNGFileFormat.compute_end_position(
            data, offset=offset, max_length=max_length
        )

        data_length = end_of_data_pos - offset
        print(f'data length: {data_length}')

        curr_pos = offset

        if with_header:
            header_data = BytesUtility.extract_bytes(
                data, 0, PNGFileFormat.PNGHeaderLength, curr_pos
            )
            header_data_hexdump = HexDump.to_hex(header_data, sep=' ')
            header_data_text = HexDump.to_text(header_data)
            print(f'offset: {curr_pos}; header: {header_data_hexdump} "{header_data_text}"')
            curr_pos += PNGFileFormat.PNGHeaderLength

            if header_data != PNGFileFormat.PNGHeader:
                return curr_pos

        while curr_pos < end_of_data_pos:
            chunk_length = BytesUtility.extract_integer(data, 0, 4, pos=curr_pos, endian='big')
            chunk_type = BytesUtility.extract_bytes(data, 4, 4, pos=curr_pos)
            chunk_data = BytesUtility.extract_bytes(data, 8, chunk_length, pos=curr_pos)
            chunk_crc = BytesUtility.extract_bytes(data, 8 + chunk_length, 4, pos=curr_pos)
            chunk_crc_hexdump = HexDump.to_hex(chunk_crc, sep='')
            print(f'offset: {curr_pos}; type: {chunk_type}; length: {chunk_length}; crc: {chunk_crc_hexdump}')
            curr_pos += 12 + chunk_length

            if chunk_type == b'IEND':
                break

        return curr_pos
    
    @staticmethod
    def extract_png_data(data, offset=0, max_length=-1, with_header=True):
        end_of_data_pos = PNGFileFormat.compute_end_position(
            data, offset=offset, max_length=max_length
        )

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

    @staticmethod
    def main():
        params = {
            'prog': 'parse_pngfile',
            'description': 'Parse and list content of pngfiles.',
            'file_arg_name': 'pngfile',
            'file_arg_name_help': 'png file to parse',
            'file_actions': {
                'parse': PNGFileFormat.parse,
                'extract': PNGFileFormat.extract_png_data,
            }
        }
        FileFormat.main(params)
        return
    
if __name__ == '__main__':
    PNGFileFormat.main()
    
# --- end of file --- #

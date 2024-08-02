# file: gzipfile_format.py

# Reference:
# - https://en.wikipedia.org/wiki/Gzip
# - https://datatracker.ietf.org/doc/html/rfc1952.html
# Free Sample Gzip Files:
# - https://getsamplefiles.com/sample-archive-files/gzip

from common_util.bytes_util import BytesUtility
from ctf_library.file_format.file_format import FileFormat

class GzipFileFormat(FileFormat):

    flag_ftext = 0x01
    flag_fhcrc = 0x02
    flag_fextra = 0x04
    flag_fname = 0x08
    flag_fcomment = 0x10

    @staticmethod
    def parse(data, offset=0, max_length=-1):
        end_of_data_pos = GzipFileFormat.compute_end_position(
            data, offset=offset, max_length=max_length
        )

        data_length = end_of_data_pos - offset
        print(f'data length: {data_length}')

        curr_pos = offset

        print(f'header:')
        header_length_fixed = 10
        if end_of_data_pos >= curr_pos + header_length_fixed:
            magic_number = BytesUtility.extract_bytes(data, 0, 2, pos=curr_pos)
            compression_method = BytesUtility.extract_integer(data, 2, 1, pos=curr_pos)
            header_flags = BytesUtility.extract_integer(data, 3, 1, pos=curr_pos)
            timestamp = BytesUtility.extract_integer(data, 4, 4, pos=curr_pos)
            compression_flags = BytesUtility.extract_integer(data, 8, 1, pos=curr_pos)
            operating_system_id = BytesUtility.extract_integer(data, 9, 1, pos=curr_pos)

            print(f'  magic number: {magic_number}')
            print(f'  compression method: {compression_method}')
            print(f'  header flags: {header_flags:08b}')
            print(f'  timestamp:  {timestamp}')
            print(f'  compression flags: {compression_flags}')
            print(f'  operating system id: {operating_system_id}')
        else:
            return GzipFileFormat.error_insufficient_data(data, header_length_fixed, pos=curr_pos)

        curr_pos += header_length_fixed

        print(f'  remaining data: {data[curr_pos:curr_pos+40]}')

        print(f'optional fields:')

        if header_flags & GzipFileFormat.flag_fextra != 0:
            extra_field_length = BytesUtility.extract_integer(data, 0, 2, pos=curr_pos)
            extra_field_data = BytesUtility.extract_bytes(data, 2, extra_field_length, pos=curr_pos)
            print(f'  extra field length: {extra_field_length}')
            print(f'  extra field data: {extra_field_data}')
            curr_pos += 2 + extra_field_length
        else:
            print(f'  no extra field')

        #print(f'  remaining data: {data[curr_pos:curr_pos+40]}')

        if header_flags & GzipFileFormat.flag_fname != 0:
            filename_char_count = 0
            while data[curr_pos+filename_char_count] != 0x00:
               filename_char_count += 1
            # filename = data[curr_pos:curr_pos+filename_char_count]
            filename = BytesUtility.extract_bytes(data, 0, filename_char_count, pos=curr_pos)
            print(f'  filename: {filename} ({filename_char_count} characters)')
            curr_pos += filename_char_count + 1
        else:
            print(f'  no filename')

        #print(f'  remaining data: {data[curr_pos:curr_pos+40]}')

        if header_flags & GzipFileFormat.flag_fcomment != 0:
            comment_char_count = 0
            while data[curr_pos+comment_char_count] != 0x00:
               comment_char_count += 1
            # comment = data[curr_pos:curr_pos+comment_char_count]
            comment = BytesUtility.extract_bytes(data, 0, comment_char_count, pos=curr_pos)
            print(f'  comment: {comment} ({comment_char_count} characters)')
            curr_pos += comment_char_count + 1
        else:
            print(f'  no comment')

        #print(f'  remaining data: {data[curr_pos:curr_pos+40]}')

        if header_flags & GzipFileFormat.flag_fhcrc != 0:
            crc16 = BytesUtility.extract_bytes(data, 0, 2, pos=curr_pos)
            print(f'  crc16 (header): {crc16}')
            curr_pos += 2
        else:
            print(f'  no crc')

        print(f'compressed data:')

        remaining_data_length = end_of_data_pos - curr_pos
        trailer_length_fixed = 8

        print(f'  compress block location: {curr_pos}')

        print(f'  remaining data length: {remaining_data_length}')
        print(f'  remaining data: {data[curr_pos:curr_pos+40]}')
        print(f'                  {data[-20:]}')

        if remaining_data_length >= trailer_length_fixed:
            crc32_pos = end_of_data_pos - 8
            isize_pos = end_of_data_pos - 4
            crc32 = BytesUtility.extract_bytes(data, 0, 4, pos=crc32_pos)
            isize = BytesUtility.extract_integer(data, 0, 4, pos=isize_pos)
            compressed_block_length = crc32_pos - curr_pos
            compressed_block = BytesUtility.extract_bytes(
                data, curr_pos, compressed_block_length
            )
            print(f'  crc32 location: {crc32_pos}')
            print(f'  isize location: {isize_pos}')
            print(f'  crc32 (uncompressed data): {crc32}')
            print(f'  isize (input size): {isize}')
            print(f'  compressed block data: {compressed_block[:40]}')
            print(f'                         {compressed_block[-20:]}')
            print(f'    - length: {compressed_block_length}')
            # TODO: need to update curr_pos here
            curr_pos = end_of_data_pos # TODO: Temporary do this. Need to check.
        else:
            return GzipFileFormat.error_insufficient_data(data, trailer_length_fixed, pos=curr_pos)

        return curr_pos

    @staticmethod
    def main():
        params = {
            'prog': 'parse_gzipfile',
            'description': 'Parse and list content of gzipfiles.',
            'file_arg_name': 'gzipfile',
            'file_arg_name_help': 'gzipfile to parse',
            'file_parse_function': GzipFileFormat.parse,
        }
        FileFormat.main(params)
        return
    
if __name__ == '__main__':
    GzipFileFormat.main()
    
# --- end of file --- #

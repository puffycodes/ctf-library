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
        # data_length = len(data)
        # curr_pos = pos

        # end_of_data_pos = len(data)
        # if max_length > 0:
        #     end_of_data_pos = min(end_of_data_pos, offset + max_length)
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
            print(f'  header flags: {header_flags:b}')
            print(f'  timestamp:  {timestamp}')
            print(f'  compression flags: {compression_flags}')
            print(f'  operating system id: {operating_system_id}')
        else:
            return GzipFileFormat.error_insufficient_data(data, header_length_fixed, pos=curr_pos)

        curr_pos += header_length_fixed

        print(f'  remaining data: {data[curr_pos:curr_pos+40]}')

        if header_flags & GzipFileFormat.flag_fextra != 0:
            extra_field_length = BytesUtility.extract_integer(data, 0, 2, pos=curr_pos)
            extra_field_data = BytesUtility.extract_bytes(data, 2, extra_field_length, pos=curr_pos)
            print(f'  extra field length: {extra_field_length}')
            print(f'  extra field data: {extra_field_data}')
            curr_pos += 2 + extra_field_length
        else:
            print('  no extra field')

        #print(f'  remaining data: {data[curr_pos:curr_pos+40]}')

        if header_flags & GzipFileFormat.flag_fname != 0:
            filename_char_count = 0
            while data[curr_pos+filename_char_count] != 0x00:
               filename_char_count += 1
            filename = data[curr_pos:curr_pos+filename_char_count]
            print(f'  filename: {filename} ({filename_char_count} characters)')
            curr_pos += filename_char_count + 1
        else:
            print('  no filename')

        #print(f'  remaining data: {data[curr_pos:curr_pos+40]}')

        if header_flags & GzipFileFormat.flag_fcomment != 0:
            comment_char_count = 0
            while data[curr_pos+comment_char_count] != 0x00:
               comment_char_count += 1
            comment = data[curr_pos:curr_pos+comment_char_count]
            print(f'  comment: {comment} ({comment_char_count} characters)')
            curr_pos += comment_char_count + 1
        else:
            print('  no comment')

        #print(f'  remaining data: {data[curr_pos:curr_pos+40]}')

        if header_flags & GzipFileFormat.flag_fhcrc != 0:
            crc16 = BytesUtility.extract_bytes(data, 0, 2, pos=curr_pos)
            print(f'  crc16 (header): {crc16}')
            curr_pos += 2
        else:
            print('  no crc')

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
            print(f'  crc32 location: {crc32_pos}')
            print(f'  isize location: {isize_pos}')
            print(f'  crc32 (compressed block): {crc32}')
            print(f'  isize: {isize}')
            # TODO: need to update curr_pos here
            curr_pos = end_of_data_pos # TODO: Temporary do this. Need to check.
        else:
            return GzipFileFormat.error_insufficient_data(data, trailer_length_fixed, pos=curr_pos)

        return curr_pos

# --- end of file --- #

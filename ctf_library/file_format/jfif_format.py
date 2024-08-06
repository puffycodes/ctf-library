# file: jfif_format.py

from common_util.bytes_util import BytesUtility
from ctf_library.file_format.file_format import FileFormat

class JFIFFileFormat(FileFormat):

    MarkerSOI = b'\xff\xd8'
    MarkerAPP0 = b'\xff\xe0'
    MarkerSOS = b'\xff\xda'
    MarkerEOI = b'\xff\xd9'

    @staticmethod
    def parse(data, offset=0, max_length=-1):
        end_of_data_pos = JFIFFileFormat.compute_end_position(
            data, offset=offset, max_length=max_length
        )

        data_length = end_of_data_pos - offset
        print(f'data length: {data_length}')
        print()

        curr_pos = offset

        while curr_pos < end_of_data_pos:
            marker = BytesUtility.extract_bytes(data, 0, 2, pos=curr_pos)
            if marker == JFIFFileFormat.MarkerSOI:
                curr_pos = JFIFFileFormat.parse_soi_marker_segment(
                    data, pos=curr_pos, end_pos=end_of_data_pos
                )
            elif marker == JFIFFileFormat.MarkerAPP0:
                curr_pos = JFIFFileFormat.parse_app0_marker_segment(
                    data, pos=curr_pos, end_pos=end_of_data_pos
                )
            else:
                curr_pos = JFIFFileFormat.parse_unknown_marker_segment(
                    data, pos=curr_pos, end_pos=end_of_data_pos
                )
                print(f'parsing ended at location {curr_pos}')
                break
            print()

        return curr_pos

    @staticmethod
    def parse_soi_marker_segment(data, pos=0, end_pos=-1):
        if end_pos < 0:
            end_pos = len(data)
        curr_pos = pos

        header_length_fixed = 2

        if end_pos >= curr_pos + header_length_fixed:
            marker = BytesUtility.extract_bytes(data, 0, 2, pos=curr_pos)
            print(f'SOI Marker Segment:')
            print(f'  - marker: {marker}')
        else:
            return JFIFFileFormat.error_insufficient_data(data, header_length_fixed, pos=curr_pos)

        curr_pos += header_length_fixed

        return curr_pos
    
    @staticmethod
    def parse_app0_marker_segment(data, pos=0, end_pos=-1):
        if end_pos < 0:
            end_pos = len(data)
        curr_pos = pos

        header_length_fixed = 10

        if end_pos >= curr_pos + header_length_fixed:
            marker = BytesUtility.extract_bytes(data, 0, 2, pos=curr_pos)
            print(f'APP0 Marker Segment:')
            print(f'  - marker: {marker}')
            length = BytesUtility.extract_integer(data, 2, 2, pos=curr_pos, endian='big')
            identifier = BytesUtility.extract_bytes(data, 4, 5, pos=curr_pos)
            thumbnail_format = BytesUtility.extract_integer(
                data, 9, 1, pos=curr_pos, endian='big'
            )
            thumbnail_data_length = length - header_length_fixed + 2
            print(f'  - segment length: {length}')
            print(f'  - identifier: {identifier}')
            print(f'  - thumbnail format: {thumbnail_format}')
        else:
            return JFIFFileFormat.error_insufficient_data(data, header_length_fixed, pos=curr_pos)

        curr_pos += header_length_fixed

        if end_pos >= curr_pos + thumbnail_data_length:
            thumbnail_data = BytesUtility.extract_bytes(
                data, 0, thumbnail_data_length, pos=curr_pos
            )
            print(f'  - thumbnail data: {thumbnail_data[:50]}')
            print(f'                    {thumbnail_data[-20:]}')
        else:
            return JFIFFileFormat.error_insufficient_data(data, thumbnail_data_length, pos=curr_pos)

        curr_pos += thumbnail_data_length

        return curr_pos
    
    @staticmethod
    def parse_unknown_marker_segment(data, pos=0, end_pos=-1):
        if end_pos < 0:
            end_pos = len(data)
        curr_pos = pos

        header_length_fixed = 2

        if end_pos >= curr_pos + header_length_fixed:
            marker = BytesUtility.extract_bytes(data, 0, 2, pos=curr_pos)
            print(f'Unknown Marker Segment:')
            print(f'  - marker: {marker}')
        else:
            return JFIFFileFormat.error_insufficient_data(data, header_length_fixed, pos=curr_pos)

        curr_pos += header_length_fixed

        next_marker_pos = curr_pos
        while end_pos > next_marker_pos and data[next_marker_pos:next_marker_pos+1] != b'\xff':
            next_marker_pos += 1
        unknown_data_length = next_marker_pos - curr_pos
        unknown_data = BytesUtility.extract_bytes(
            data, 0, unknown_data_length, pos=curr_pos
        )
        print(f'  - data: {unknown_data[:50]}')
        print(f'          {unknown_data[-20:]}')
        print(f'      - length: {unknown_data_length}')

        curr_pos = next_marker_pos

        return curr_pos
    
    @staticmethod
    def main():
        params = {
            'prog': 'parse_jfiffile',
            'description': 'Parse and list content of jfiffiles.',
            'file_arg_name': 'jfiffile',
            'file_arg_name_help': 'jfiffile to parse',
            'file_parse_function': JFIFFileFormat.parse,
        }
        FileFormat.main(params)
        return
    
if __name__ == '__main__':
    JFIFFileFormat.main()
    
# --- end of file --- #

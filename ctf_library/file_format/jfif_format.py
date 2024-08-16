# file: jfif_format.py

import sys
from common_util.bytes_util import BytesUtility
from common_util.hexdump import HexDump
from ctf_library.file_format.file_format import FileFormat

class JFIFFileFormat(FileFormat):

    MarkerSOI = b'\xff\xd8'
    MarkerEOI = b'\xff\xd9'
    MarkerSOS = b'\xff\xda'
    Marker0xDB = b'\xff\xdb'

    Marker0xC0 = b'\xff\xc0'
    Marker0xC2 = b'\xff\xc2'
    Marker0xC4 = b'\xff\xc4'

    MarkerAPP0 = b'\xff\xe0'

    Marker0xFE = b'\xff\xfe'

    ValidMarkers = [
        MarkerSOI, MarkerEOI, MarkerSOS, Marker0xDB,
        Marker0xC0, Marker0xC4, MarkerAPP0,
    ]
    MarkersWithTwoBytesLength = [
        Marker0xDB, Marker0xC0, Marker0xC2, Marker0xC4, Marker0xFE,
    ]

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
                curr_pos = JFIFFileFormat.parse_soi_segment(
                    data, pos=curr_pos, end_pos=end_of_data_pos
                )
            elif marker == JFIFFileFormat.MarkerEOI:
                curr_pos = JFIFFileFormat.parse_eoi_segment(
                    data, pos=curr_pos, end_pos=end_of_data_pos
                )
            elif marker == JFIFFileFormat.MarkerAPP0:
                curr_pos = JFIFFileFormat.parse_app0_segment(
                    data, pos=curr_pos, end_pos=end_of_data_pos
                )
            elif marker == JFIFFileFormat.MarkerSOS:
                curr_pos = JFIFFileFormat.parse_sos_segment(
                    data, pos=curr_pos, end_pos=end_of_data_pos
                )
            elif marker in JFIFFileFormat.MarkersWithTwoBytesLength:
                curr_pos = JFIFFileFormat.parse_segment_with_two_bytes_length(
                    data, pos=curr_pos, end_pos=end_of_data_pos
                )
            else:
                curr_pos = JFIFFileFormat.parse_unknown_segment(
                    data, pos=curr_pos, end_pos=end_of_data_pos
                )
            print()

        return curr_pos

    @staticmethod
    def parse_soi_segment(data, pos=0, end_pos=-1):
        if end_pos < 0:
            end_pos = len(data)
        curr_pos = pos

        header_length_fixed = 2

        if end_pos >= curr_pos + header_length_fixed:
            marker = BytesUtility.extract_bytes(data, 0, 2, pos=curr_pos)
            marker_pos = curr_pos
            print(f'Start of Image (SOI) Segment:')
            print(f'  - marker: {marker} at {marker_pos}')
        else:
            return JFIFFileFormat.error_insufficient_data(data, header_length_fixed, pos=curr_pos)

        curr_pos += header_length_fixed

        return curr_pos
    
    @staticmethod
    def parse_eoi_segment(data, pos=0, end_pos=-1):
        if end_pos < 0:
            end_pos = len(data)
        curr_pos = pos

        header_length_fixed = 2

        if end_pos >= curr_pos + header_length_fixed:
            marker = BytesUtility.extract_bytes(data, 0, 2, pos=curr_pos)
            marker_pos = curr_pos
            print(f'End of Image (EOI) Segment:')
            print(f'  - marker: {marker} at {marker_pos}')
        else:
            return JFIFFileFormat.error_insufficient_data(data, header_length_fixed, pos=curr_pos)

        curr_pos += header_length_fixed

        return curr_pos
    
    @staticmethod
    def parse_app0_segment(data, pos=0, end_pos=-1):
        if end_pos < 0:
            end_pos = len(data)
        curr_pos = pos

        common_header_length_fixed = 9

        if end_pos >= curr_pos + common_header_length_fixed:
            marker = BytesUtility.extract_bytes(data, 0, 2, pos=curr_pos)
            marker_pos = curr_pos
            print(f'APP0 Segment:')
            print(f'  - marker: {marker} at {marker_pos}')

            length = BytesUtility.extract_integer(
                data, 2, 2, pos=curr_pos, endian='big'
            )
            identifier = BytesUtility.extract_bytes(data, 4, 5, pos=curr_pos)
            print(f'  - segment length: {length}')
            print(f'  - identifier: {identifier}')
        else:
            return JFIFFileFormat.error_insufficient_data(
                data, common_header_length_fixed, pos=curr_pos
            )

        # JFIF-APP0 Segment
        if identifier == b'JFIF\x00':
            print(f'  - JFIF-APP0 Segment')

            header_length_fixed = common_header_length_fixed + 9
            if end_pos < curr_pos + header_length_fixed:
                return JFIFFileFormat.error_insufficient_data(
                    data, header_length_fixed, pos=curr_pos
                )

            version_major = BytesUtility.extract_integer(
                data, 9, 1, pos=curr_pos, endian='big'
            )
            version_minor = BytesUtility.extract_integer(
                data, 10, 1, pos=curr_pos, endian='big'
            )
            units = BytesUtility.extract_integer(
                data, 11, 1, pos=curr_pos, endian='big'
            )
            xdensity = BytesUtility.extract_integer(
                data, 12, 2, pos=curr_pos, endian='big'
            )
            ydensity = BytesUtility.extract_integer(
                data, 14, 2, pos=curr_pos, endian='big'
            )
            xthumbnail = BytesUtility.extract_integer(data, 16, 1)
            ythumbnail = BytesUtility.extract_integer(data, 17, 1)
            thumbnail_data_length = length - header_length_fixed + 2

            print(f'  - version: {version_major}.{version_minor}')
            print(f'  - units: {units}')
            print(f'  - density: x={xdensity} y={ydensity}')
            print(f'  - pixel count: {xthumbnail} x {ythumbnail}')
            print(f'  - thumbnail data length: {thumbnail_data_length}')

            curr_pos += header_length_fixed

            if end_pos >= curr_pos + thumbnail_data_length:
                if thumbnail_data_length > 0:
                    thumbnail_data = BytesUtility.extract_bytes(
                        data, 0, thumbnail_data_length, pos=curr_pos
                    )
                    print(f'  - thumbnail data: {thumbnail_data[:50]}')
                    print(f'                    {thumbnail_data[-20:]}')
                else:
                    thumbnail_data = b''
                    print(f'  - thumbnail data: none')
            else:
                return JFIFFileFormat.error_insufficient_data(data, thumbnail_data_length, pos=curr_pos)

            curr_pos += thumbnail_data_length

        # JFXX-APP0 Segment
        elif identifier == b'JFXX\x00':
            print(f'  - JFXX-APP0 Segment')

            header_length_fixed = common_header_length_fixed + 1
            if end_pos < curr_pos + header_length_fixed:
                return JFIFFileFormat.error_insufficient_data(
                    data, header_length_fixed, pos=curr_pos
                )

            extension_code = BytesUtility.extract_integer(
                data, 9, 1, pos=curr_pos, endian='big'
            )
            thumbnail_data_length = length - header_length_fixed + 2
            print(f'  - extension code: {extension_code}')
            print(f'  - thumbnail data length: {thumbnail_data_length}')

            curr_pos += header_length_fixed

            # TODO: thumbnail data

            curr_pos += thumbnail_data_length

        # Bombed
        else:
            print(f'  - Unknown APP0 Segment')
            header_length_fixed = common_header_length_fixed
            print(f'  - unknown identifier: {identifier}')
            curr_pos += header_length_fixed

        return curr_pos
    
    @staticmethod
    def parse_sos_segment(data, pos=0, end_pos=-1):
        if end_pos < 0:
            end_pos = len(data)
        curr_pos = pos

        header_length_fixed = 2

        if end_pos >= curr_pos + header_length_fixed:
            marker = BytesUtility.extract_bytes(data, 0, 2, pos=curr_pos)
            marker_pos = curr_pos
            print(f'Start of Scan (SOS) Segment:')
            print(f'  - marker: {marker} at {marker_pos}')
        else:
            return JFIFFileFormat.error_insufficient_data(data, header_length_fixed, pos=curr_pos)

        curr_pos += header_length_fixed

        next_marker_pos = JFIFFileFormat.find_next_marker(
            data, curr_pos, end_pos = end_pos
        )
        next_marker = BytesUtility.extract_bytes(data, 0, 2, pos=next_marker_pos)
        if next_marker == JFIFFileFormat.MarkerEOI:
            print(f'  - next marker is EOI {next_marker} at {next_marker_pos}')
        else:
            print(f'  - next marker is not EOI: found {next_marker} at {next_marker_pos}')

        compressed_image_data_length = next_marker_pos - curr_pos
        compressed_image_data = BytesUtility.extract_bytes(
            data, 0, compressed_image_data_length, pos=curr_pos
        )

        JFIFFileFormat.show_data(
            compressed_image_data,
            curr_pos, next_marker_pos, compressed_image_data_length, tag='compressed image data'
        )

        curr_pos = next_marker_pos

        return curr_pos
    
    @staticmethod
    def parse_segment_with_two_bytes_length(data, pos=0, end_pos=-1):
        if end_pos < 0:
            end_pos = len(data)
        curr_pos = pos

        header_length_fixed = 4

        if end_pos >= curr_pos + header_length_fixed:
            marker = BytesUtility.extract_bytes(data, 0, 2, pos=curr_pos)
            marker_pos = curr_pos
            length = BytesUtility.extract_integer(
                data, 2, 2, endian='big', pos=curr_pos
            )
            length_bytes = BytesUtility.extract_bytes(data, 2, 2, pos=curr_pos)
            data_length = length - header_length_fixed + 2
            print(f'Segment with length (2 bytes):')
            print(f'  - marker: {marker} at {marker_pos}')
            print(f'  - length: {length} (0x{length:04x}); {length_bytes}')
        else:
            return JFIFFileFormat.error_insufficient_data(data, header_length_fixed, pos=curr_pos)

        curr_pos += header_length_fixed

        if end_pos >= curr_pos + data_length:
            if data_length > 0:
                data = BytesUtility.extract_bytes(data, 0, data_length, pos=curr_pos)
                # print(f'  - data: {data[:50]}')
                # print(f'          {data[-20:]}')
                # print(f'      - start: {curr_pos}; end: {curr_pos+data_length}; length: {data_length}')
                JFIFFileFormat.show_data(
                    data, curr_pos, curr_pos + data_length, data_length, tag='data'
                )
            else:
                print(f'  - data: none')
        else:
            return JFIFFileFormat.error_insufficient_data(data, data_length, pos=curr_pos)

        curr_pos += data_length

        return curr_pos
    
    @staticmethod
    def parse_unknown_segment(data, pos=0, end_pos=-1):
        if end_pos < 0:
            end_pos = len(data)
        curr_pos = pos

        header_length_fixed = 2

        if end_pos >= curr_pos + header_length_fixed:
            marker = BytesUtility.extract_bytes(data, 0, 2, pos=curr_pos)
            marker_pos = curr_pos
            print(f'*** Unknown Marker Segment:')
            print(f'  - marker: {marker} at {marker_pos}')
        else:
            return JFIFFileFormat.error_insufficient_data(data, header_length_fixed, pos=curr_pos)

        curr_pos += header_length_fixed

        next_marker_pos = JFIFFileFormat.find_next_marker(
            data, curr_pos, end_pos = end_pos
        )

        unknown_data_length = next_marker_pos - curr_pos
        unknown_data = BytesUtility.extract_bytes(
            data, 0, unknown_data_length, pos=curr_pos
        )

        # print(f'  - data: {unknown_data[:50]}')
        # print(f'          {unknown_data[-20:]}')
        # print(f'      - start: {curr_pos}; end: {next_marker_pos}; length: {unknown_data_length}')
        JFIFFileFormat.show_data(
            unknown_data, curr_pos, next_marker_pos, unknown_data_length, tag='unknown data'
        )

        curr_pos = next_marker_pos

        return curr_pos
    
    @staticmethod
    def find_next_marker(data, start_pos, end_pos=-1):
        if end_pos <= 0:
            end_pos = len(data)

        next_marker_pos = start_pos

        # resync to the next b'\xff\xvv' which is in the list of valid markers
        while end_pos > next_marker_pos:
            if data[next_marker_pos:next_marker_pos+1] == b'\xff':
                if end_pos > next_marker_pos + 1:
                    next_marker = data[next_marker_pos:next_marker_pos+2]
                    if  next_marker in JFIFFileFormat.ValidMarkers:
                        break
            next_marker_pos += 1

        return next_marker_pos
    
    # --- Display Data --- #
    
    @staticmethod
    def show_data(data, start_label, end_label, length, tag='data', fout=sys.stdout):
        print(f'  - {tag}:', file=fout)
        print(f'        {data[:50]}', file=fout)
        print(f'        {data[-20:]}', file=fout)
        print(
            f'      - start: {start_label} (0x{start_label:x});'
            f' end: {end_label} (0x{end_label:x}); length: {length}',
            file=fout
        )
        print(f'      - hexdump:', file=fout)
        data_hexdump = HexDump.hexdump_start_and_end(data, pos_label=start_label)
        HexDump.print_hexdump(data_hexdump, prefix='          ', fout=fout)
        return
    
    # --- Main Function --- #
    
    @staticmethod
    def main():
        params = {
            'prog': 'parse_jfiffile',
            'description': 'Parse and list content of jfif files.',
            'file_arg_name': 'jfiffile',
            'file_arg_name_help': 'jfiffile to parse',
            'file_parse_function': JFIFFileFormat.parse,
        }
        FileFormat.main(params)
        return
    
if __name__ == '__main__':
    JFIFFileFormat.main()
    
# --- end of file --- #

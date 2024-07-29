# file: zipfile_format.py

from common_util.bytes_util import BytesUtility
from ctf_library.file_format.file_format import FileFormat

# Reference:
# - https://docs.fileformat.com/compression/zip/
# Free Sample ZIP Files:
# - https://file-examples.com/index.php/text-files-and-archives-download/

class ZipFileFormat(FileFormat):

    LocalFileHeaderSignature = b'\x50\x4b\x03\x04'
    CentralDirectoryFileHeaderSignature = b'\x50\x4b\x01\x02'
    EndOfCentralDirectorySignature = b'\x50\x4b\x05\x06'
    DataDescriptorSignature = b'\x50\x4b\x07\x08'

    # TODO: Not implemented
    Zip64EndOfCentralDirectorySignature = b'\x50\x4b\x06\x06'

    @staticmethod
    def parse(data, offset=0, max_length=-1):
        # end_of_data_pos = len(data)
        # if max_length > 0:
        #     end_of_data_pos = min(end_of_data_pos, offset + max_length)
        end_of_data_pos = ZipFileFormat.compute_end_position(
            data, offset=offset, max_length=max_length
        )

        data_length = end_of_data_pos - offset
        print(f'data lenght: {data_length}')

        curr_pos = offset

        while curr_pos < end_of_data_pos:
            signature = BytesUtility.extract_bytes(data, 0, 4, pos=curr_pos)
            print(f'=== found signature {signature} at {curr_pos}')
            if signature == ZipFileFormat.LocalFileHeaderSignature:
                curr_pos = ZipFileFormat.parse_local_file_header(
                    data, pos=curr_pos, end_pos=end_of_data_pos
                )
            elif signature == ZipFileFormat.CentralDirectoryFileHeaderSignature:
                curr_pos = ZipFileFormat.parse_central_directory_file_header(
                    data, pos=curr_pos, end_pos=end_of_data_pos
                )
            elif signature == ZipFileFormat.EndOfCentralDirectorySignature:
                curr_pos = ZipFileFormat.parse_end_of_central_directory_record(
                    data, pos=curr_pos, end_pos=end_of_data_pos
                )
            elif signature == ZipFileFormat.DataDescriptorSignature:
                curr_pos = ZipFileFormat.parse_data_descriptor(
                    data, pos=curr_pos, end_pos=end_of_data_pos
                )
            # elif signature.startswith(b'P'):
            #     curr_pos = ZipFileFormat.parse_data_descriptor(
            #         data, pos=curr_pos, end_pos=end_of_data_pos
            #     )
            else:
                curr_pos = ZipFileFormat.parse_unknown_signature(
                    data, pos=curr_pos, end_pos=end_of_data_pos
                )
            print()
        
        return curr_pos
    
    @staticmethod
    def parse_local_file_header(data, pos=0, end_pos=-1):
        if end_pos < 0:
            end_pos = len(data)
        curr_pos = pos

        header_length_fixed = 30

        print(f'local file header at offset {curr_pos}:')
        if end_pos >= curr_pos + header_length_fixed:
            signature = BytesUtility.extract_bytes(data, 0, 4, pos=curr_pos)
            version = BytesUtility.extract_integer(data, 4, 2, pos=curr_pos)
            bit_flag = BytesUtility.extract_integer(data, 6, 2, pos=curr_pos)
            compression_method = BytesUtility.extract_integer(data, 8, 2, pos=curr_pos)
            last_modified_time = BytesUtility.extract_integer(data, 10, 2, pos=curr_pos)
            last_modified_date = BytesUtility.extract_integer(data, 12, 2, pos=curr_pos)
            crc32 = BytesUtility.extract_bytes(data, 14, 4, pos=curr_pos)
            compressed_size = BytesUtility.extract_integer(data, 18, 4, pos=curr_pos)
            uncompressed_size = BytesUtility.extract_integer(data, 22, 4, pos=curr_pos)
            file_name_length = BytesUtility.extract_integer(data, 26, 2, pos=curr_pos)
            extra_field_length = BytesUtility.extract_integer(data, 28, 2, pos=curr_pos)

            print(f'  signature: {signature}')
            print(f'  minimum version needed to extract: {version}')
            print(f'  general purpose bit flag: {bit_flag:016b}')
            print(f'  compression method: {compression_method}')
            print(f'  file last modified time: {last_modified_time}')
            print(f'  file last modified date: {last_modified_date}')
            print(f'  crc32: {crc32}')
            print(f'  compressed size: {compressed_size} (0x{compressed_size:x})')
            print(f'  uncompressed size: {uncompressed_size} (0x{uncompressed_size:x})')
            print(f'  file name length: {file_name_length}')
            print(f'  extra field length: {extra_field_length}')
        else:
            return ZipFileFormat.error_insufficient_data(data, header_length_fixed, pos=curr_pos)

        curr_pos += header_length_fixed

        if end_pos >= curr_pos + file_name_length:
            filename = BytesUtility.extract_bytes(data, 0, file_name_length, pos=curr_pos)
            print(f'  file name: {filename}')
        else:
            return ZipFileFormat.error_insufficient_data(data, file_name_length, pos=curr_pos)

        curr_pos += file_name_length

        if end_pos >= curr_pos + extra_field_length:
            extra_field = BytesUtility.extract_bytes(data, 0, extra_field_length, pos=curr_pos)
            print(f'  extra field: {extra_field}')
        else:
            return ZipFileFormat.error_insufficient_data(data, extra_field_length, pos=curr_pos)

        curr_pos += extra_field_length

        is_zip64 = False
        has_data_descriptor = False

        # TODO: Check how the data_size is computed. (Done?)
        if compressed_size == 0xffffffff and uncompressed_size == 0xffffffff:
            is_zip64 = True
            has_data_descriptor = True
        else:
            is_zip64 = False
            if bit_flag & 0x08 != 0:
                has_data_descriptor = True
            else:
                has_data_descriptor = False

        if has_data_descriptor:
            next_signature_pos = ZipFileFormat.find_next_signature(
                data, curr_pos+1, end_pos=end_pos
            )
            data_size = next_signature_pos - curr_pos
            compressed_data = BytesUtility.extract_bytes(
                data, 0, data_size, pos=curr_pos
            )
        else:                
            data_size = compressed_size if compressed_size != 0 else uncompressed_size
            if end_pos >= curr_pos + data_size:
                compressed_data = BytesUtility.extract_bytes(
                    data, 0, data_size, pos=curr_pos
                )
            else:
                return ZipFileFormat.error_insufficient_data(data, data_size, pos=curr_pos)
                
        print(f'  data: {compressed_data[:50]}')
        print(f'    - start: {curr_pos}; end: {curr_pos+data_size}; length {data_size}')
        print(f'    - zip64: {is_zip64}')
        print(f'    - has data descriptor: {has_data_descriptor}')

        curr_pos += data_size

        return curr_pos

    @staticmethod
    def parse_central_directory_file_header(data, pos=0, end_pos=-1):
        if end_pos < 0:
            end_pos = len(data)
        curr_pos = pos

        header_length_fixed = 46

        print(f'central directory file header at offset {curr_pos}:')
        if end_pos >= curr_pos + header_length_fixed:
            signature = BytesUtility.extract_bytes(data, 0, 4, pos=curr_pos)
            #
            crc32 = BytesUtility.extract_bytes(data, 16, 4, pos=curr_pos)
            #
            file_name_length = BytesUtility.extract_integer(data, 28, 2, pos=curr_pos)
            extra_field_length = BytesUtility.extract_integer(data, 30, 2, pos=curr_pos)
            file_comment_length = BytesUtility.extract_integer(data, 32, 2, pos=curr_pos)
            #
            local_file_header_offset = BytesUtility.extract_integer(data, 42, 4, pos=curr_pos)

            print(f'  signature: {signature}')
            #
            print(f'  crc32: {crc32}')
            #
            print(f'  file name length: {file_name_length}')
            print(f'  extra field length: {extra_field_length}')
            print(f'  file comment length: {file_comment_length}')
            #
            print(f'  relative offset of local file header: {local_file_header_offset}')
        else:
            return ZipFileFormat.error_insufficient_data(data, header_length_fixed, pos=curr_pos)

        curr_pos += header_length_fixed

        if end_pos >= curr_pos + file_name_length:
            filename = BytesUtility.extract_bytes(data, 0, file_name_length, pos=curr_pos)
            print(f'  file name: {filename}')
        else:
            return ZipFileFormat.error_insufficient_data(data, file_name_length, pos=curr_pos)

        curr_pos += file_name_length

        if end_pos >= curr_pos + extra_field_length:
            extra_field = BytesUtility.extract_bytes(data, 0, extra_field_length, pos=curr_pos)
            print(f'  extra field: {extra_field}')
        else:
            return ZipFileFormat.error_insufficient_data(data, extra_field_length, pos=curr_pos)

        curr_pos += extra_field_length

        if end_pos >= curr_pos + file_comment_length:
            file_comment = BytesUtility.extract_bytes(data, 0, file_comment_length, pos=curr_pos)
            print(f'  file comment: {file_comment}')
        else:
            return ZipFileFormat.error_insufficient_data(data, file_comment_length, pos=curr_pos)

        curr_pos += file_comment_length

        return curr_pos
    
    @staticmethod
    def parse_end_of_central_directory_record(data, pos=0, end_pos=-1):
        if end_pos < 0:
            end_pos = len(data)
        curr_pos = pos

        header_length_fixed = 22

        print(f'end of central directory record at offset {curr_pos}:')
        if end_pos >= curr_pos + header_length_fixed:
            signature = BytesUtility.extract_bytes(data, 0, 4, pos=curr_pos)
            #
            comment_length = BytesUtility.extract_integer(data, 20, 2, pos=curr_pos)

            print(f'  signature: {signature}')
            #
            print(f'  comment length: {comment_length}')
        else:
            return ZipFileFormat.error_insufficient_data(data, header_length_fixed, pos=curr_pos)

        curr_pos += header_length_fixed

        if end_pos >= curr_pos + comment_length:
            comment = BytesUtility.extract_bytes(data, 0, comment_length, pos=curr_pos)
            print(f'  comment: {comment}')
        else:
            return ZipFileFormat.error_insufficient_data(data, comment_length, pos=curr_pos)

        curr_pos += comment_length

        return curr_pos
    
    @staticmethod
    def parse_data_descriptor(data, pos=0, end_pos=-1, with_signature=True, is_zip64=False):
        if end_pos < 0:
            end_pos = len(data)
        curr_pos = pos

        if with_signature:
            header_length_fixed = 4
            print(f'data descriptor signautre at offset {curr_pos}:')
            if end_pos >= curr_pos + header_length_fixed:
                signature = BytesUtility.extract_bytes(data, 0, 4, pos=curr_pos)
                print(f'  data descriptor signature {signature} at {curr_pos}')
            else:
                return ZipFileFormat.error_insufficient_data(data, header_length_fixed, pos=curr_pos)
        else:
            header_length_fixed = 0
            print(f'without data descriptor signature')

        next_signature_pos = ZipFileFormat.find_next_signature(
            data, curr_pos+1, end_pos=end_pos
        )
        descriptor_data_length = next_signature_pos - curr_pos
        descriptor_data = BytesUtility.extract_bytes(
            data, 0, descriptor_data_length, pos=curr_pos
        )
        print(f'  data at {curr_pos}-{next_signature_pos}: {descriptor_data}')
        print(f'    - length: {descriptor_data_length}')

        data_offset = header_length_fixed
        crc32 = BytesUtility.extract_bytes(data, data_offset, 4, pos=curr_pos)
        if is_zip64:
            compressed_size = BytesUtility.extract_integer(data, data_offset+4, 8, pos=curr_pos)
            uncompressed_size = BytesUtility.extract_integer(data, data_offset+12, 8, pos=curr_pos)
        else:
            compressed_size = BytesUtility.extract_integer(data, data_offset+4, 4, pos=curr_pos)
            uncompressed_size = BytesUtility.extract_integer(data, data_offset+8, 4, pos=curr_pos)
        print(f'  crc32: {crc32}')
        print(f'  compressed size: {compressed_size}')
        print(f'  uncompressed size: {uncompressed_size}')

        #curr_pos += skip_length_fixed
        curr_pos += descriptor_data_length

        return curr_pos
    
    @staticmethod
    def parse_unknown_signature(data, pos=0, end_pos=-1):
        if end_pos < 0:
            end_pos = len(data)
        curr_pos = pos

        skip_length_fixed = 4

        print(f'*** unknown signature at offset {curr_pos}:')
        if end_pos >= curr_pos + skip_length_fixed:
            signature = BytesUtility.extract_bytes(data, 0, 4, pos=curr_pos)
            print(f'  unknown signature {signature} at {curr_pos}')

        next_signature_pos = ZipFileFormat.find_next_signature(
            data, curr_pos+1, end_pos=end_pos
        )

        unknown_data_length = next_signature_pos - curr_pos
        #unknown_data = data[curr_pos:curr_pos+unknown_data_length]
        unknown_data = BytesUtility.extract_bytes(
            data, 0, unknown_data_length, pos=curr_pos
        )
        print(f'  unknown data length: {unknown_data_length}')
        print(f'  data at {curr_pos}-{next_signature_pos}: {unknown_data}')

        curr_pos += unknown_data_length

        return curr_pos
    
    @staticmethod
    def find_next_signature(data, start_pos, end_pos=-1):
        if end_pos <= 0:
            end_pos = len(data)
        # resync to the next b'PK'
        next_signature_pos = start_pos
        while end_pos >= next_signature_pos:
            if BytesUtility.extract_bytes(data, 0, 2, pos=next_signature_pos) == b'PK':
                break
            next_signature_pos += 1
        return next_signature_pos
    
# --- end of file --- #

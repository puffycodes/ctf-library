# file: zipfile_format.py

from common_util.bytes_util import BytesUtility
from ctf_library.file_format.file_format import FileFormat

# Reference:
# - https://en.wikipedia.org/wiki/ZIP_(file_format)
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
    Zip64SomeSignature = b'\x50\x4b\x06\x07'

    @staticmethod
    def parse(data, offset=0, max_length=-1):
        end_of_data_pos = ZipFileFormat.compute_end_position(
            data, offset=offset, max_length=max_length
        )

        data_length = end_of_data_pos - offset
        print(f'data length: {data_length} (0x{data_length:x})')
        print()

        curr_pos = offset

        while curr_pos < end_of_data_pos:
            signature = BytesUtility.extract_bytes(data, 0, 4, pos=curr_pos)
            print(f'=== found signature {signature} at {curr_pos} (0x{curr_pos:x})')
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
            elif signature == ZipFileFormat.Zip64EndOfCentralDirectorySignature:
                curr_pos = ZipFileFormat.parse_zip64_end_of_central_directory_record(
                    data, pos=curr_pos, end_pos=end_of_data_pos
                )
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
        data_size_undetermined = False

        if compressed_size == 0xffffffff and uncompressed_size == 0xffffffff:
            is_zip64 = True
            has_data_descriptor = True # TODO: True or False? Or irrelevant?
            data_size_undetermined = True
        else:
            is_zip64 = False
            if bit_flag & 0x08 != 0:
                has_data_descriptor = True
                data_size_undetermined = True
            else:
                has_data_descriptor = False
                data_size_undetermined = False

        if data_size_undetermined:
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
            version_made = BytesUtility.extract_integer(data, 4, 2, pos=curr_pos)
            version_needed = BytesUtility.extract_integer(data, 6, 2, pos=curr_pos)
            bit_flag = BytesUtility.extract_integer(data, 8, 2,pos=curr_pos)
            compression_method = BytesUtility.extract_integer(data, 10, 2, pos=curr_pos)
            last_modification_time = BytesUtility.extract_integer(data, 12, 2, pos=curr_pos)
            last_modification_date = BytesUtility.extract_integer(data, 14, 2, pos=curr_pos)
            crc32 = BytesUtility.extract_bytes(data, 16, 4, pos=curr_pos)
            compressed_size = BytesUtility.extract_integer(data, 20, 4, pos=curr_pos)
            uncompressed_size = BytesUtility.extract_bytes(data, 24, 4, pos=curr_pos)
            file_name_length = BytesUtility.extract_integer(data, 28, 2, pos=curr_pos)
            extra_field_length = BytesUtility.extract_integer(data, 30, 2, pos=curr_pos)
            file_comment_length = BytesUtility.extract_integer(data, 32, 2, pos=curr_pos)
            disk_number_file_start = BytesUtility.extract_integer(data, 34, 2, pos=curr_pos)
            file_attribute_internal = BytesUtility.extract_integer(data, 36, 2, pos=curr_pos)
            file_attribute_external = BytesUtility.extract_integer(data, 38, 4, pos=curr_pos)
            local_file_header_offset = BytesUtility.extract_integer(data, 42, 4, pos=curr_pos)

            print(f'  signature: {signature}')
            print(f'  made with version: {version_made}')
            print(f'  version needed to extract: {version_needed}')
            print(f'  general purpose bit flag: {bit_flag:b}')
            print(f'  compression method: {compression_method}')
            print(f'  file last modification time: {last_modification_time}')
            print(f'  file last modification date: {last_modification_date}')
            print(f'  crc32: {crc32}')
            print(f'  compressed size: {compressed_size}')
            print(f'  uncompressed size: {uncompressed_size}')
            print(f'  file name length: {file_name_length}')
            print(f'  extra field length: {extra_field_length}')
            print(f'  file comment length: {file_comment_length}')
            print(f'  file starts at disk: {disk_number_file_start}')
            print(f'  internal file attributes: {file_attribute_internal}')
            print(f'  external file attribute: {file_attribute_external}')
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
            disk_number = BytesUtility.extract_integer(data, 4, 2, pos=curr_pos)
            disk_of_central_directory = BytesUtility.extract_integer(data, 6, 2, pos=curr_pos)
            directory_count_this_disk = BytesUtility.extract_integer(data, 8, 2, pos=curr_pos)
            directory_count_total = BytesUtility.extract_integer(data, 10, 2, pos=curr_pos)
            directory_size = BytesUtility.extract_integer(data, 12, 4, pos=curr_pos)
            directory_start = BytesUtility.extract_integer(data, 16, 4, pos=curr_pos)
            comment_length = BytesUtility.extract_integer(data, 20, 2, pos=curr_pos)

            print(f'  signature: {signature}')
            print(f'  this disk number: {disk_number}')
            print(f'  disk where central directory starts: {disk_of_central_directory}')
            print(f'  number of central directory on this disk: {directory_count_this_disk}')
            print(f'  total number of central directory: {directory_count_total}')
            print(f'  central directory size: {directory_size}')
            print(f'  start of central directory: {directory_start}')            #
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
        print(f'  data: {descriptor_data}')
        print(f'    - start: {curr_pos}; end: {next_signature_pos}; length: {descriptor_data_length}')

        data_offset = header_length_fixed
        crc32 = BytesUtility.extract_bytes(data, data_offset, 4, pos=curr_pos)
        if is_zip64:
            compressed_size = BytesUtility.extract_integer(data, data_offset+4, 8, pos=curr_pos)
            uncompressed_size = BytesUtility.extract_integer(data, data_offset+12, 8, pos=curr_pos)
        else:
            compressed_size = BytesUtility.extract_integer(data, data_offset+4, 4, pos=curr_pos)
            uncompressed_size = BytesUtility.extract_integer(data, data_offset+8, 4, pos=curr_pos)
        print(f'  crc32: {crc32}')
        print(f'  compressed size: {compressed_size} (0x{compressed_size:x})')
        print(f'  uncompressed size: {uncompressed_size} (0x{uncompressed_size:x})')

        curr_pos += descriptor_data_length

        return curr_pos

    @staticmethod
    def parse_zip64_end_of_central_directory_record(data, pos=0, end_pos=-1):
        if end_pos < 0:
            end_pos = len(data)
        curr_pos = pos

        header_length_fixed = 56

        print(f'zip64 end of central directory record at offset {curr_pos}:')
        if end_pos >= curr_pos + header_length_fixed:
            signature = BytesUtility.extract_bytes(data, 0, 4, pos=curr_pos)
            eocd64_size = BytesUtility.extract_integer(data, 4, 8, pos=curr_pos)
            version_made_by = BytesUtility.extract_integer(data, 12, 2, pos=curr_pos)
            version_needed = BytesUtility.extract_integer(data, 14, 2, pos=curr_pos)
            disk_number = BytesUtility.extract_integer(data, 16, 4, pos=curr_pos)
            disk_of_central_directory = BytesUtility.extract_integer(data, 20, 4, pos=curr_pos)
            directory_count_this_disk = BytesUtility.extract_integer(data, 24, 8, pos=curr_pos)
            directory_count_total = BytesUtility.extract_integer(data, 32, 8, pos=curr_pos)
            directory_size = BytesUtility.extract_integer(data, 40, 8, pos=curr_pos)
            directory_start = BytesUtility.extract_integer(data, 48, 8, pos=curr_pos)
            comment_length = eocd64_size - 56 + 12

            print(f'  signature: {signature}')
            print(f'  record size: {eocd64_size}')
            print(f'  made with version: {version_made_by}')
            print(f'  version needed to extract: {version_needed}')
            print(f'  this disk number: {disk_number}')
            print(f'  disk where central directory starts: {disk_of_central_directory}')
            print(f'  number of directory records on this disk: {directory_count_this_disk}')
            print(f'  total number of directory records: {directory_count_total}')
            print(f'  size of central directory: {directory_size}')
            print(f'  start of central directory: {directory_start}')
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
        unknown_data = BytesUtility.extract_bytes(
            data, 0, unknown_data_length, pos=curr_pos
        )
        print(f'  data: {unknown_data}')
        print(f'    - start: {curr_pos}; end: {next_signature_pos}; length: {unknown_data_length}')

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
    
    @staticmethod
    def main():
        params = {
            'prog': 'parse_zipfile',
            'description': 'Parse and list content of zipfiles.',
            'file_arg_name': 'zipfile',
            'file_arg_name_help': 'zipfile to parse',
            'file_parse_function': ZipFileFormat.parse,
        }
        FileFormat.main(params)
        return
    
if __name__ == '__main__':
    ZipFileFormat.main()
    
# --- end of file --- #

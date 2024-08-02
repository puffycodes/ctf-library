# file: gzipfile_format_test.py

import unittest
import gzip
import binascii
from ctf_library.file_format.gzipfile_format import GzipFileFormat
from common_util.dir_util import DirectoryUtility
from common_util.bytes_util import BytesUtility

class GzipFileFormatTest(unittest.TestCase):

    data_file_dir = 'data/gzipfile'

    def test_list_and_parse_zipfile(self):
        file_list = DirectoryUtility.list_files(
            GzipFileFormatTest.data_file_dir, '*.gz', recursive=True
        )
        if len(file_list) <= 0:
            print(f'no gzip files in directory "{GzipFileFormatTest.data_file_dir}"')
            return
        for file in file_list:
            print(f'=== file: {file}')
            try:
                with open(file, 'rb') as fd:
                    gzip_data = fd.read()
            except Exception as e:
                print(f'*** cannot read gzip file {file}: Error: {e}')
                print()
                continue
            end_pos = GzipFileFormat.parse(gzip_data)
            print(f'---------')
            print(f'verification using gzip:')
            try:
                ungzip_data = gzip.decompress(gzip_data)
                crc = binascii.crc32(ungzip_data)
                crc_bytes = BytesUtility.integer_to_bytes(crc, 4)
                print(f'  uncompressed data: {ungzip_data[:40]}')
                print(f'                     {ungzip_data[-20:]}')
                print(f'    - length: {len(ungzip_data)}')
                print(f'    - crc: {crc_bytes}')
            except Exception as e:
                print(f'  cannot uncompress data: Error: {e}')
            print(f'---------')
            print(f'data length is {len(gzip_data)}')
            print(f'parsing ends at offset {end_pos}')
            print(f'---------')
            print()
        return
    
if __name__ == '__main__':
    unittest.main()

# --- end of file --- #

# file: gzipfile_format_test.py

import unittest
from ctf_library.file_format.gzipfile_format import GzipFileFormat
from common_util.dir_util import DirectoryUtility

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
            print(f'data length is {len(gzip_data)}')
            print(f'parsing ends at offset {end_pos}')
            print(f'---------')
            print()
        return
    
if __name__ == '__main__':
    unittest.main()

# --- end of file --- #

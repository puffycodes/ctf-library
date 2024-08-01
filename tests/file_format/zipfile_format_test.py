# file: zipfile_format_test.py

import unittest
from ctf_library.file_format.zipfile_format import ZipFileFormat
from common_util.dir_util import DirectoryUtility

class ZipFileFormatTest(unittest.TestCase):

    data_file_dir = 'data/zipfile'

    def test_list_and_parse_zipfile(self):
        file_list = DirectoryUtility.list_files(
            ZipFileFormatTest.data_file_dir, '*.zip', recursive=True
        )
        if len(file_list) <= 0:
            print(f'no Zip files in directory "{ZipFileFormatTest.data_file_dir}"')
            return
        for file in file_list:
            print(f'=== file: {file}')
            try:
                with open(file, 'rb') as fd:
                    zip_data = fd.read()
            except Exception as e:
                print(f'*** cannot read Zip file {file}: Error: {e}')
                print()
                continue
            end_pos = ZipFileFormat.parse(zip_data)
            print(f'---------')
            print(f'data length is {len(zip_data)}')
            print(f'parsing ends at offset {end_pos}')
            print(f'---------')
            print()
        return
    
    def test_get_zipfile_records(self):
        file_list = DirectoryUtility.list_files(
            ZipFileFormatTest.data_file_dir, '*.zip', recursive=True
        )
        if len(file_list) <= 0:
            print(f'no Zip files in directory "{ZipFileFormatTest.data_file_dir}"')
            return
        for file in file_list:
            print(f'=== file: {file}')
            try:
                with open(file, 'rb') as fd:
                    zip_data = fd.read()
            except Exception as e:
                print(f'*** cannot read Zip file {file}: Error: {e}')
                print()
                continue
            print(f'total length: {len(zip_data)}')
            records = ZipFileFormat.get_zipfile_records(zip_data)
            for type, signature, start, end in records:
                print(f'{type} {signature}: {start} - {end}')
            print()
        return
    
if __name__ == '__main__':
    unittest.main()

# --- end of file --- #

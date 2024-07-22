# file: pngfile_format_test.py

import unittest
from ctf_library.file_format.pngfile_format import PNGFileFormat
from common_util.dir_util import DirectoryUtility

class PNGFileFormatTest(unittest.TestCase):

    data_file_dir = 'data/pngfile'

    def test_list_and_parse_pngfile(self):
        file_list = DirectoryUtility.list_files(
            PNGFileFormatTest.data_file_dir, '*.png', recursive=True
        )
        if len(file_list) <= 0:
            print(f'no PNG files in directory "{PNGFileFormatTest.data_file_dir}"')
            return
        for file in file_list:
            print(f'=== file: {file}')
            if not file.endswith('.png'):
                print(f'*** {file} is not a PNG file')
                print()
                continue
            try:
                with open(file, 'rb') as fd:
                    png_data = fd.read()
            except Exception as e:
                print(f'*** cannot read PNG file {file}: Error: {e}')
                print()
                continue
            end_pos = PNGFileFormat.parse(png_data)
            print(f'-----------')
            print(f'data length is {len(png_data)}')
            print(f'parsing ends at offset {end_pos}')
            print(f'-----------')
            print()
        return

if __name__ == '__main__':
    unittest.main()

# --- end of file --- #

# file: usb_keystroke_decoder_test.py

import unittest
from scapy.all import *
from ctf_library.packet.usb_keystroke_decoder import USBKeystrokeDecoder
from common_util.dir_util import DirectoryUtility

class USBKeystrokeDecoderTest(unittest.TestCase):

    data_file_dir = 'data'

    def test_decoder(self):
        print('empty test')
        file_list = DirectoryUtility.list_files(USBKeystrokeDecoderTest.data_file_dir, '*.pcap*', recursive=True)
        for file in file_list:
            print(f'file: {file}')
            packets = rdpcap(file)
            print(len(packets))
            for p in packets[:10]:
                print(f'{p}')
        return
    
    def test_print_decoder_string(self):
        decoder = USBKeystrokeDecoder()
        print(f'=====')
        print(f'unshift table: {decoder.unshift_table} ({len(decoder.unshift_table)})')
        print(f'shift table:   {decoder.shift_table} ({len(decoder.shift_table)})')
        print(f'=====')
        return
    
if __name__ == '__main__':
    unittest.main()

# --- end of file --- #

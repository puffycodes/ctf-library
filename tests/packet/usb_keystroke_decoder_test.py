# file: usb_keystroke_decoder_test.py

import unittest
from scapy.all import *
from ctf_library.packet.usb_keystroke_decoder import USBKeystrokeDecoder
from common_util.dir_util import DirectoryUtility

class USBKeystrokeDecoderTest(unittest.TestCase):

    data_file_dir = 'data/usb_keystroke'

    def test_list_and_decode_pcap_files(self):
        decoder = USBKeystrokeDecoder()
        file_list = DirectoryUtility.list_files(
            USBKeystrokeDecoderTest.data_file_dir, '*.pcap*', recursive=True
        )
        if len(file_list) == 0:
            print(f'no capture files in directory "{USBKeystrokeDecoderTest.data_file_dir}"')
            return
        for file in file_list:
            print(f'=== file: {file}')
            if not file.endswith('.pcap') and not file.endswith('.pcapng'):
                print(f'*** {file} is not a pcap file.')
                continue
            try:
                packets = rdpcap(file)
            except Exception as e:
                print(f'*** cannot read pcap file: Error: {e}')
                continue
            print(f'number of packets: {len(packets)}')
            for p in packets[:5]:
                self.print_packet(p)
            result = decoder.decode_packets(packets)
            print(f'==> final result:')
            for line in result:
                print(f'  {line}')
        return
    
    def print_packet(self, packet):
        try:
            payload = packet.load
            print(f'{packet}: {payload}')
        except AttributeError as e:
            print(f'{packet}')
        return
    
    def test_print_decoder_string(self):
        decoder = USBKeystrokeDecoder()
        print(f'=====')
        print(f'unshift table: {decoder.unshift_table} ({len(decoder.unshift_table)})')
        print(f'shift table:   {decoder.shift_table} ({len(decoder.shift_table)})')
        print(f'-----')
        print(f'numpad table:  {decoder.numpad_table} ({len(decoder.numpad_table)})')
        print(f'=====')
        return
    
if __name__ == '__main__':
    unittest.main()

# --- end of file --- #

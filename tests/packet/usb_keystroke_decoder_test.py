# file: usb_keystroke_decoder_test.py

import unittest
from scapy.all import *
from ctf_library.packet.usb_keystroke_decoder import USBKeystrokeDecoder, USBKeystrokeTable, USBKeyboard
from common_util.dir_util import DirectoryUtility

class USBKeystrokeDecoderTest(unittest.TestCase):

    data_file_dir = 'data/usb_keystroke'

    def test_list_and_decode_pcap_files(self):
        decoder = USBKeystrokeDecoder()
        file_list = DirectoryUtility.list_files(
            USBKeystrokeDecoderTest.data_file_dir, '*.pcap*', recursive=True
        )
        if len(file_list) <= 0:
            print(f'no capture files in directory "{USBKeystrokeDecoderTest.data_file_dir}"')
            return
        for file in file_list:
            print(f'=== file: {file}')
            if not file.endswith('.pcap') and not file.endswith('.pcapng'):
                print(f'*** {file} is not a pcap file.')
                print()
                continue
            try:
                packets = rdpcap(file)
            except Exception as e:
                print(f'*** cannot read pcap file: Error: {e}')
                print()
                continue
            show_packets = False
            if show_packets:
                print(f'---------- packets')
                print(f'number of packets: {len(packets)}')
                for p in packets[:5]:
                    self.print_packet(p)
            print(f'---------- keystroke list')
            keystroke_processor = USBKeystrokeDecoder.KeystrokeList()
            result_list = decoder.decode_packets(
                packets, keystroke_processor=keystroke_processor,
                keyboard_type=USBKeyboard.Keyboard_Type_1,
                verbose=False, debug=False
            )
            print(result_list.get_result())
            print(f'---------- output of decode_packets(): Keyboard_Type_1')
            result_01 = decoder.decode_packets(
                packets, keystroke_processor=None, keyboard_type=USBKeyboard.Keyboard_Type_1,
                verbose=False, debug=False
            )
            result_text_01 = result_01.get_text()
            print(result_text_01)
            print(f'---------- output of decode_packets(): Keyboard_Type_2')
            result_02 = decoder.decode_packets(
                packets, keystroke_processor=None, keyboard_type=USBKeyboard.Keyboard_Type_2,
                verbose=False, debug=False
            )
            result_text_02 = result_02.get_text()
            print(result_text_02)
            print(f'---------- comparison')
            result_comparison = result_text_01 == result_text_02
            print(f'result_text_01 == result_text_02? {result_comparison}')
            test_old = False
            if test_old:
                print(f'---------- output of decode_packets_old()')
                result = decoder.decode_packets_old(packets)
                print(f'==> final result:')
                for line in result:
                    print(f'  {line}')
            print(f'----------')
            print()
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
    
class USBKeystrokeTableTest(unittest.TestCase):
    
    def test_print_keystroke_table(self):
        keystroke_table = USBKeystrokeTable()
        print(f'=====')
        print(f'- unshift table length: {len(keystroke_table.unshift_table)}')
        print(f'- unshift table: {keystroke_table.unshift_table}')
        print(f'- shift table length: {len(keystroke_table.shift_table)}')
        print(f'- shift table: {keystroke_table.shift_table}')
        print(f'=====')
        return
    
    def test_check_keystroke_table(self):
        keystroke_table = USBKeystrokeTable()
        keystorke_test_list = [
            [False, 4, 'a'], [True, 4, 'A'], [False, 39, '0'], [True, 39, ')'],
            [False, 44, ' '], [True, 44, ' '], [False, 45, '-'], [True, 45, '_'],
            [False, 40, USBKeystrokeTable.Key_Enter],
            [True, 40, USBKeystrokeTable.Key_Enter],
            [False, 88, USBKeystrokeTable.Key_Enter],
            [True, 88, USBKeystrokeTable.Key_Enter],
            [False, 57, USBKeystrokeTable.Key_CapsLock],
            [True, 57, USBKeystrokeTable.Key_CapsLock],
            [False, 0x32, '#'], [True, 0x32, '~'],
        ]
        for shift, key_code, expected_key in keystorke_test_list:
            key = keystroke_table.get_key_value(key_code, shift=shift)
            self.assertEqual(key, expected_key)
        return
    
    def test_check_special_key(self):
        keystroke_table = USBKeystrokeTable()
        special_key_test_list = [
            ['a', False], ['=', False], ['`', False],
            [USBKeystrokeTable.Key_UpArrow, True],
            [USBKeystrokeTable.Key_Unknown, False],
        ]
        for key_value, expected_result in special_key_test_list:
            is_special_key = keystroke_table.is_special_key_value(key_value)
            self.assertEqual(is_special_key, expected_result)
        return
    
if __name__ == '__main__':
    unittest.main()

# --- end of file --- #

# file: windows_defender_quarantine_file.py

# Ref: https://reversingfun.com/posts/how-to-extract-quarantine-files-from-windows-defender/
# Ref: https://static.ernw.de/whitepaper/ERNW-Whitepaper-71_AV_Quarantine_signed.pdf

import os
import argparse
from Crypto.Cipher import ARC4
from common_util.bytes_util import BytesUtility
from common_util.dir_util import DirectoryUtility
from common_util.hexdump import HexDump
from ctf_library.file_format.file_format import FileFormat

class WindowsDefenderQuarantineFile(FileFormat):

    # Decryption Key for Windows Defender Quarantine Files (RC4)
    decryption_key = [
        0x1E, 0x87, 0x78, 0x1B, 0x8D, 0xBA, 0xA8, 0x44, 0xCE, 0x69, 0x70, 0x2C, 0x0C,
        0x78, 0xB7, 0x86, 0xA3, 0xF6, 0x23, 0xB7, 0x38, 0xF5, 0xED, 0xF9, 0xAF, 0x83,
        0x53, 0x0F, 0xB3, 0xFC, 0x54, 0xFA, 0xA2, 0x1E, 0xB9, 0xCF, 0x13, 0x31, 0xFD,
        0x0F, 0x0D, 0xA9, 0x54, 0xF6, 0x87, 0xCB, 0x9E, 0x18, 0x27, 0x96, 0x97, 0x90,
        0x0E, 0x53, 0xFB, 0x31, 0x7C, 0x9C, 0xBC, 0xE4, 0x8E, 0x23, 0xD0, 0x53, 0x71,
        0xEC, 0xC1, 0x59, 0x51, 0xB8, 0xF3, 0x64, 0x9D, 0x7C, 0xA3, 0x3E, 0xD6, 0x8D,
        0xC9, 0x04, 0x7E, 0x82, 0xC9, 0xBA, 0xAD, 0x97, 0x99, 0xD0, 0xD4, 0x58, 0xCB,
        0x84, 0x7C, 0xA9, 0xFF, 0xBE, 0x3C, 0x8A, 0x77, 0x52, 0x33, 0x55, 0x7D, 0xDE,
        0x13, 0xA8, 0xB1, 0x40, 0x87, 0xCC, 0x1B, 0xC8, 0xF1, 0x0F, 0x6E, 0xCD, 0xD0,
        0x83, 0xA9, 0x59, 0xCF, 0xF8, 0x4A, 0x9D, 0x1D, 0x50, 0x75, 0x5E, 0x3E, 0x19,
        0x18, 0x18, 0xAF, 0x23, 0xE2, 0x29, 0x35, 0x58, 0x76, 0x6D, 0x2C, 0x07, 0xE2,
        0x57, 0x12, 0xB2, 0xCA, 0x0B, 0x53, 0x5E, 0xD8, 0xF6, 0xC5, 0x6C, 0xE7, 0x3D,
        0x24, 0xBD, 0xD0, 0x29, 0x17, 0x71, 0x86, 0x1A, 0x54, 0xB4, 0xC2, 0x85, 0xA9,
        0xA3, 0xDB, 0x7A, 0xCA, 0x6D, 0x22, 0x4A, 0xEA, 0xCD, 0x62, 0x1D, 0xB9, 0xF2,
        0xA2, 0x2E, 0xD1, 0xE9, 0xE1, 0x1D, 0x75, 0xBE, 0xD7, 0xDC, 0x0E, 0xCB, 0x0A,
        0x8E, 0x68, 0xA2, 0xFF, 0x12, 0x63, 0x40, 0x8D, 0xC8, 0x08, 0xDF, 0xFD, 0x16,
        0x4B, 0x11, 0x67, 0x74, 0xCD, 0x0B, 0x9B, 0x8D, 0x05, 0x41, 0x1E, 0xD6, 0x26,
        0x2E, 0x42, 0x9B, 0xA4, 0x95, 0x67, 0x6B, 0x83, 0x98, 0xDB, 0x2F, 0x35, 0xD3,
        0xC1, 0xB9, 0xCE, 0xD5, 0x26, 0x36, 0xF2, 0x76, 0x5E, 0x1A, 0x95, 0xCB, 0x7C,
        0xA4, 0xC3, 0xDD, 0xAB, 0xDD, 0xBF, 0xF3, 0x82, 0x53
    ]

    # Folder Names
    default_main_folder = 'C:\\ProgramData\\Microsoft\\Windows Defender\\Quarantine'
    entries_sub_folder = 'Entries'
    resources_sub_folder = 'Resources'
    resource_data_sub_folder = 'ResourceData'
    all_sub_folders = [
        entries_sub_folder, resources_sub_folder, resource_data_sub_folder,
    ]

    # Header Values
    entries_file_id = bytes([
        0xdb, 0xe8, 0xc5, 0x01, 0x01, 0, 0x01, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    ])
    resource_data_file_id = bytes([
        0x03, 0, 0, 0, 0x02, 0, 0, 0,
    ])

    # Header Lengths
    entries_file_part_1_length = 0x3c
    entries_file_part_2_length_offset = 0x28
    entries_file_part_3_length_offset = 0x28 + 4

    @staticmethod
    def parse_entries_file(entries_filename):
        with open(entries_filename, 'rb') as fd:
            entries_file_data_encrypted = fd.read()
        end_pos = WindowsDefenderQuarantineFile.parse_entries_file_data(
            entries_file_data_encrypted
        )
        return end_pos
    
    @staticmethod
    def parse_resources_file(resources_filename):
        with open(resources_filename, 'rb') as fd:
            resources_file_data_encrypted = fd.read()
        end_pos = WindowsDefenderQuarantineFile.parse_resources_file_data(
            resources_file_data_encrypted
        )
        return end_pos

    @staticmethod
    def parse_resource_data_file(resource_data_filename):
        with open(resource_data_filename, 'rb') as fd:
            resource_data_file_data_encrypted = fd.read()
        end_pos = WindowsDefenderQuarantineFile.parse_resource_data_file_data(
            resource_data_file_data_encrypted, is_encrypted=True
        )
        return end_pos
    
    @staticmethod
    def parse_entries_file_data(data, offset=0, max_length=-1):
        end_of_data_pos = WindowsDefenderQuarantineFile.compute_end_position(
            data, offset=offset, max_length=max_length
        )

        data_length = end_of_data_pos - offset
        print(f'data length: {data_length} (0x{data_length:x})')
        print()

        curr_pos = offset

        header_length_fixed = WindowsDefenderQuarantineFile.entries_file_part_1_length

        # Data Block #1
        if end_of_data_pos >= curr_pos + header_length_fixed:
            encrypted_part_1_data = BytesUtility.extract_bytes(
                data, 0, WindowsDefenderQuarantineFile.entries_file_part_1_length, pos=curr_pos
            )
            decrypted_part_1_data = WindowsDefenderQuarantineFile.decrypt_data(
                encrypted_part_1_data
            )

            HexDump.hexdump_and_print(
                [ decrypted_part_1_data ], [ 'entries file part #1:' ], [ curr_pos ]
            )

            file_id = BytesUtility.extract_bytes(decrypted_part_1_data, 0, 0x10, pos=0)
            unknown_data_01 = BytesUtility.extract_bytes(
                decrypted_part_1_data, 0x10, 0x18, pos=0
            )
            length_2, length_3 = WindowsDefenderQuarantineFile.get_entries_file_parts_length(
                decrypted_part_1_data, is_encrypted=False
            )
            unknown_data_02 = BytesUtility.extract_bytes(
                decrypted_part_1_data, 0x30, 0x0c, pos=0
            )

            file_id_hex = HexDump.to_hex(file_id)
            unknown_data_01_hex = HexDump.to_hex(unknown_data_01)
            unknown_data_02_hex = HexDump.to_hex(unknown_data_02)
            if file_id == WindowsDefenderQuarantineFile.entries_file_id:
                print(f'file id: {file_id_hex}')
            else:
                print(f'unknown file id: {file_id_hex}')
            print(f'unknown data #1: {unknown_data_01_hex}')
            print(f'length #1: {length_2} (0x{length_2:x})')
            print(f'length #2: {length_3} (0x{length_3:x})')
            print(f'unknown data #2: {unknown_data_02_hex}')
            print()
        else:
            WindowsDefenderQuarantineFile.error_insufficient_data(
                data, header_length_fixed, pos=curr_pos
            )

        curr_pos += header_length_fixed

        # Data Block #2
        if end_of_data_pos >= curr_pos + length_2:
            encrypted_part_2_data = BytesUtility.extract_bytes(
                data, 0, length_2, pos=curr_pos
            )
            decrypted_part_2_data = WindowsDefenderQuarantineFile.decrypt_data(
                encrypted_part_2_data
            )

            HexDump.hexdump_and_print(
                [ decrypted_part_2_data ], [ 'entries file part #2:' ], [ curr_pos ]
            )

            curr_offset = 0
            guid = BytesUtility.extract_bytes(
                decrypted_part_2_data, curr_offset, WindowsDefenderQuarantineFile.Extraction.LENGTH_GUID,
                pos=0
            )
            curr_offset += WindowsDefenderQuarantineFile.Extraction.LENGTH_GUID
            unknown_data_03 = BytesUtility.extract_bytes(
                decrypted_part_2_data, curr_offset, 0x10, pos=0
            )
            curr_offset += 0x10
            timestamp = BytesUtility.extract_bytes(
                decrypted_part_2_data,
                curr_offset, WindowsDefenderQuarantineFile.Extraction.LENGTH_WIN_FILE_TIME,
                pos=0
            )

            curr_offset += WindowsDefenderQuarantineFile.Extraction.LENGTH_WIN_FILE_TIME
            id_11 = BytesUtility.extract_integer(
                decrypted_part_2_data, curr_offset, 4, endian='little', pos=0
            )
            curr_offset += 4
            id_12 = BytesUtility.extract_integer(
                decrypted_part_2_data, curr_offset, 2, endian='little', pos=0
            )
            curr_offset += 2
            id_13 = BytesUtility.extract_integer(
                decrypted_part_2_data, curr_offset, 2, endian='little', pos=0
            )
            curr_offset += 2
            number_of_strings = BytesUtility.extract_integer(
                decrypted_part_2_data, curr_offset, 4, endian='little', pos=0
            )
            curr_offset += 4
            malware_type_list = []
            for _ in range(number_of_strings):
                curr_malware_type = BytesUtility.extract_bytes_until(
                    decrypted_part_2_data, curr_offset, b'\x00', include_marker=True
                )
                malware_type_list.append(curr_malware_type.decode('utf-8').strip())
                curr_offset += len(curr_malware_type)

            guid_hex = HexDump.to_hex(guid)
            unknown_data_03_hex = HexDump.to_hex(unknown_data_03)
            timestamp_hex = HexDump.to_hex(timestamp)
            print(f'guid: {guid_hex}')
            print(f'unknown data #3: {unknown_data_03_hex}')
            print(f'timestamp: {timestamp_hex}')
            print(f'id 11: {id_11}')
            print(f'id 12: {id_12}')
            print(f'id 13: {id_13}')
            print(f'number of strings: {number_of_strings}')
            print(f'malware types:')
            for m_type in malware_type_list:
                print(f'- {m_type}')
            print()
        else:
            WindowsDefenderQuarantineFile.error_insufficient_data(data, length_2, pos=0)

        curr_pos += length_2

        # Data Block #3
        if end_of_data_pos >= curr_pos + length_3:
            encrypted_part_3_data = BytesUtility.extract_bytes(
                data, 0, length_3, pos=curr_pos
            )
            decrypted_part_3_data = WindowsDefenderQuarantineFile.decrypt_data(
                encrypted_part_3_data
            )
            
            HexDump.hexdump_and_print(
                [ decrypted_part_3_data ], [ 'entries file part #3:' ], [ curr_pos ]
            )

            curr_offset = 0
            number_of_entries = BytesUtility.extract_integer(
                decrypted_part_3_data, curr_offset, 4, endian='little', pos=0
            )
            curr_offset += 4
            entries_offset_list = []
            for _ in range(number_of_entries):
                curr_entries_offset = BytesUtility.extract_integer(
                    decrypted_part_3_data, curr_offset, 4, endian='little', pos=0
                )
                entries_offset_list.append(curr_entries_offset)
                curr_offset += 4
            entries_data_list = []
            for curr_entries_offset in entries_offset_list:
                curr_entries_data = BytesUtility.extract_bytes_until(
                    decrypted_part_3_data, curr_entries_offset, marker=b'\x00\x00',
                    step=2, pos=0, include_marker=True
                )
                curr_offset += len(curr_entries_data)
                if len(curr_entries_data) % 2 != 0:
                    curr_offset += 1
                entries_data_list.append(curr_entries_data.decode('utf-16').strip())

            remaining_data_label = f'remaining data at {curr_pos+curr_offset} (0x{(curr_pos+curr_offset):x})'
            HexDump.hexdump_and_print(
                [ decrypted_part_3_data[curr_offset:] ],
                label_list=[ remaining_data_label ], pos_label_list=[ curr_pos + curr_offset ]
            )

            # TODO: Continue the extraction and printing of fields

            print(f'number of entries: {number_of_entries}')
            print(f'offsets:')
            for i in range(number_of_entries):
                print(f'- entry {i+1} at {entries_offset_list[i]}: {entries_data_list[i]}')
            print()
        else:
            WindowsDefenderQuarantineFile.error_insufficient_data(data, length_3, pos=0)

        curr_pos += length_3

        print(f'parsing ends at {curr_pos} (0x{curr_pos:x})')

        return curr_pos

    @staticmethod
    def parse_resources_file_data(data, offset=0, max_length=-1, is_encrypted=True):
        if is_encrypted:
            data = WindowsDefenderQuarantineFile.decrypt_data(data)

        end_of_data_pos = WindowsDefenderQuarantineFile.compute_end_position(
            data, offset=offset, max_length=max_length
        )

        data_length = end_of_data_pos - offset
        print(f'data length: {data_length} (0x{data_length:x})')
        print()

        curr_pos = offset

        # TODO: to implement
        print(f'not implemented yet')
        print()

        print(f'parsing ends at {curr_pos} (0x{curr_pos:x})')

        return curr_pos

    @staticmethod
    def parse_resource_data_file_data(data, offset=0, max_length=-1, is_encrypted=True):
        if is_encrypted:
            data = WindowsDefenderQuarantineFile.decrypt_data(data)

        end_of_data_pos = WindowsDefenderQuarantineFile.compute_end_position(
            data, offset=offset, max_length=max_length
        )

        data_length = end_of_data_pos - offset
        print(f'data length: {data_length} (0x{data_length:x})')
        print()

        curr_pos = offset

        header_length_fixed = 8 + 4 + 8

        if end_of_data_pos >= curr_pos + header_length_fixed:
            file_id = BytesUtility.extract_bytes(data, 0, 8, pos=curr_pos)
            binary_data_length = BytesUtility.extract_integer(data, 8, 4, pos=curr_pos, endian='little')
            padding_01 = BytesUtility.extract_bytes(data, 12, 8, pos=curr_pos)
            file_id_hex = HexDump.to_hex(file_id)
            padding_01_hex = HexDump.to_hex(padding_01)
            if file_id == WindowsDefenderQuarantineFile.resource_data_file_id:
                print(f'file id: {file_id_hex}')
            else:
                print(f'unknown file id: {file_id_hex}')
            print(f'binary data length: {binary_data_length} (0x{binary_data_length:x})')
            print(f'padding: {padding_01_hex}')
            print()
        else:
            return WindowsDefenderQuarantineFile.error_insufficient_data(
                data, header_length_fixed, pos=curr_pos
            )
        
        curr_pos += header_length_fixed

        if end_of_data_pos >= curr_pos + binary_data_length:
            binary_data = BytesUtility.extract_bytes(data, 0, binary_data_length, pos=curr_pos)
            binary_data_label = f'binary data at {curr_pos} (0x{curr_pos:x}):'
            HexDump.hexdump_and_print([binary_data], label_list=[binary_data_label],
                                      pos_label_list=[curr_pos])
        else:
            return WindowsDefenderQuarantineFile.error_insufficient_data(
                data, binary_data_length, pos=curr_pos
            )
        
        curr_pos += binary_data_length

        header_2_length_fixed = 8 + 8 + 4

        if end_of_data_pos >= curr_pos + header_2_length_fixed:
            padding_02 = BytesUtility.extract_bytes(data, 0, 8, pos=curr_pos)
            malware_file_length = BytesUtility.extract_integer(
                data, 8, 8, pos=curr_pos, endian='little'
            )
            padding_03 = BytesUtility.extract_bytes(data, 16, 4, pos=curr_pos)
            padding_02_hex = HexDump.to_hex(padding_02)
            padding_03_hex = HexDump.to_hex(padding_03)
            print(f'padding: {padding_02_hex}')
            print(f'malware file length: {malware_file_length} (0x{malware_file_length:x})')
            print(f'padding: {padding_03_hex}')
            print()
        else:
            return WindowsDefenderQuarantineFile.error_insufficient_data(
                data, header_2_length_fixed, pos=curr_pos
            )
        
        curr_pos += header_2_length_fixed

        if end_of_data_pos >= curr_pos + malware_file_length:
            malware_file_data = BytesUtility.extract_bytes(
                data, 0, malware_file_length, pos=curr_pos
            )
            malware_file_data_label = f'malware file data at {curr_pos} (0x{curr_pos:x}):'
            HexDump.hexdump_and_print([malware_file_data], label_list=[malware_file_data_label],
                                      pos_label_list=[curr_pos])
        else:
            return WindowsDefenderQuarantineFile.error_insufficient_data(
                data, malware_file_length, pos=curr_pos
            )
        
        curr_pos += malware_file_length

        remaining_data_length = end_of_data_pos - curr_pos
        remaining_data = BytesUtility.extract_bytes(data, 0, remaining_data_length, pos=curr_pos)
        remaining_data_label = f'remaining data at {curr_pos} (0x{curr_pos:x}):'
        HexDump.hexdump_and_print([remaining_data], label_list=[remaining_data_label],
                                  pos_label_list=[curr_pos])

        curr_pos += remaining_data_length

        print(f'parsing ends at {curr_pos} (0x{curr_pos:x})')

        return curr_pos

    @staticmethod
    def get_quarantine_file_list(dir_name=''):
        if dir_name == '':
            dir_name = WindowsDefenderQuarantineFile.default_main_folder
        entries_files = DirectoryUtility.list_files(
            os.path.join(dir_name, WindowsDefenderQuarantineFile.entries_sub_folder), '*',
            recursive=True
        )
        resources_files = DirectoryUtility.list_files(
            os.path.join(dir_name, WindowsDefenderQuarantineFile.resources_sub_folder), '*',
            recursive=True
        )
        resource_data_files = DirectoryUtility.list_files(
            os.path.join(dir_name, WindowsDefenderQuarantineFile.resource_data_sub_folder), '*',
            recursive=True
        )
        return entries_files, resources_files, resource_data_files
    
    # --- Internal Functions

    @staticmethod
    def get_cipher():
        # RC4 cipher needs to be created for the decryption of every data stream
        cipher = ARC4.new(bytes(WindowsDefenderQuarantineFile.decryption_key))
        return cipher

    @staticmethod
    def decrypt_data(data):
        cipher = WindowsDefenderQuarantineFile.get_cipher()
        decrypted_data = cipher.decrypt(data)
        return decrypted_data
    
    @staticmethod
    def decrypt_entries_file_data(data):
        required_length = WindowsDefenderQuarantineFile.entries_file_part_1_length
        data_length = len(data)
        if data_length < required_length:
            raise ValueError(f'insufficient data: length = {data_length}; required = {required_length}')
        
        encrypted_part_1_data = BytesUtility.extract_bytes(
            data, 0, WindowsDefenderQuarantineFile.entries_file_part_1_length, pos=0
        )
        decrypted_part_1_data = WindowsDefenderQuarantineFile.decrypt_data(encrypted_part_1_data)

        part_2_length, part_3_length = WindowsDefenderQuarantineFile.get_entries_file_parts_length(
            decrypted_part_1_data, is_encrypted=False
        )

        required_length = WindowsDefenderQuarantineFile.entries_file_part_1_length + \
            part_2_length + part_3_length
        data_length = len(data)
        if data_length < required_length:
            raise ValueError(f'insufficient data: length = {data_length}; required = {required_length}')

        part_2_offset = WindowsDefenderQuarantineFile.entries_file_part_1_length
        encrypted_part_2_data = BytesUtility.extract_bytes(data, part_2_offset, part_2_length, pos=0)
        decrypted_part_2_data = WindowsDefenderQuarantineFile.decrypt_data(encrypted_part_2_data)

        part_3_offset = part_2_offset + part_2_length
        encrypted_part_3_data = BytesUtility.extract_bytes(data, part_3_offset, part_3_length, pos=0)
        decrypted_part_3_data = WindowsDefenderQuarantineFile.decrypt_data(encrypted_part_3_data)

        encrypted_data_blocks = [
            encrypted_part_1_data, encrypted_part_2_data, encrypted_part_3_data,
        ]
        decrypted_data_blocks = [
            decrypted_part_1_data, decrypted_part_2_data, decrypted_part_3_data,
        ]
        pos_labels = [ 0, part_2_offset, part_3_offset, ]

        return encrypted_data_blocks, decrypted_data_blocks, pos_labels
    
    @staticmethod
    def get_entries_file_parts_length(part_1_data, is_encrypted=False):
        if is_encrypted:
            part_1_data = WindowsDefenderQuarantineFile.decrypt_data(part_1_data)
            
        required_length = WindowsDefenderQuarantineFile.entries_file_part_3_length_offset + 4
        data_length = len(part_1_data)
        if data_length < required_length:
            raise ValueError(f'insufficient data: length = {data_length}; required = {required_length}')
        
        part_2_length = BytesUtility.extract_integer(
            part_1_data,
            WindowsDefenderQuarantineFile.entries_file_part_2_length_offset, 4,
            endian='little'
        )
        part_3_length = BytesUtility.extract_integer(
            part_1_data,
            WindowsDefenderQuarantineFile.entries_file_part_3_length_offset, 4,
            endian='little'
        )

        return part_2_length, part_3_length
    
    @staticmethod
    def main_list_quarantine_files():
        parser = argparse.ArgumentParser(
            prog='list_quarantine_files',
            description='List Windows Defender Quarantine Files'
        )
        parser.add_argument('-d', '--directory', default='')
        args = parser.parse_args()
        kwargs = {
            'dir_name': args.directory,
        }
        entries_files, resources_files, resource_data_files = \
            WindowsDefenderQuarantineFile.get_quarantine_file_list(**kwargs)
        print(f'Entries Files:')
        if len(entries_files) <= 0:
            print(f'  no entries files')
        else:
            for file in entries_files:
                print(f'{  file}')
        print()
        print(f'Resources Files:')
        if len(resources_files) <= 0:
            print(f'  no resources files')
        else:
            for file in resources_files:
                print(f'  {file}')
        print()
        print(f'Resource Data Files:')
        if len(resource_data_files) <= 0:
            print(f'  no resource data files')
        else:
            for file in resource_data_files:
                print(f'  {file}')
        return
    
    @staticmethod
    def main():
        params = {
            'prog': 'parse_windows_defender_files',
            'description': 'Parse and list content of Windows Defender Files',
            'file_arg_name': 'defender_file',
            'file_arg_name_help': 'defender file to parse',
            'file_actions': {
                'parse': WindowsDefenderQuarantineFile.parse_entries_file_data,
                'parse_data': WindowsDefenderQuarantineFile.parse_resource_data_file_data,
                'parse_resource': WindowsDefenderQuarantineFile.parse_resources_file_data,
            }
        }
        FileFormat.main(params)
        return
    
if __name__ == '__main__':
    WindowsDefenderQuarantineFile.main_list_quarantine_files()

# --- end of file --- #

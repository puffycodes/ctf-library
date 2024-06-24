# file: usb_keystroke_decoder.py

class USBKeystrokeTable:

    # Keyboard encoding, ranges from 4 to 56.
    # 40 to 43 are 'Enter', 'ESC', 'DEL' and 'TAB'.
    # Table offset is 0.

    unshift_table_str = "::::abcdefghijklmnopqrstuvwxyz1234567890:::: -=[]\\#;'`,./"
    shift_table_str =   ';;;;ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*();;;; _+{}|~:"~<>?'

    unshift_table_offset = 0
    shift_table_offset = 0

    unshift_table_exclude_char = ':'
    shift_table_exclude_char = ';'

    # Numpad encoding, range from 84 to 99. 88 is 'Enter'.
    # Table offset is 84.

    numpad_table_str = '/*-+:1234567890.'
    numpad_table_offset = 84
    numpad_table_exclude_char = ':'

    # Special Key

    Key_Enter = 'Enter' # 40 & 88
    Key_Esc = 'Esc' # 41
    Key_Del = 'Del' # 42
    Key_Tab = 'Tab' # 43
    Key_CapsLock = 'CapsLock' # 57
    Key_RightArrow = 'RightArrow' # 79
    Key_LeftArrow = 'LeftArrow' # 80
    Key_DownArrow = 'DownArrow' # 81
    Key_UpArrow = 'UpArrow' # 82'

    special_key_table = {
        40: Key_Enter, 41: Key_Esc, 42: Key_Del, 43: Key_Tab,
        57: Key_CapsLock,
        79: Key_RightArrow, 80: Key_LeftArrow, 81: Key_DownArrow, 82: Key_UpArrow,
        88: Key_Enter,
    }

    special_key_list = {
        Key_Enter, Key_Esc, Key_Del, Key_Tab, Key_CapsLock,
        Key_RightArrow, Key_LeftArrow, Key_DownArrow, Key_UpArrow,
    }

    Key_Unknown = 'Unknown'

    def __init__(self):
        self.init_keystroke_table()
        return
    
    def init_keystroke_table(self):
        self.unshift_table = {}
        self.shift_table = {}

        self.expand_keystroke_table(
            self.unshift_table,
            USBKeystrokeTable.unshift_table_offset,
            USBKeystrokeTable.unshift_table_str,
            USBKeystrokeTable.unshift_table_exclude_char
        )
        self.expand_keystroke_table(
            self.unshift_table,
            USBKeystrokeTable.numpad_table_offset,
            USBKeystrokeTable.numpad_table_str,
            USBKeystrokeTable.numpad_table_exclude_char
        )

        self.expand_keystroke_table(
            self.shift_table,
            USBKeystrokeTable.shift_table_offset,
            USBKeystrokeTable.shift_table_str,
            USBKeystrokeTable.shift_table_exclude_char
        )
        self.expand_keystroke_table(
            self.shift_table,
            USBKeystrokeTable.numpad_table_offset,
            USBKeystrokeTable.numpad_table_str,
            USBKeystrokeTable.numpad_table_exclude_char
        )

        for key_code, key_value in self.special_key_table.items():
            self.unshift_table[key_code] = key_value
            self.shift_table[key_code] = key_value

        return
    
    def expand_keystroke_table(self, table, start_code, table_str, exclude_char):
        key_code = start_code
        for key_value in table_str:
            if key_value == exclude_char:
                # do not append key_value, just increase key_code
                key_code += 1
                continue
            table[key_code] = key_value
            key_code += 1
        return table
    
    def get_key_value(self, key_code, shift=False):
        key_value = USBKeystrokeTable.Key_Unknown
        if shift:
            # Shift
            if key_code in self.shift_table:
                key_value = self.shift_table[key_code]
        else:
            # Unshift
            if key_code in self.unshift_table:
                key_value = self.unshift_table[key_code]
        return key_value
    
    def is_special_key_value(self, key_value):
        return key_value in USBKeystrokeTable.special_key_list

class USBKeystrokeDecoder:
    
    def __init__(self):
        # Keyboard encoding, ranges from 4 to 56.
        # 40 to 43 are 'Enter', 'ESC', 'DEL' and 'TAB'.
        # Table offset is 0.
        self.unshift_table = USBKeystrokeTable.unshift_table_str
        self.shift_table = USBKeystrokeTable.shift_table_str

        # Numpad encoding, range from 84 to 99. 88 is 'Enter'.
        # Table offset is 84.
        self.numpad_table = USBKeystrokeTable.numpad_table_str

        self.keystroke_table = USBKeystrokeTable()
        return

    # Ref: USBPcap Capture format specification
    #      (https://desowin.org/usbpcap/captureformat.html)
    def iterate_packets(self, packets, start_count=1, verbose=False):
        # Wireshark packet numbering starts from 1
        packet_count = start_count

        for p in packets:
            # Check whether packet is raw data
            try:
                packet_payload = p.load
            except AttributeError as e:
                packet_count += 1
                continue

            # Do not process packet that pseudo header length is not 27 (0x1b00)
            pseudo_header_length = packet_payload[0:2]
            if pseudo_header_length != b'\x1b\x00':
                packet_count += 1
                continue

            # IRP ID does not matter?
            # irp_id = packet_payload[2:10]
            # if irp_id != b'\xa0\x49\x4f\x70\x07\x85\xff\xff':
            #     print(f'IRP ID: {irp_id}')

            # Do not process packet that is not URB_INTERRUPT (0x01)
            if packet_payload[22] != 0x01:
                packet_count += 1
                continue

            # Length of Leftover Capture Data
            data_length_bytes = packet_payload[23:27]
            data_length = int.from_bytes(data_length_bytes, 'little')

            if verbose:
                keystroke_data = packet_payload[27:27+data_length]
                print(f'length: {data_length_bytes} -> {data_length}: {keystroke_data}')
            
            # Do not process packet that is empty
            if data_length <= 0:
                packet_count += 1
                continue

            # Only process packet with data length == 8
            if data_length != 8:
                packet_count += 1
                continue

            yield (packet_count, p, data_length)
            packet_count += 1
        
        return
    
    def decode_packets_2(self, packets, verbose=False, debug=False):
        result = []
        caps_lock = False

        for p_count, p, data_length in self.iterate_packets(packets):
            modifier = p.load[27]
            key_code = p.load[29]

            if key_code == 0:
                # ignore key_code 0
                if debug:
                    self.show_unknown_key_code(
                        p_count, modifier, key_code, 'no key code'
                    )
                continue

            shift = caps_lock
            if modifier == 0:
                shift = caps_lock
            elif modifier == 2 or modifier == 0x20:
                shift = not caps_lock
            else:
                # Unknown/unimplemented modifier
                self.show_unknown_key_code(p_count, modifier, key_code)
                continue

            key_value = self.keystroke_table.get_key_value(key_code, shift)
            if key_value == USBKeystrokeTable.Key_Unknown:
                self.show_unknown_key_code(p_count, modifier, key_code)
                # do not send unknown key to next stage
                continue
            elif key_value == USBKeystrokeTable.Key_CapsLock:
                caps_lock = not caps_lock
                if verbose:
                    self.show_known_key_code(
                        p_count, modifier, key_code, key_value,
                        info=f'CapsLock: {caps_lock}'
                    )
                # send CapsLock to next stage
                #continue

            result.append(key_value)
            if verbose:
                self.show_known_key_code(p_count, modifier, key_code, key_value)

        return result
    
    def show_unknown_key_code(self,
                              packet_id, modifier, key_code,
                              reason='unknown key'):
        print(f'{packet_id}: {reason}: modifier={modifier}, key_code={key_code}')
        return
    
    def show_known_key_code(self,
                            packet_id, modifier, key_code, key_value,
                            info=''):
        print(f'{packet_id}: {key_value} ({modifier}, {key_code}) {info}')
        return
    
    def decode_packets(self, packets, verbose=False, debug=False):
        result = []

        value_list = []
        value_ptr = 0
        caps_lock = False
        
        # # TODO: This is here because of some old code below.
        # value_str = ''

        for p_count, p, data_length in self.iterate_packets(packets):
            #modifier = p.load[-8]
            #key = p.load[-6]
            modifier = p.load[27]
            key = p.load[29]
            #print(p.load[-8:-4])
            if debug:
                print(f' - {p_count}: {modifier} {key}')

            if key == 0:
                continue

            if key == 40 or key == 88:
                # Enter
                curr_result = ''.join(value_list)
                result.append(curr_result)
                print(f'line: {curr_result}')
                value_list = []
                value_ptr = 0
            elif key == 41:
                # ESC
                pass
            elif key == 42:
                # Del
                # TODO: Is this correct?
                value_list.pop(value_ptr - 1)
                value_ptr -= 1
                pass
            elif key == 43:
                # Tab
                value_list.insert(value_ptr, '\t')
                value_ptr += 1
                pass
            elif key == 57:
                # Caps Lock
                # TODO: Is this correct?
                caps_lock = not caps_lock
                pass
            elif key == 79:
                # Right Arrow
                value_ptr += 1
            elif key == 80:
                # Left Arrow
                value_ptr -= 1
            elif key == 81: # 0x51
                # Down Arrow
                print(p_count, modifier, key, 'down arrow not implemented')
            elif key == 82: # 0x52
                # Up Arrow
                print(p_count, modifier, key, 'up arrow not implemented')

            elif key >= 84 and key <= 99:
                if modifier == 0 or modifier == 2:
                    char_value = self.numpad_table[key-84]
                    if char_value == ':':
                        print(p_count, modifier, key)
                    value_list.insert(value_ptr, char_value)
                    value_ptr += 1
                else:
                    print(p_count, modifier, key)

            else:
                # TODO: Should take into consideration caps_lock
                if modifier != 0:
                    if modifier == 2 or modifier == 0x20:
                        if key != 0:
                            if key < len(self.shift_table):
                                char_value = self.shift_table[key]
                                if char_value == ';':
                                    print(p_count, modifier, key)
                                value_list.insert(value_ptr, char_value)
                                value_ptr += 1
                            else:
                                print(p_count, modifier, key)
                    else:
                        print(p_count, modifier, key)
                else:
                    if key < len(self.unshift_table):
                        char_value = self.unshift_table[key]
                        if char_value == ':':
                            print(p_count, modifier, key)
                        value_list.insert(value_ptr, char_value)
                        value_ptr += 1
                    else:
                        if key != 0:
                            print(p_count, modifier, key)
                            # # TODO: Find out what is this doing.
                            # #       Some reminant of an older version of code?
                            # value_str = value_str + '_'

        # Remaining, if any
        if len(value_list) > 0:
            curr_result = ''.join(value_list)
            result.append(curr_result)
            print(f'line: {curr_result}')
            
        return result
    
if __name__ == '__main__':
    print('usage:')
    print('>>> from usb_keystroke_decoder import USBKeystrokeDecoder')
    print('>>> decoder = USBKeystrokeDecoder()')
    print('>>> decoder.decode_packets(packets_from_pcap)')

# --- end of file --- #

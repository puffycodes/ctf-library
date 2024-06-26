# file: usb_keystroke_decoder.py

class USBKeyboard:
    # Shift will flip caps lock
    Keyboard_Type_1 = 1
    # Shift is independent of caps lock
    Keyboard_Type_2 = 2

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

    # Simple class to gather keystroke as a list and return the resulted list.
    class KeystrokeList:

        def __init__(self):
            self.key_value_list = []
            return
        
        def process_key_value(self, key_value):
            self.key_value_list.append(key_value)
            return
        
        def get_result(self):
            return self.key_value_list
        
        def get_text(self):
            return ''.join(self.key_value_list)

    # A class to gather keystroke as they will appear as typed in an editor.
    class KeystrokeToText:

        def __init__(self):
            self.text_buffer = []
            self.line_ptr = 0
            self.column_ptr = 0
            self.expand_text_buffer()
            return
    
        def process_key_value(self, key_value):
            if key_value == USBKeystrokeTable.Key_Enter:
                self.line_ptr += 1
                self.expand_text_buffer()
                self.column_ptr = min(
                    self.column_ptr,
                    len(self.text_buffer[self.line_ptr])
                )
            elif key_value == USBKeystrokeTable.Key_Esc:
                pass
            elif key_value == USBKeystrokeTable.Key_Del:
                self.text_buffer[self.line_ptr].pop(self.column_ptr - 1)
                self.column_ptr -= 1
            elif key_value == USBKeystrokeTable.Key_Tab:
                self.text_buffer[self.column_ptr].insert(self.column_ptr, '\t')
                self.column_ptr += 1
            elif key_value == USBKeystrokeTable.Key_CapsLock:
                pass
            elif key_value == USBKeystrokeTable.Key_RightArrow:
                self.column_ptr += 1
                if self.column_ptr > len(self.text_buffer[self.line_ptr]):
                    self.column_ptr = len(self.text_buffer[self.line_ptr])
            elif key_value == USBKeystrokeTable.Key_LeftArrow:
                self.column_ptr -= 1
                if self.column_ptr < 0:
                    self.column_ptr = 0
            elif key_value == USBKeystrokeTable.Key_DownArrow:
                self.line_ptr += 1
                self.expand_text_buffer()
                self.column_ptr = min(
                    self.column_ptr,
                    len(self.text_buffer[self.line_ptr])
                )
            elif key_value == USBKeystrokeTable.Key_UpArrow:
                self.line_ptr -= 1
                if self.line_ptr < 0:
                    self.line_ptr = 0
                self.column_ptr = min(
                    self.column_ptr,
                    len(self.text_buffer[self.line_ptr])
                )
            else:
                self.text_buffer[self.line_ptr].insert(self.column_ptr, key_value)
                self.column_ptr += 1
            return
        
        def get_result(self):
            return self.text_buffer
        
        def get_text(self):
            lines = [''.join(line) for line in self.text_buffer]
            text = '\n'.join(lines)
            return text
        
        def expand_text_buffer(self):
            while self.line_ptr >= len(self.text_buffer):
                self.text_buffer.append([])
            return

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

            # Extract modifier and key code
            modifier = packet_payload[27]
            key_code = packet_payload[29]

            yield (packet_count, p, modifier, key_code)
            packet_count += 1
        
        return
    
    def decode_packets(self, packets, keystroke_processor=None,
                       keyboard_type=USBKeyboard.Keyboard_Type_1,
                       verbose=False, debug=False):
        if keystroke_processor == None:
            keystroke_processor = USBKeystrokeDecoder.KeystrokeToText()

        caps_lock = False

        for packet_id, packet, modifier, key_code in self.iterate_packets(packets):
            if key_code == 0:
                # ignore key_code 0
                if debug:
                    self.show_unknown_key_code(
                        packet_id, modifier, key_code, f'key code is zero'
                    )
                continue

            shift = caps_lock
            if modifier == 0:
                # Shift Key is not pressed
                if key_code >= 4 and key_code <= 29:
                    # caps lock only apply to key_code 'a' to 'z'
                    shift = caps_lock
                else:
                    shift = False
            elif modifier == 2 or modifier == 0x20:
                # Shift Key is pressed
                if keyboard_type == USBKeyboard.Keyboard_Type_1:
                    # Type 1: shift flip the caps_lock
                    # E.g. Windows keyboard
                    # TODO: check whether does flipping apply to key_code 'a' to 'z' only?
                    # TODO: and whether caps lock apply to number/symbol keys?
                    if key_code >= 4 and key_code <= 29:
                        shift = not caps_lock
                    else:
                        shift = True
                elif keyboard_type == USBKeyboard.Keyboard_Type_2:
                    # Type 2: shift is alway shift, regardless of caps_lock
                    # E.g. Apple keyboard
                    shift = True
                else:
                    # Default
                    shift = True
            else:
                # Unknown/unimplemented modifier
                self.show_unknown_key_code(
                    packet_id, modifier, key_code, f'unknown modifier'
                )
                continue

            key_value = self.keystroke_table.get_key_value(key_code, shift)
            if key_value == USBKeystrokeTable.Key_Unknown:
                self.show_unknown_key_code(
                    packet_id, modifier, key_code, f'unknown key code'
                )
                # do not send unknown key to next stage
                continue
            elif key_value == USBKeystrokeTable.Key_CapsLock:
                caps_lock = not caps_lock
                if verbose:
                    self.show_known_key_code(
                        packet_id, modifier, key_code, key_value,
                        info=f'CapsLock: {caps_lock}'
                    )
                # CapsLock will be send to next stage
                #continue
            else:
                if verbose:
                    self.show_known_key_code(
                        packet_id, modifier, key_code, key_value
                    )

            # send key to keystroke processor
            keystroke_processor.process_key_value(key_value)

        return keystroke_processor
    
    def show_unknown_key_code(self,
                              packet_id, modifier, key_code,
                              reason='unknown key code'):
        print(f'{packet_id}: {reason}: modifier={modifier}, key_code={key_code}')
        return
    
    def show_known_key_code(self,
                            packet_id, modifier, key_code, key_value,
                            info=''):
        print(f'{packet_id}: {key_value} ({modifier}, {key_code}) {info}')
        return
    
    def decode_packets_old(self, packets, verbose=False, debug=False):
        result = []

        value_list = []
        value_ptr = 0
        caps_lock = False
        
        # # TODO: This is here because of some old code below.
        # value_str = ''

        for packet_id, packet, modifier, key_code in self.iterate_packets(packets):
            # #modifier = packet.load[-8]
            # #key = packet.load[-6]
            # modifier = packet.load[27]
            # key = packet.load[29]
            # #print(packet.load[-8:-4])
            if debug:
                print(f' - {packet_id}: {modifier} {key_code}')

            if key_code == 0:
                continue

            if key_code == 40 or key_code == 88:
                # Enter
                curr_result = ''.join(value_list)
                result.append(curr_result)
                print(f'line: {curr_result}')
                value_list = []
                value_ptr = 0
            elif key_code == 41:
                # ESC
                pass
            elif key_code == 42:
                # Del
                # TODO: Is this correct?
                value_list.pop(value_ptr - 1)
                value_ptr -= 1
                pass
            elif key_code == 43:
                # Tab
                value_list.insert(value_ptr, '\t')
                value_ptr += 1
                pass
            elif key_code == 57:
                # Caps Lock
                # TODO: Is this correct?
                caps_lock = not caps_lock
                pass
            elif key_code == 79:
                # Right Arrow
                value_ptr += 1
            elif key_code == 80:
                # Left Arrow
                value_ptr -= 1
            elif key_code == 81: # 0x51
                # Down Arrow
                print(packet_id, modifier, key_code, 'down arrow not implemented')
            elif key_code == 82: # 0x52
                # Up Arrow
                print(packet_id, modifier, key_code, 'up arrow not implemented')

            elif key_code >= 84 and key_code <= 99:
                if modifier == 0 or modifier == 2:
                    char_value = self.numpad_table[key_code-84]
                    if char_value == ':':
                        print(packet_id, modifier, key_code)
                    value_list.insert(value_ptr, char_value)
                    value_ptr += 1
                else:
                    print(packet_id, modifier, key_code)

            else:
                # TODO: Should take into consideration caps_lock
                if modifier != 0:
                    if modifier == 2 or modifier == 0x20:
                        if key_code != 0:
                            if key_code < len(self.shift_table):
                                char_value = self.shift_table[key_code]
                                if char_value == ';':
                                    print(packet_id, modifier, key_code)
                                value_list.insert(value_ptr, char_value)
                                value_ptr += 1
                            else:
                                print(packet_id, modifier, key_code)
                    else:
                        print(packet_id, modifier, key_code)
                else:
                    if key_code < len(self.unshift_table):
                        char_value = self.unshift_table[key_code]
                        if char_value == ':':
                            print(packet_id, modifier, key_code)
                        value_list.insert(value_ptr, char_value)
                        value_ptr += 1
                    else:
                        if key_code != 0:
                            print(packet_id, modifier, key_code)
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

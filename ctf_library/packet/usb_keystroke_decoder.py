# file: usb_keystroke_decoder.py

class USBKeystrokeDecoder:
    
    def __init__(self):
        self.unshift_table = "::::abcdefghijklmnopqrstuvwxyz1234567890:::: -=[]\\#;'`,./"
        self.shift_table =   ';;;;ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*();;;; _+{}|~:"~<>?'
        return

    # Ref: USBPcap Capture format specification
    #      (https://desowin.org/usbpcap/captureformat.html)
    def iterate_packets(self, packets, verbose=False):
        # Wireshark packet numbering starts from 1
        packet_count = 1

        for p in packets:
            # Do not process packet that pseudo header length is not 27 (0x1b00)
            pseudoheader_length = p.load[0:2]
            if pseudoheader_length != b'\x1b\x00':
                packet_count += 1
                continue

            # IRP ID does not matter?
            # irp_id = p.load[2:10]
            # if irp_id != b'\xa0\x49\x4f\x70\x07\x85\xff\xff':
            #     print(f'IRP ID: {irp_id}')

            # Do not process packet that is not URB_INTERRUPT (0x01)
            if p.load[22] != 0x01:
                packet_count += 1
                continue

            # Length of Leftover Capture Data
            data_length_bytes = p.load[23:27]
            data_length = int.from_bytes(data_length_bytes, 'little')

            if verbose:
                print(f'length: {data_length_bytes} -> {data_length}: {p.load[27:27+data_length]}')
            
            # Do not process packet that is empty
            if data_length <= 0:
                packet_count += 1
                continue

            yield (packet_count, p, data_length)
            packet_count += 1
        
        return
    
    def decode_packets(self, packets):
        result = []

        value_list = []
        value_ptr = 0
        caps_lock = False
        
        # TODO: This is here because of some old code below.
        value_str = ''

        for p_count, p, data_length in self.iterate_packets(packets):
            #modifier = p.load[-8]
            #key = p.load[-6]
            modifier = p.load[27]
            key = p.load[29]
            #print(p.load[-8:-4])

            if key == 0:
                continue

            if key == 40:
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
            elif key ==82: # 0x52
                # Up Arrow
                print(p_count, modifier, key, 'up arrow not implemented')

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
                            # TODO: Find out what is this doing.
                            #       Some reminant of an older version of code?
                            value_str = value_str + '_'

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

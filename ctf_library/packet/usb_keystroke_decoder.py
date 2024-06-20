# file: usb_keystroke_decoder.py

class USBKeystrokeDecoder:
    
    def __init__(self):
        self.unshift_table = "::::abcdefghijklmnopqrstuvwxyz1234567890:::: -=[]\\#;'`,./"
        self.shift_table =   ';;;;ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*();;;; _+{}|~:"~<>?'
        return
    
    def decode_packets(self, packets):
        value_list = []
        value_ptr = 0
        caps_lock = False
        
        # TODO: This is here because of some old code below.
        value_str = ''

        for p in packets:
            modifier = p.load[-8]
            key = p.load[-6]
            #print(p.load[-8:-4])

            if key == 0:
                continue

            if key == 40:
                # Enter
                print(''.join(value_list))
                value_list = []
                value_ptr = 0
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

            else:
                # TODO: Should take into consideration caps_lock
                if modifier != 0:
                    if modifier == 2 or modifier == 0x20:
                        if key != 0:
                            if key < len(self.shift_table):
                                char_value = self.shift_table[key]
                                if char_value == ';':
                                    print(modifier, key)
                                value_list.insert(value_ptr, char_value)
                                value_ptr += 1
                            else:
                                print(modifier, key)
                    else:
                        print(modifier, key)
                else:
                    if key < len(self.unshift_table):
                        char_value = self.unshift_table[key]
                        if char_value == ':':
                            print(modifier, key)
                        value_list.insert(value_ptr, char_value)
                        value_ptr += 1
                    else:
                        if key != 0:
                            print(modifier, key)
                            # TODO: Find out what is this doing.
                            #       Some reminant of an older version of code?
                            value_str = value_str + '_'

        if len(value_list) > 0:
            print(''.join(value_list))
            
        return
    
if __name__ == '__main__':
    print('usage:')
    print('>>> from usb_keystroke_decoder import USBKeystrokeDecoder')
    print('>>> decoder = USBKeystrokeDecoder()')
    print('>>> decoder.decode_packets(packets_from_pcap)')

# --- end of file --- #
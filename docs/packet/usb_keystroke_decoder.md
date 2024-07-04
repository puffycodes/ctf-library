# Documentation for USB Keystroke Decoder

## Features of the Decoder

1. Extract and decode relevant packets directly from an unfiltered list of packets.
1. Decode keys with combinations of Shift and CapsLock keys.
1. Decode Left, Right, Up and Down Arrow keys.
1. Decode NumPad keys.

## Usage

```
from scapy.all import *
from ctf_library.packet.usb_keystroke_decoder import USBKeystrokeDecoder

decoder = USBKeystrokeDecoder()
packets = rdpcap('my_keystroke_file.pcap')
result = decoder.decode_packets(packets)
print(f'result is:\n{result.get_text()}')
```

## References on USB Pcap Captures

1. [Wireshark Sample Captures](https://wiki.wireshark.org/SampleCaptures)
1. [USBPcap Capture format specification](https://desowin.org/usbpcap/captureformat.html)

## References on Decoding USB Pcap Captures

1. [kaizen-ctf 2018 — Reverse Engineer usb keystrok from pcap file](https://abawazeeer.medium.com/kaizen-ctf-2018-reverse-engineer-usb-keystrok-from-pcap-file-2412351679f4)
1. [Decoding Mixed Case USB Keystrokes from PCAP](https://blog.stayontarget.org/2019/03/decoding-mixed-case-usb-keystrokes-from.html)
1. [HackTheBox.eu Deadly Arthropod Write-Up](https://github.com/tanc7/HacktheBox_Deadly_Arthropod_Writeup/tree/master)
    - Sample: [deadly_arthropod.pcap](https://github.com/tanc7/HacktheBox_Deadly_Arthropod_Writeup/blob/master/deadly_arthropod.pcap) (Sample contains captures of Left and Right Arrow)
1. [USB Keyboard packet capture analysis](https://naykisec.github.io/USB-Keyboard-packet-capture-analysis/)
    - Sample: [task.pcap](https://0xd13a.github.io/ctfs/hackit2017/foren100/task.pcap) (Sample contains captures of Up and Down Arrow)

## A Note on Keyboard Types

There are differences between keyboards for the combinations of Shift and CapsLock keys. (Not sure if this will translate to a difference in USB keystroke captures.)

Type 1 keyboards are found on Windows OS. Type 2 keyboards are found on MacOS.

The decoder accepts a parameter (keyboard_type) to switch between the two keyboard types.

The tables below show the differences between the keyboards.

Type 1 Keyboard:

```
Shift CapsLock
----- --------
 no     no      asdfghjkl 1234567890-=` ;',./[]\
 yes    no      ASDFGHJKL !@#$%^&*()_+~ :"<>?{}|
 no     yes     ASDFGHJKL 1234567890-=` ;',./[]\
 yes    yes     asdfghjkl !@#$%^&*()_+~ :"<>?{}|    (Different from Type 2)
```

Type 2 Keyboard:

```
Shift CapsLock
----- --------
 no     no      asdfghjkl 1234567890-=` ;',./[]\
 yes    no      ASDFGHJKL !@#$%^&*()_+~ :"<>?{}|
 no     yes     ASDFGHJKL 1234567890-=` ;',./[]\
 yes    yes     ASDFGHJKL !@#$%^&*()_+~ :"<>?{}|   (Different from Type 1)
```

***

*Updated on 28 June 2024*

# Documentation for USB Keystroke Decoder

## References on USB Pcap Captures

1. [Wireshark Sample Captures](https://wiki.wireshark.org/SampleCaptures)
1. [USBPcap Capture format specification](https://desowin.org/usbpcap/captureformat.html)

## References on Decoding USB Pcap Captures

1. [kaizen-ctf 2018 — Reverse Engineer usb keystrok from pcap file](https://abawazeeer.medium.com/kaizen-ctf-2018-reverse-engineer-usb-keystrok-from-pcap-file-2412351679f4)
1. [Decoding Mixed Case USB Keystrokes from PCAP](https://blog.stayontarget.org/2019/03/decoding-mixed-case-usb-keystrokes-from.html)
1. [HackTheBox.eu Deadly Arthropod Write-Up](https://github.com/tanc7/HacktheBox_Deadly_Arthropod_Writeup/tree/master)
    - Sample: [deadly_arthropod.pcap](https://github.com/tanc7/HacktheBox_Deadly_Arthropod_Writeup/blob/master/deadly_arthropod.pcap) (Sample captures Left and Right Arrow)
1. [USB Keyboard packet capture analysis](https://naykisec.github.io/USB-Keyboard-packet-capture-analysis/)
    - Sample: [task.pcap](https://0xd13a.github.io/ctfs/hackit2017/foren100/task.pcap) (Sample captures Up and Down Arrow)

## Keyboard Types

Type 1 Keyboard:

```
Shift CapsLock
----- --------
 no     no      asdfghjkl 1234567890-=` ;',./[]\
 yes    no      ASDFGHJKL !@#$%^&*()_+~ :"<>?{}|
 no     yes     ASDFGHJKL 1234567890-=` ;',./[]\
 yes    yes     asdfghjkl !@#$%^&*()_+~ :"<>?{}|
```

Type 2 Keyboard:

```
Shift CapsLock
----- --------
 no     no      asdfghjkl 1234567890-=` ;',./[]\
 yes    no      ASDFGHJKL !@#$%^&*()_+~ :"<>?{}|
 no     yes     ASDFGHJKL 1234567890-=` ;',./[]\
 yes    yes     ASDFGHJKL !@#$%^&*()_+~ :"<>?{}|
```

***

*Updated on 28 June 2024*

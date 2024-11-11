# Installation of AutoRecon

## Install AutoRecon

Set up a virtual environment:
```
$ mkdir autorecon
$ cd autorecon
$ python -m virtualenv -p python3 .
$ source bin/activate
(autorecon) $ pip install autorecon
```

Install from Git instead of PyPI:
```
(autorecon) $ python3 -m pip install git+https://github.com/Tib3rius/AutoRecon.git
```

## Install Tools on Kali Linux

```
(autorecon) $ sudo apt install seclists curl dnsrecon enum4linux feroxbuster gobuster impacket-scripts nbtscan nikto nmap onesixtyone oscanner redis-tools smbclient smbmap snmp sslscan sipvicious tnscmd10g whatweb wkhtmltopdf
```

## Install Tools on Ubuntu

Install virtualenv:
```
$ sudo apt install python3-virtualenv
```

Using apt:
```
(autorecon) $ sudo apt install curl dnsrecon gobuster nbtscan nikto nmap onesixtyone redis-tools smbclient smbmap sslscan whatweb wkhtmltopdf
```

Using snap:
```
(autorecon) $ snap install seclists enum4linux feroxbuster
```

TODO: No such  on apt or snap
```
impacket-scripts oscanner snmpwalk svwar tnscmd10g
```

```
(autorecon) $ git clone https://gitlab.com/kalilinux/packages/oscanner.git
```

## Install Tools on MacOS

1. SecLists:

    Small:
    ```
    (autorecon) $ git clone --depth 1 https://github.com/danielmiessler/SecLists.git
    ```

    Complete:
    ```
    (autorecon) $ git clone https://github.com/danielmiessler/SecLists.git
    ```

1. curl:

    Already installed? Test with:
    ```
    (autorecon) $ curl -V
    ```

1. feroxbuster:
    ```
    (autorecon) $ brew install feroxbuster
    ```

1. dnsrecon:
    ```
    (autorecon) $ pip install dnsrecon
    ```

1. enum4linux:
    ```
    ???
    ```

1. ...

## Links to AutoRecon and Tools

1. Repositories of [AutoRecon and Tools](index.md#auto-scanning-tools)

***
*Updated on 7 November 2024*

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

## Install Tools on Kali Linux

```
(autorecon) $ sudo apt install seclists curl dnsrecon enum4linux feroxbuster gobuster impacket-scripts nbtscan nikto nmap onesixtyone oscanner redis-tools smbclient smbmap snmp sslscan sipvicious tnscmd10g whatweb wkhtmltopdf
```

## Install Tools on MacOS

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

1. [AutoRecon and Tools](index.md#auto-scanning-tools)

***
*Updated on 7 November 2024*

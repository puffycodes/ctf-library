# AutoRecon

## Resources

1. [AutoRecon](https://github.com/Tib3rius/AutoRecon)

## Tools used by AutoRecon

1. [SecLists Project](https://github.com/danielmiessler/SecLists)
1. [curl](https://curl.se/)
1. [feroxbuster](https://github.com/epi052/feroxbuster)
1. [dnsrecon](https://github.com/darkoperator/dnsrecon)
1. [enum4linux](https://github.com/CiscoCXSecurity/enum4linux)
1. [gobuster](https://github.com/OJ/gobuster)
1. ...

# Installation of AutoRecon

## Install AutoRecon

Set up a virtual environment:
```
$ mkdir autorecon
$ cd autorecon
$ python -m virtualenv -p python3 .
$ source bin/activate
```

Install from PyPI:
```
(autorecon) $ pip install autorecon
```

Install from Git instead of PyPI:
```
(autorecon) $ python3 -m pip install git+https://github.com/Tib3rius/AutoRecon.git
```

# Installation of Tools used by AutoRecon

## Install Tools on Kali Linux

```
(autorecon) $ sudo apt install seclists curl dnsrecon enum4linux feroxbuster gobuster impacket-scripts nbtscan nikto nmap onesixtyone oscanner redis-tools smbclient smbmap snmp sslscan sipvicious tnscmd10g whatweb wkhtmltopdf
```

## Install Tools on Ubuntu

### Pre-requisites:

Install Pip and Python virtualenv:
```
$ sudo apt install python3-pip python3-virtualenv
```

Install Java:
```
$ sudo apt install default-jre
```

Install Snap:
```
$ sudo apt install snapd
```

***

### Installation of Tools

Tools installed using apt:
```
$ sudo apt install curl dnsrecon gobuster nbtscan nikto nmap onesixtyone redis-tools smbclient smbmap snmp sslscan sipvicious whatweb wkhtmltopdf
```

Tools installed using snap:
```
$ snap install seclists enum4linux feroxbuster
```

Tools that does not have a package on apt or snap (TODO)
```
impacket-scripts oscanner tnscmd10g
```

Missing Commands at this point:
```
oscanner tnscmd10g
```

Git Repositories:
- oscanner needs Java.
```
$ git clone https://gitlab.com/kalilinux/packages/impacket-scripts.git
$ git clone https://gitlab.com/kalilinux/packages/oscanner.git
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

***
*Updated on 17 December 2024*

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

[Kali Source Packages](https://gitlab.com/kalilinux/packages)

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

Obtain seclists from Git Repository:
```
$ git clone --depth 1 https://github.com/danielmiessler/SecLists.git
$ ln ./SecLists /usr/share/seclists
```

[Download and install enum4linux](https://labs.portcullis.co.uk/tools/enum4linux/):
```
$ curl -sLO https://labs.portcullis.co.uk/download/enum4linux-0.8.9.tar.gz
$ tar -xvzf enum4linux-0.8.9.tar.gz
$ ln ./enum4linux-0.8.9/enum4linux.pl /usr/bin/enum4linux.pl
$ ln ./enum4linux-0.8.9/enum4linux.pl /usr/bin/enum4linux
```

[Install feroxbuster from .deb download](https://epi052.github.io/feroxbuster-docs/docs/installation/):

```
$ curl -sLO https://github.com/epi052/feroxbuster/releases/latest/download/feroxbuster_amd64.deb.zip
$ unzip feroxbuster_amd64.deb.zip
$ sudo apt install ./feroxbuster_*_amd64.deb
```

Tools that does not have a package on apt or snap (TODO)
```
impacket-scripts oscanner tnscmd10g
```

Missing Commands at this point:
```
oscanner tnscmd10g
```

Get impacket-scripts from Git Repositories:
- needs python3-impacket
- TODO: how to install?
```
$ sudo apt install python3-impacket
$ git clone https://gitlab.com/kalilinux/packages/impacket-scripts.git
```

Get oscanner from Git Repositories:
- oscanner needs Java.
```
$ git clone https://gitlab.com/kalilinux/packages/oscanner.git
ln -vs ./oscanner /usr/share/oscanner
ln -vs ./oscanner/debian/helper-script/oscanner /usr/bin/oscanner
```

Install tnscmd10g from Git Repositories:
```
$ git clone https://github.com/hacktrackgnulinux/tnscmd10g.git
chmod +x ./tnscmd10g/tnscmd10g.pl
ln -vs ./tnscmd10g/tnscmd10g.pl /usr/bin/tnscmd10g.pl
ln -vs ./tnscmd10g/tnscmd10g.pl /usr/bin/tnscmd10g
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
*Updated on 19 December 2024*

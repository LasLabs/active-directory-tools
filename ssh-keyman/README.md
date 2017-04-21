[![License: Apache 2.0](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0.html)

SSH Key Manager
===============

This repo provides two scripts to manage your own SSH keys in Active Directory
provided that you follow [this blog post](https://blog.laslabs.com/2016/08/storing-ssh-keys-in-active-directory/)
and [this other blog post](https://blog.laslabs.com/2017/04/managing-ssh-keys-stored-in-active-directory/).

Usage
=====

OS X & Linux
-------------
Install `python-ldap` as it is a requirement
```
pip install python-ldap
```

Now run the script and enter config info and your log in info, keeping in mind
that your username should be your userPrincipleName ($username@corp.example.com)

```
$ python ssh-keyman.py
```

Config items you will be asked for will be stored in ~/.ssh-keyman. The can be
cleared later on by using the --clear switch.

```
LDAP Server URI - The AD Server IP or FQDN
BASE DN - The top level OU where your user is located
SSH Key Attribute Name - The name of the attribute that holds your SSH keys in AD
```


Windows
-------
This script requires an Administrator PowerShell prompt to execute. Please note
that it will run under whatever user you are logged in as.

Run the script
```
.\ssh-keyman.ps
```
and provide the SSH Key Attribute name, SSH Host and key to be added.


Contributors
============

* Ted Salmon <tsalmon@laslabs.com>

Maintainer
==========

[![LasLabs Inc.](https://laslabs.com/logo.png)](https://laslabs.com)

This module is maintained by [LasLabs Inc.](https://laslabs.com)

* https://repo.laslabs.com/projects/DEP/repos/ansible-base/

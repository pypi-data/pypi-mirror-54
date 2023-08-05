# Python-DDNS

[![Build Status](https://travis-ci.com/jwhite1st/python-ddns.svg?branch=master)](https://travis-ci.com/jwhite1st/python-ddns) [![GitHub license](https://img.shields.io/github/license/jwhite1st/python-ddns?style=flat-square)](https://github.com/jwhite1st/python-ddns/blob/master/LICENSE.md)  
![GitHub last commit](https://img.shields.io/github/last-commit/jwhite1st/python-ddns)![GitHub issues](https://img.shields.io/github/issues-raw/jwhite1st/python-ddns)

![PyPI](https://img.shields.io/pypi/v/Python-DDNS)

This is program written in python that acts as a DDNS client, currently just for Cloudflare.  
Works on python3 and up.  

I plan on making it a ppa to have it easier to update.

## Git Install

```bash
git clone https://github.com/jwhite1st/python-ddns
cd python-ddns/
pip install -r requirements
# Modify config.conf with the require fields.
# To test configuration
python3 python-ddns.py
# Edit crontab to run script
crontab -e
# Add
0 * * * * /usr/bin/python3 $PWD/python-ddns.py >/dev/null 2>&1 #Updates every hour.
```

## Python Install

There is a package available on [pypi](https://pypi.org/project/Python-DDNS/) if you would rather install it that way.

```bash
pip install python-ddns
#Modify the config file. To find where it is install use pip show -f python-ddns
# Edit crontab to run script
crontab -e
# Add
0 * * * * /usr/bin/python-ddns >/dev/null 2>&1 #Updates every hour.
```

### TODO

- Easier config editing
- Better service functionality
- Other DNS systems supported

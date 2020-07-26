# 🍺 Dirscan ![Stage](https://img.shields.io/badge/Release-STABLE-brightgreen.svg)  [![Python 3.7](https://img.shields.io/badge/Python-3.7-yellow.svg)](http://www.python.org/download/) ![Build Status](https://img.shields.io/badge/Version-0.1-red.svg)

🎃 目录扫描工具

![-w690](media/15957398083981.jpg)

## 1. Install
```
git clone https://github.com/j3ers3/Dirscan
pip3 install -r requirements.txt
```

## 2. Usage
```
-h, --help        show this help message and exit
-u URL           URL target
-w WORDLIST  Customize wordlist (default wordlist.txt)
-t THREADS    Set thread (default 20)
-v                  show verbose
```

```
python3 dirscan.py -u http://127.0.0.1:8081
python3 dirscan.py -u http://127.0.0.1:8081 -w dict.txt -t 30 -v
```

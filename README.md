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
optional arguments:
  -h, --help   show this help message and exit
  -u URL       URL target
  -U URLFILE   URL list target
  -w WORDLIST  Customize wordlist (default wordlist.txt) or a single path
  -t THREADS   Set thread (default 20)
  -v           show verbose
```


- 默认扫描：python3 dirscan.py -u http://127.0.0.1:8081
- 显示详细：python3 dirscan.py -u http://127.0.0.1:8081 -v
- 指定字典：python3 dirscan.py -u http://127.0.0.1:8081 -w wordlist.txt -t 30 -v
- 文件扫描：python3 dirscan.py -U url.txt -w /admin -t 20 -v

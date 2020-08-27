#!/usr/bin/env python3
# encoding:utf8
import time
import asyncio
import aiohttp
import argparse
from rich.console import Console
from rich.table import Column, Table
from rich.progress import track
from util.util import *

__author__ = 'whois'
__date__ = '2020/07/25'
__version__ = 'v0.2'
"""
    Dirscan
    A simple and fast directory scanning tool for pentesters
    
"""

TIMEOUT = 4
output = "output_{}.txt".format(randomDigits())

HEADERS = {"Cache-Control": "max-age=0", "Upgrade-Insecure-Requests": "1",
           "Content-Type": "application/x-www-form-urlencoded",
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3578.98 Safari/537.36",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
           "Referer": "https://google.com", "Accept-Encoding": "gzip, deflate",
           "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,ko;q=0.6", 
           "Connection": "close"}

console = Console()
table = Table(show_header=True, header_style="bold magenta")
table.add_column("Code")
table.add_column("URL")
table.add_column("Length", justify="right")


def banner():
    console.print('''[red]
██████╗ ██╗██████╗ ███████╗ ██████╗ █████╗ ███╗   ██╗
██╔══██╗██║██╔══██╗██╔════╝██╔════╝██╔══██╗████╗  ██║
██║  ██║██║██████╔╝███████╗██║     ███████║██╔██╗ ██║
██║  ██║██║██╔══██╗╚════██║██║     ██╔══██║██║╚██╗██║
██████╔╝██║██║  ██║███████║╚██████╗██║  ██║██║ ╚████║
╚═════╝ ╚═╝╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝

                                    [/red][yellow]code by {0}[/yellow] [blue]{1}[/blue]


'''.format(__author__, __version__))


def word_list(wordfile):
    import os.path
    if not os.path.isfile(wordfile):
        print("[x] The specified dictionary file does not exist!")
        exit(1)
    with open(wordfile, 'r') as f:
        f = [line.rstrip() for line in f.readlines()]
    return f

def url_list(urlfile):
    with open(urlfile, 'r') as f:
        f = [line.rstrip() for line in f.readlines()]
    return f


async def get(url, w, sem, verbose):
    async with sem:
        async with aiohttp.ClientSession(headers=HEADERS) as session:
            scan_url = url + w

            try:
                r = await session.get(scan_url, timeout=TIMEOUT, allow_redirects=False)
                s, l= r.status, len(await r.text())
                if verbose == 1:
                    console.print("[cyan]{}[/cyan] -> [red]{}[/red] -> [green]{}[/green]".format(scan_url, s, l))
                
                # 默认文件输出，不用可注释
                if s in [200, 301, 302, 401, 403]:
                    with open(output, 'a') as f:
                        f.write("{} -> {} -> {}\n".format(scan_url, s, l))

                if s == 200:
                    table.add_row("[green]{}[/green]".format(s), scan_url, "{}".format(l))
                elif s in [301, 302]:
                    table.add_row("[blue]{}[/blue]".format(s), scan_url, "{}".format(l))
                elif s in [401, 403]:
                    table.add_row("[purple]{}[/purple]".format(s), scan_url, "{}".format(l))
            except Exception as e:
                #print(e)
                pass


async def run(url, wordfile, threads, verbose):
    sem = asyncio.Semaphore(threads)  # 限制并发量
    do = [get(url, w, sem, verbose) for w in word_list(wordfile)] 
    await asyncio.wait(do)


async def run2(urlfile, word, threads, verbose):
    sem = asyncio.Semaphore(threads)  # 限制并发量
    do = [get(url, word, sem, verbose) for url in url_list(urlfile)] 
    await asyncio.wait(do)


def main():
    banner()
    parser = argparse.ArgumentParser(
        usage='\ndirscan -u url -w dict.txt -t 20 -v\ndirscan -U url.txt -w /admin -t 20 -v',
        description="目录扫描工具",
    )

    parser.add_argument("-u", dest="url",
                        help="URL target")
    parser.add_argument("-U", dest="urlfile",
                        help="URL list target")
    parser.add_argument("-w", dest="wordlist", type=str, default="./wordlist.txt",
                        help="Customize wordlist (default wordlist.txt) or a single path")
    parser.add_argument("-t", dest="threads", type=int, default=20,
                        help="Set thread (default 20)")
    parser.add_argument("-v", dest="verbose", action="store_true",
                        help="show verbose")

    args = parser.parse_args()

    if args.url is None and args.urlfile is None:
        console.print("[red][[x]] python3 dirscan.py -h[/red]")
        exit(0)

 
    start_time = time.time()


    loop = asyncio.get_event_loop()
   
    if args.url:
        console.print("[blue]Use {} threads to scan {}[/blue]".format(args.threads, args.url))
        # 设置是否展示详细
        loop.run_until_complete(run(args.url, args.wordlist, args.threads, 1)) if args.verbose is True else loop.run_until_complete(run(args.url, args.wordlist, args.threads, 0))

    elif args.urlfile:
        console.print("[blue]Use {} threads to scan {}[/blue]".format(args.threads, args.urlfile))
        loop.run_until_complete(run2(args.urlfile, args.wordlist, args.threads, 1)) if args.verbose is True else loop.run_until_complete(run2(args.urlfile, args.wordlist, args.threads, 0))
 
    loop.close()

    console.print(table)

    console.print("\nTask Completed used [green]{0}[/green] seconds".format(time.time() - start_time))


if __name__ == '__main__':
    main()
    

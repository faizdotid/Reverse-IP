#just for fun

import requests
from proxyscrape import create_collector
collector = create_collector('my-collector', ['http', 'https', 'socks5', 'socks4'])
import sys
import time
from threading import Thread
import os
from queue import Queue

try:
  os.mkdir('result')
except:
  pass


def reqprox():
  p = collector.get_proxy()
  proxy = p.host+':'+p.port
  dictprox = dict({'http': proxy, 'https': proxy})
  return dictprox
 

proxy = reqprox()


def revip(ip):
  global proxy
  apiUrl = 'https://api.hackertarget.com/reverseiplookup/?q='+ip
  head = {'User-Agent': 'Mozzila'}
  try:
    request = requests.get(apiUrl, proxies=proxy, headers=head, timeout=70)
    if 'No DNS' in request.text:
      print('[-] Wrong IP Format [-]')
    elif 'API count' in request.text:
      print('[-] Try To Bypass With >> {} [-]'.format(proxy))
      proxy = reqprox()
      revip(ip)
    elif '429 Too Many' in request.text:
      print('[-] Wait [-]')
      time.sleep(3)
      proxy = reqprox()
      revip(ip)
    else:
      totdom = 0
      for dom in request.text.splitlines():
        totdom += 1
        print('[+] Grabbed >> {} [+]'.format(dom))
        sv = open('result/reversed.txt', 'a')
        sv.write('http://'+dom+'\n')
        sv.close()
      svdup = open('result/exec.txt', 'a')
      svdup.write(ip+' | '+str(totdom)+'\n')
      svdup.close()
  except Exception:
    print('[-] Dead Proxy >> {} [-]'.format(proxy))
    proxy = reqprox()
    revip(ip)
 
def redup(ip):
  open('result/exec.txt', 'a')
  try:
    if ip in open('result/exec.txt', 'r').read():
      print('[-] Duplicate >> {} [+]'.format(ip))
    else:
      revip(ip)
  except:
    pass

job = Queue()

def jalan(q):
  while not q.empty():
    targ = q.get()
    targ = targ.replace('http://', '').replace('https://', '').replace('/', '')
    redup(targ)
    q.task_done()

if len(sys.argv) != 3:
  print('Usage : python3 {} ips.txt threads'.format(sys.argv[0]))
else:
  for tt in open(sys.argv[1], 'r').read().split('\n'):
    job.put(tt)
  for i in range(int(sys.argv[2])):
    t = Thread(target=jalan, args=(job,))
    t.start()

job.join()
  

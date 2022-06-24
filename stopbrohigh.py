import os
import requests
from pytools.pytools import pickledump
from pytools.pytools import pickleread
from ckhash import *

current=19

s=requests.Session()
on=os.environ['on']
notice=''
config=pickleread('stopbrohigh.txt',{'num':0,'running':'','network':True})
num=config['num']
running=config['running']
network=config['network']
with open('exeblacklist.txt') as f:
  blacklist=f.read().splitlines()

def stopbrohigh():
  try:
    r=s.get('http://bropc.lan:1234/stophigh')
    if '.exe' in r.text:
      return '高占用已结束'
  except requests.exceptions.ConnectionError:
    return '连接出错'

pc,raw,exe=bropcHash()

if exe=='连接出错':
  network=False
elif network==False: #首次恢复连接
  num=0
  network=True
else: #连接正常
  network=True

if pc<current:
  if running!=exe or exe=='pausing':
    num=0
  else:
    num+=1
  if (exe in blacklist) and bronum==5 and network==True:
    notice=stopbrohigh()
else:
  num=0

if num>=5:
  if network==False:
    reason='连接出错'
  elif notice:
    reason=notice
  else:
    reason='未知错误'
  serverchen('弟弟高占用达%s次#%s'%(num,reason),raw)

print('before: '+config)
config={'num':num,'running':exe,'network':network}
print('after: '+config)
print(raw)
if on=='schedule':
  pickledump(config,'stopbrohigh.txt')

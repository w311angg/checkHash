import os
import requests
from pytools.pytools import pickledump
from pytools.pytools import pickleread
from pytools.pytools import ifOnePlusTwoPlusThree
from ckhash import *

current=19

s=requests.Session()
on=os.environ['on']
notice=''
pc,raw,exe=bropcHash()
status=raw.split(', ')[0]
config=pickleread('stopbrohigh.txt',{'num':0,'running':exe,'network':True})
num=config['num']
running=config['running']
network=config['network']
blacklist={}
with open('exeblacklist.txt') as f:
  for i in [i.split() for i in f.read().splitlines()]:
    name=i[0]
    times=int(i[1])
    blacklist[name]={}
    blacklist[name]['times']=times

def stopbrohigh():
  try:
    r=s.get('http://bropc.lan:1234/stophigh?forbro')
    if '.exe' in r.text:
      return '高占用已结束'
    else:
      return r.text
  except requests.exceptions.ConnectionError:
    return '连接出错'

if exe=='连接出错':
  network=False
elif network==False: #首次恢复连接
  num=0
  network=True
else: #连接正常
  network=True
if running!=exe and running[-4:]=='.exe':
  num=0

if exe=='pausing':
  num=0
elif pc<current or status=='checkonly':
  if status!='checkonly':
    num+=1
  else:
    print('处于checkonly模式')
    exe=[i for i in raw.split(', ') if '.exe' in i][0]
    if exe in blacklist:
      num+=1
  if (exe in blacklist) and num%blacklist[exe]['times']==0 and network==True:
    notice=stopbrohigh()
else:
  num=0

def sendmessage():
  if ((num>=5 and ifOnePlusTwoPlusThree(num)) or num==5) or (exe in blacklist and num>=blacklist[exe]['times']-1):
    if network==False:
      reason='连接出错'
      if status=='checkonly':
        print('处于checkonly模式，忽略连接出错，因为电脑可能休眠')
        return
    elif notice:
      reason=notice
    elif exe=='not running!!':
      reason=exe
    elif not exe in blacklist:
      reason='不在黑名单'
    elif num%blacklist[exe]['times']==blacklist[exe]['times']-1:
      reason='即将关闭'
      print('因已有检测是否使用而不提醒即将关闭')
      return
    else:
      reason='关闭后仍不达标'
    serverchen('弟弟高占用达%s次#%s'%(num,reason),raw)
sendmessage()

print('before: '+str(config))
config={'num':num,'running':exe,'network':network}
print('after: '+str(config))
print('blacklist: '+str(blacklist))
print(raw)
if on=='schedule':
  pickledump(config,'stopbrohigh.txt')

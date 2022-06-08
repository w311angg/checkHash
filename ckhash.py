import os
import requests
from pytools.pytools import jmail
from pytools.pytools import isnewday
from pytools.pytools import serverchen

current=19

s=requests.Session()
shortmsg=''
forcesend=0
try:
  with open('num.txt') as f:
    number=int(f.read())
except FileNotFoundError:
  number=0
with open('exeblacklist.txt') as f:
  blacklist=f.read().splitlines()
with open('errnum.txt') as f:
  errnum=int(f.read())

def hash(url):
  try:
    with s.get(url) as resp:
      text=resp.text
      data=text.split(', ')
      status=data[0]
      if len(data)==1 or len(data)==2:
        hash=0
        specialexe='pausing' if 'pausing' in status else status
      else:
        hash=data[2].replace(' MH/s','')
        if hash=='N/A':
          hash=0
          specialexe='未运行!!'
        else:
          hash=float(hash)
        specialexe=data[3]
  except requests.exceptions.ConnectionError:
    hash=0
    text='ConnectionError'
    specialexe='连接出错'
  return (hash,text,specialexe)

def mypcHash():
  return hash('http://mypc.lan:1234')

def bropcHash():
  return hash('http://bropc.lan:1234')

mypchash=mypcHash()
mypc=mypchash[0]
mypctext=mypchash[1]
mypcexe=mypchash[2]

bropchash=bropcHash()
bropc=bropchash[0]
bropctext=bropchash[1]
bropcexe=bropchash[2]

def check():
  if mypc+bropc<current:
    return 1 #单台不达标
  elif mypc<current or bropc<current:
    return 2 #不达标
  else:
    return 0

def sendemail(title):
#  content="""\
#基准速率 %s MH/s<br>
#我 %s<br>
#弟弟 %s<br>
#<i><b><a href="http://pi.lan/checkhash.php">刷新</a></b></i>\
#"""%(current,mypctext,bropctext)
  #jmail('checkHash',title,content,html=True)
  serverchen(title,content)
  print('已发送邮件')

def stopbrohigh():
  global shortmsg
  try:
    r=s.get('http://bropc.lan:1234/stophigh')
    if '.exe' in r.text:
      shortmsg='高占用已结束'
  except requests.exceptions.ConnectionError:
    shortmsg='连接出错'
    #因为check时出错已计算errnum
    #errnum+=1

def numberadd():
  global number
  if os.environ['on']=='schedule':
    number+=1

status=check()
connectionError=('连接出错' in (mypcexe,bropcexe))
pausing=('pausing' in (bropcexe,mypcexe))
if pausing or connectionError:
  number=0
  if connectionError:
    errnum+=1
    title='哈希宝连接出错%s小时'%errnum
    forcesend=number
elif status==1:
  numberadd()
  title='哈希宝单台不达标%s小时#%s'%(number,'%s')
elif status==2:
  numberadd()
  title='哈希宝不达标%s小时#%s'%(number,'%s')
elif status==0:
  if number!=0:
    forcesend=number
    title='哈希宝达标'
  else:
    title=''
  number=0

if not connectionError:
  errnum=0

#“连接出错”的情况包含在bropcexe中，而blacklist中没有“连接出错”
if bropc<current and bropcexe!='pausing' and number>=5 and (bropcexe in blacklist):
  stopbrohigh()
  forcesend=number
  number=0

try:
  title=title%(bropcexe if not shortmsg else shortmsg)
except TypeError:
  pass
content="""\
基准速率 %s MH/s
我 %s [关闭](http://mypc.lan:1234/stophigh)
弟弟 %s [关闭](http://bropc.lan:1234/stophigh)
_**[刷新](http://pi.lan/checkhash.php)**_\
"""%(current,mypctext,bropctext)
content=content.replace('\n','\n\n')

print(title,number)
if forcesend or number==1 or number>=4:
  sendemail(title)

with open('num.txt','w') as f:
  f.write(str(number))
with open('errnum.txt','w') as f:
  f.write(str(number))

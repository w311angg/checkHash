import requests
from pytools.pytools import jmail
from pytools.pytools import isnewday
from pytools.pytools import serverchen

current=19

s=requests.Session()
if isnewday():
  number=0
else:
  try:
    with open('num.txt') as f:
      number=int(f.read())
  except FileNotFoundError:
    number=0

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

bropchash=bropcHash()
bropc=bropchash[0]
bropctext=bropchash[1]
bropcexe=bropchash[2]

def check():
  if mypc+bropc<current:
    return 1 #单台不达标
  elif mypc+bropc<current*2:
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
  content="""\
基准速率 %s MH/s
我 %s
弟弟 %s
_**[刷新](http://pi.lan/checkhash.php)**_\
"""%(current,mypctext,bropctext)
  content=content.replace('\n','\n\n')
  print(title)
  print(content)
  #jmail('checkHash',title,content,html=True)
  serverchen(title,content)

status=check()
if status==1:
  number+=1
  sendemail('哈希宝单台不达标%s小时#%s'%(number,bropcexe))
elif status==2:
  number+=1
  if bropctext!='pausing':
    sendemail('哈希宝不达标%s小时#%s'%(number,bropcexe))
elif status==0 and number!=0:
  number=0
  sendemail('哈希宝达标')

with open('num.txt','w') as f:
  f.write(str(number))

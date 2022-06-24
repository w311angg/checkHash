import os
import requests
from pytools.pytools import serverchen

if __name__=='__main__':
  current=19

  s=requests.Session()
  try:
    with open('num.txt') as f:
      number=int(f.read())
  except FileNotFoundError:
    number=0

def hash(url):
  if __name__!='__main__':
    s=requests.Session()
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
  return hash,text,specialexe

def mypcHash():
  return hash('http://mypc.lan:1234')

def bropcHash():
  return hash('http://bropc.lan:1234')

def sendemail(title):
  content=content.replace('\n','\n\n')
  serverchen(title,content)
  print('已发送邮件')

if __name__=='__main__':
  mypc,mypctext,mypcexe=mypcHash()
  bropc,bropctext,bropcexe=bropcHash()

  content="""\
基准速率 %s MH/s
我 %s [关闭](http://mypc.lan:1234/stophigh)
弟弟 %s [关闭](http://bropc.lan:1234/stophigh)
_**[刷新](http://pi.lan/checkhash.php)**_\
"""%(current,mypctext,bropctext)

  if mypc+bropc<current: #单台不达标
    number+=1
    title='哈希宝单台不达标%s小时#%s'%(number,bropcexe)
    if number>=6:
      sendemail(title)
  elif mypc<current or bropc<current: #不达标
    number+=1
    title='哈希宝不达标%s小时#%s'%(number,bropcexe)
    if number>=6:
      sendemail(title)
  else:
    if number!=0:
      number=0
      title='哈希宝已达标'
      #sendemail(title)

  print('number: %s\ntitle: %s\ncontent:\n%s'%(number,title,content))

  with open('num.txt','w') as f:
    f.write(str(number))

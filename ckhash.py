import os
import requests
from pytools.pytools import serverchen
from pytools.pytools import ifOnePlusTwoPlusThree

if __name__=='__main__':
  current=19

  s=requests.Session()
  try:
    with open('num.txt') as f:
      number=int(f.read())
  except FileNotFoundError:
    number=0

  with open('exeblacklist.txt') as f:
    txt=f.read()
    blacklist=[i.split(' ')[0] for i in txt.splitlines()]

def hash(url):
  s=requests.Session()
  try:
    with s.get(url) as resp:
      code=resp.status_code
      if code!=200:
        hash=0
        text='ConnectionError'
        specialexe='连接出错'
      else:
        text=resp.text
        data=text.split(', ')
        status=data[0]
        if 'pausing' in status: #pausing后会接还剩多久时间
          hash=0
          specialexe='pausing'
        elif status=='running':
          hash=data[2].replace(' MH/s','')
          if hash=='N/A':
            hash=0
            specialexe='未运行!!'
          else:
            hash=float(hash)
            specialexe=data[3]
        else:
            hash=0
            specialexe=status
  except requests.exceptions.ConnectionError as e:
    print(e)
    hash=0
    text='ConnectionError'
    specialexe='连接出错'
  return hash,text,specialexe

def mypcHash():
  return hash('http://mypc.lan:1234')

def bropcHash():
  return hash('http://bropc.lan:1234')

def sendemail(title):
  contentmd=content.replace('\n','\n\n')
  serverchen(title,contentmd)
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

  if mypc<current: #我不达标
    number+=1
    title='哈希宝我不达标%s小时#%s'%(number,bropcexe)
    if number>=6 and ifOnePlusTwoPlusThree(number):
      sendemail(title)
  else:
    if number!=0:
      number=0
      title='哈希宝我已达标'
      #sendemail(title)
    else:
      title='我哈希宝达标'

  print('number: %s\ntitle: %s\ncontent:\n%s'%(number,title,content))

  with open('num.txt','w') as f:
    f.write(str(number))

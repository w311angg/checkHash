import requests
from pytools.pytools import jmail
from pytools.pytools import isnewday

current=20

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
  with s.get(url) as resp:
    text=resp.text
    data=text.split(', ')
    if len(data)==1:
      return (0,text)
    else:
      hash=float(data[2].replace(' MH/s',''))
  return (hash,text)

def mypcHash():
  return hash('http://mypc.lan:1234')

def bropcHash():
  return hash('http://bropc.lan:1234')

mypc=mypcHash()[0]
bropc=bropcHash()[0]
mypctext=mypcHash()[1]
bropctext=bropcHash()[1]
def check():
  if mypc+bropc<current:
    return 1 #单台不达标
  elif mypc+bropc<current*2:
    return 2 #不达标
  else:
    return 0

def sendemail(title):
  content="""\
基准速率 %s MH/s
我 %s
弟弟 %s\
"""%(current,mypctext,bropctext)
  print(title)
  print(content)
  jmail('checkHash',title,content)

status=check()
if status==1:
  number+=1
  sendemail('哈希宝单台不达标')
elif status==2:
  number+=1
  sendemail('哈希宝不达标')
elif status==0:
  number=0
  sendemail('哈希宝达标')

with open('num.txt','w') as f:
  f.write(str(number))

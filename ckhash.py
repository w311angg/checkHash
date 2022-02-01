import requests
from pytools.pytools import jmail
from pytools.pytools import isnewday

s=requests.Session()
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
  current=20
  print(mypc,bropc)
  if mypc<current or bropc<current:
    return 1 #单台不达标
  elif mypc+bropc<current*2:
    return 2 #不达标
  else:
    return 0

def sendemail(title):
  global number
  content='\n'.join((mypctext,bropctext))
  number+=1
  jmail('checkHash',title,content)

status=check()
if status==1:
  sendemail('哈希宝单台不达标')
elif status==2:
  sendemail('哈希宝不达标')
elif status==0:
  number=0
if isnewday():
  number=0

with open('num.txt','w') as f:
  f.write(number)

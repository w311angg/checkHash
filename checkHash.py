import requests
import os
import random
import time
import pickle
from tenacity import retry, stop_after_attempt
from pas import pas

try:
  print(requests.get('https://www.google.com/'))
except:
  pass

proxies = {
    'http': 'socks5://localhost:1080',
    'https': 'socks5://localhost:1080'
}
session = requests.Session()
#session.proxies.update(proxies)
session.headers.update({'user-agent':'Dalvik/2.1.0 (Linux; U; Android 10; ONEPLUS A3010 Build/QQ3A.200805.001)','Content-Type':'application/x-www-form-urlencoded;charset=UTF-8'})
try:
  with open('cookies.txt','rb') as f:
    first=False
    dict=pickle.load(f)
    #print(dict)
    session.cookies.update(dict['cookies'])
    uid=dict['uid']
    rewarded=dict['rewarded']
except FileNotFoundError:
  first=True
  rewarded=False
  print('FileNotFoundError')
#print(session.get('https://www.google.com/').text)
num=0
with open('num.txt',mode='r') as f:
  num=int(f.read())
wait=random.randint(1,9)
print('等'+str(wait)+'分钟')
on=os.getenv('on')
#print(on)
if on=='schedule':
  time.sleep(wait*60)
#print(session.cookies,session.post('http://app.hxbao.com/api/v2/workdata',data={'uid':uid}).cookies,session.cookies)
@retry(stop=stop_after_attempt(10))
def login():
  global h,uid
  h=session.post('http://app.hxbao.com/api/v2/login',data={'password':os.getenv('password'),'account':os.getenv('account')})
  uid=h.json()['data']['uid']
  print('已登录')
#print(session.post('http://app.hxbao.com/api/v2/workdata',data={'uid':uid}).text)
if first or session.post('http://app.hxbao.com/api/v2/workdata',data={'uid':uid}).json()['code']==400:
  login()
#print(h.text,h.cookies)
a='number=2&uid=%s&card=1060'%(uid)
#print(session.post('http://app.hxbao.com/api/v2/CalByCard',data=a).text)
#print(session.post('http://app.hxbao.com/api/v2/CalByCard',data=a).json()['data'])
目标=session.post('http://app.hxbao.com/api/v2/CalByCard',data=a,headers={'Content-Type':'application/x-www-form-urlencoded;charset=UTF-8'}).json()['data']['incomeNum']
e='number=1&uid=%s&card=1060'%(uid)
f=session.post('http://app.hxbao.com/api/v2/CalByCard',data=e,headers={'Content-Type':'application/x-www-form-urlencoded;charset=UTF-8'}).json()['data']
目标1=f['incomeNum']
速度1=f['speed']
phps=session.cookies.get('PHPSESSID',domain='app.hxbao.com')
b=session.post('http://app.hxbao.com/api/v2/workdata',data='uid=9891',cookies={'PHPSESSID':phps}).json()
#print(b)
实际=int(b['data']['rate'][0]['rate'].replace('元',''))
在线=int(b['data']['online'].replace('台',''))
#实际=0
在线情况=''
#在线=0
if 在线!=0:
  #print(session.post('http://app.hxbao.com/api/v2/terminal',data='uid=9891',cookies={'PHPSESSID':phps}).json())
  c=session.post('http://app.hxbao.com/api/v2/terminal',data='uid=9891',cookies={'PHPSESSID':phps}).json()['Machine']
  for i in c:
    在线情况+=i['remark']+' '+i['speed_24h']
g=str(round(实际-目标,2))
host=os.getenv('host')
pas(host,os.getenv('pw'))
url='http://'+host+'/'
myhash=requests.get(url+'myhash.php').text
brohash=requests.get(url+'brohash.php').text
发送内容="""应挖%s，实挖%s(%s)，在线%s
基准速度 %sM
%s
------
我的电脑 %s
弟弟的电脑 %s
"""%(目标,实际,g,在线,速度1,在线情况,myhash,brohash)
print(发送内容)
发送主题=''

def check():
  global 发送主题,g,num
  if 实际<目标:
    num+=1
    with open('num.txt',mode='w') as f:
      f.write(str(num))
    if 实际<目标1:
      发送主题='⚠单台电脑哈希宝不达标'
      g=str(round(实际-目标1,2))
      print(发送主题)
      print('已连续'+str(num)+'次未达标')
      return True
    发送主题='已连续%s次不达标'%num
    print(发送主题)
    print('已连续'+str(num)+'次未达标')
    return True
    #return False
  else:
    print('挖矿达标')
    if num!=0 and (not num%2):
      发送主题='哈希宝已达标'
      print(发送主题)
      num=0
      with open('num.txt',mode='w') as f:
        f.write(str(num))
      return True
    return False

if check() and (not num%2):
  #if myhash=='None':
  #  mystat=requests.get(url+'myhash.php?restart')
  #  print(mystat.text)
  #if brohash=='None':
  #  brostat=requests.get(url+'brohash.php?restart')
  #  print(brostat.text)

  import smtplib
  from email.mime.text import MIMEText
  from email.utils import formataddr
   
  my_sender=os.getenv('sender')    # 发件人邮箱账号
  my_pass = os.getenv('pass')              # 发件人邮箱密码
  my_user=os.getenv('to')      # 收件人邮箱账号，我这边发送给自己
  def mail():
      msg=MIMEText(发送内容,'plain','utf-8')
      msg['From']=formataddr(["checkHash",my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
      msg['To']=formataddr(["WG",my_user])              # 括号里的对应收件人邮箱昵称、收件人邮箱账号
      msg['Subject']=发送主题                # 邮件的主题，也可以说是标题
   
      server=smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
      server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
      server.sendmail(my_sender,[my_user,],msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
      server.quit()  # 关闭连接
  mail()
  print('邮件已发送')

today=time.strftime("%d", time.localtime())
#print(today,rewarded)
if today=='19' and (not rewarded):
#if True:
  account=os.getenv('raccount')
  num=session.post('http://app.hxbao.com/api/v2/center',data={'uid':uid}).json()['data']['reward']
  num=float(num)
  #num=0.01
  #print(num)
  if num>100:
    reward=session.post('http://app.hxbao.com/api/v2/withdrawing',data={'symbol':'reward','uid':uid,'num':num,'type':1,'account':account}).json()
    print(reward['msg'])
    rewarded=True
if today!='19':
  rewarded=False

with open('cookies.txt','wb') as f:
  pickle.dump({'cookies':session.cookies,'uid':uid,'rewarded':rewarded}, f)

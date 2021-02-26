import requests
import os
import random
import time
wait=random.randint(1,9)
print('等'+str(wait)+'分钟')
time.sleep(wait*60)
h=requests.post('http://behash.com/api/v2/login',data={'password':os.getenv('password'),'account':os.getenv('account')})
uid=h.json()['data']['uid']
a='number=2&uid=%s&card=1060'%(uid)
#print(requests.post('http://behash.com/api/v2/CalByCard',data=a).text)
目标=requests.post('http://behash.com/api/v2/CalByCard',data=a).json()['data']['incomeNum']
e='number=1&uid=%s&card=1060'%(uid)
f=requests.post('http://behash.com/api/v2/CalByCard',data=e).json()['data']
目标1=f['incomeNum']
速度1=f['speed']
phps=h.cookies['PHPSESSID']
b=requests.post('http://behash.com/api/v2/workdata',data='uid=9891',cookies={'PHPSESSID':phps}).json()
#print(b)
实际=b['data']['rate']
在线=b['data']['online']
#实际=0
在线情况=''
#在线=0
if 在线!=0:
  c=list(requests.post('http://behash.com/api/v2/terminal',data='uid=9891',cookies={'PHPSESSID':phps}).json()['data'][0].items())
  for i in c:
    d=list(i)
    在线情况+=d[0]+' '+d[1]+'\n'
g=str(round(实际-目标,2))
发送内容='应挖'+str(目标)+'，实挖'+str(实际)+'('+g+')'+'，在线'+str(在线)+'\n'+'基准速度 '+速度1+'M\n'+在线情况
print(发送内容)
发送主题=''

def check():
  global 发送主题,g
  if 实际<目标 or 在线<2:
    if 实际<目标1:
      发送主题='⚠单台电脑哈希宝挖矿不达标'
      g=str(round(实际-目标1,2))
      print(发送主题)
      return True
    发送主题='哈希宝挖矿不达标'
    print(发送主题)
    #return True
    return False
  else:
    print('挖矿达标')
    return False

if check():
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

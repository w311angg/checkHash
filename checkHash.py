import requests
import os
a='number=2&uid=9891&card=1060'
目标=requests.post('http://behash.com/api/v2/CalByCard',data=a).json()['data']['incomeNum']
e='number=1&uid=9891&card=1060'
目标1=requests.post('http://behash.com/api/v2/CalByCard',data=e).json()['data']['incomeNum']
b=requests.post('http://behash.com/api/v2/workdata',data='uid=9891',cookies={'PHPSESSID':'5d7td4plvacn9v3k598rj9bj97'}).json()
实际=b['data']['rate']
在线=b['data']['online']
实际=0
c=list(requests.post('http://behash.com/api/v2/terminal',data='uid=9891',cookies={'PHPSESSID':'5d7td4plvacn9v3k598rj9bj97'}).json()['data'][0].items())
在线情况=''
for i in c:
  d=list(i)
  在线情况+=d[0]+' '+d[1]+'\n'
发送内容='应挖'+str(目标)+'，实挖'+str(实际)+'('+str(round(实际-目标,2))+')'+'，在线'+str(在线)+'\n'+在线情况
print(发送内容)
发送主题=''

def check():
  global 发送主题
  if 实际<目标 or 在线<2:
    if 实际<目标1:
      发送主题='⚠单台电脑哈希宝挖矿不达标'
      发送内容='应挖'+str(目标)+'，实挖'+str(实际)+'('+str(round(实际-目标1,2))+')'+'，在线'+str(在线)+'\n'+在线情况
      print(发送主题)
      return True
    发送主题='哈希宝挖矿不达标'
    print(发送主题)
    return True
  else:
    print('挖矿达标')
    return False

if check():
  import smtplib
  from email.mime.text import MIMEText
  from email.utils import formataddr
   
  my_sender='w311ang@qq.com'    # 发件人邮箱账号
  my_pass = os.getenv('pass')              # 发件人邮箱密码
  my_user='wg@runz.tk'      # 收件人邮箱账号，我这边发送给自己
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

from bs4 import BeautifulSoup
import requests

s=requests.Session()
s.verify=False
requests.packages.urllib3.disable_warnings()
passed=[]

def pas(host,pw):
  if ('http://' or 'https://') in host:
    url=host.replace('http://','https://')
  else:
    url='https://'+host
  #print(host)
  if not url in passed:
    try:
      with s.get(url) as web:
        text=web.text
        soup=BeautifulSoup(text,features='lxml')
        csrf=soup.find('input',{'name':'csrf'}).get('value')
        ip=soup.find('input',{'name':'ip'}).get('value')
      with s.post(url,data={'pw':pw,'csrf':csrf,'ip':ip}) as web:
        #print(web.request.body)
        text=web.text
        soup=BeautifulSoup(text,features='lxml')
        notice=soup.find('div',{'class':'notice'}).string
        notice=notice.strip()
        print(notice)
        if '认证成功' in notice:
          passed.append(url)
        return notice
    except requests.exceptions.SSLError:
      re='SSL出错，可能已验证'
      print(re)
      return re

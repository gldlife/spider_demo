import urllib.request
import re
from openpyxl import Workbook
from bs4 import BeautifulSoup
import io,sys

#改变标准输出的默认编码
#sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')

url='http://www.buildhr.com/so/11-kjBIM-sm1-p2.html' #要爬取的网址
base_url='http://www.buildhr.com'
def get_html(url):  #获取网页源码
    headers = {"User - Agent":"ozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36"}  # 伪装浏览器请求报头
    request = urllib.request.Request(url=url, headers=headers)  # 请求服务器
    response = urllib.request.urlopen(request)  # 服务器应答
    content = response.read().decode('gbk')  # 以一定的编码方式查看源码
    # print(content) #打印页面源码
    return content

#获取搜索结果中的岗位名称和网址
def get_job_url(html,base_url): #需要输入两个参数：网页源码和基础网址，基础网址用于构件完整链接地址
    soup=BeautifulSoup(html,'html.parser')
    body=soup.body
    list_url=[]
    for td in soup.find_all('td',class_='td_sp1'):
        #print(base_url+td.a['href'],td.a.text)
        url=base_url+td.a['href']
        list_url.append(url)
        #print(url)
    return list_url
    #print(body)

def get_jobinfo(html): #获取详情页的职位描述信息
    jobs_info=[]
    soup=BeautifulSoup(html,'html.parser')
    div=soup.find('div',class_='wrap_lt_job')
    name=div.find(name='h1').text.strip()
    company=div.find(name='h3').text.strip()
    date=div.find(name='span').text.strip()
    work = div.find(name='ul', class_='job_info').find_all(name='li')[2].text.strip()
    xinzi=div.find(name='ul',class_='job_info').find_all(name='li')[5].text.strip()
    info=div.find(name='dl',class_='zxd_jobinfo').text.strip()
    jobs_info.append(name)
    jobs_info.append(company)
    jobs_info.append(date)
    jobs_info.append(xinzi)
    jobs_info.append(work)
    jobs_info.append(info)
    #print(jobs_info)
    return jobs_info

wb=Workbook()
ws=wb.active
item=['职位名称','公司','发布日期','薪资','工作经验','职位描述']
ws.append(item)
for i in range(201,307):
    print('正在爬取第%s页数据'%i)
    #url_zj='http://www.buildhr.com/so/11-kjBIM-sm1-p{}.html'.format(i)
    url_zj='http://www.buildhr.com/so/11-247102,247103-sm3-p{}.html'.format(i)
    try:
        html=get_html(url_zj)
        url_list=get_job_url(html,base_url)
        for i in url_list:
            html2=get_html(i)
            try:
                ws.append(get_jobinfo(html2))
            except:
                continue
    except:
        continue
        #break
wb.save('d:/建筑英才P201-306.xlsx')

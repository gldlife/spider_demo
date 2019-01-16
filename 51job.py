"""
author:李建飞
last date:2018-11-6
功能：爬取51job网站中关于BIM招聘的相关信息
"""
import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
#定义函数：get_job_urls()
def get_job_urls(url):
    urls_list=[]
    #0、获取搜索职位结果网页源码
    response=requests.get(url)
    response.encoding='gbk'#设置网页的编码格式
    soup=BeautifulSoup(response.text,'html.parser')
    #1、查看id=resultList的div
    div=soup.find(name='div',id='resultList').find_all(name='p',class_='t1')
    #print(div)
    #2、查找class=t1的p，返回列表
    #3、查找a标签，获取href的属性
    for p in div:
        href=p.find(name='a').get('href')
        #print(href)
        urls_list.append(href)
    return urls_list

#定义函数：get_job_info()获取职位信息
def get_job_info(url):
    job_info=[]
    #0、获取职位页的网页源码
    response=requests.get(url)
    response.encoding='gbk'
    #1、查找class=tCompany_center clearfix的div的部分内容
    soup=BeautifulSoup(response.text,'html.parser')
    div=soup.find(name='div',class_='tCompany_center')
    #2、获取职位名称、公司、薪资、发布时间、职位信息等内容
    name=div.find(name='h1').text.strip()
    company=div.find(name='a',class_='catn').text.strip()
    xinzi=div.find(name='strong').text.strip()
    date=div.find(name='p',class_='msg').get('title').strip()
    jinfo=div.find(name='div',class_='bmsg job_msg inbox').text.strip()
    #print(name,xinzi,date,jinfo)
    job_info.append(name)
    job_info.append(company)
    job_info.append(xinzi)
    job_info.append(date)
    job_info.append(jinfo)
    return job_info

#定认函数：save_to_excel()
#def save_to_excel():
    #将职位名称、薪资、发布时间、职位信息等四项内容写有文件中
wb=Workbook()
ws=wb.active
item=['职业名称','公司','薪资','发布时间','职位信息']
ws.append(item)
urls=[
    'https://search.51job.com/list/000000,000000,0000,00,9,99,BIM,2,1.html?lang=c&stype=1&postchannel=0100&workyear=99&cotype=99&degreefrom=03&jobterm=01&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=22&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=',
    'https://search.51job.com/list/000000,000000,0000,00,9,99,BIM,2,2.html?lang=c&stype=1&postchannel=0100&workyear=99&cotype=99&degreefrom=03&jobterm=01&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=22&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=',
    'https://search.51job.com/list/000000,000000,0000,00,9,99,BIM,2,3.html?lang=c&stype=1&postchannel=0100&workyear=99&cotype=99&degreefrom=03&jobterm=01&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=22&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
]
for i in range(1,144,1):
    print('正在抓取第%s页'%i)
    item='https://search.51job.com/list/000000,000000,2105%252C2124,00,9,99,%2B,2,{}.html?lang=c&stype=1&postchannel=0000&workyear=01%2C02&cotype=99&degreefrom=99&jobterm=01&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=22&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='.format(i)
    #item='https://search.51job.com/list/000000,000000,0000,00,9,99,BIM,2,{}.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=01&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=7&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='.format(i)
#for item in urls:
    for url in get_job_urls(item):
        try:
            ws.append(get_job_info(url))
        except:
            continue
    #break

wb.save('d:/q51jobys.xlsx')

import requests
import json
from bs4 import BeautifulSoup
#from openyxl import Workbook

#获取页面中所有课程的链接地址
def get_lessons_url_list(url):
    urls_list=[]
    r1=requests.get(url)
    #print(r1.text)
    soup=BeautifulSoup(r1.text,'html.parser')
    content=soup.find(id='SL-container').find_all(name='li',class_='pt20')
    for item in content:
        lesson_url=item.find(name='a').get('href')
        urls_list.append(lesson_url)
        print(lesson_url)
    return urls_list

#获取课程的销售数据
def get_lesson_sales_data(url):
    r1=requests.get(url)
    soup=BeautifulSoup(r1.text,'html.parser')
    article=soup.find(name='article',class_='c-attr')
    name=article.find(name='h3').text.strip()
    datas=article.find(name='div',class_='pt10')
    sales=datas.find_all(name='span')[2].text.strip()
    visits=datas.find_all(name='span')[3].text.strip()
    print(name,sales,visits)

url='http://jzkt.glodon.com/front/showcoulist'
#url='http://jzkt.glodon.com/front/couinfo/5110'
#get_lessons_url_list(url)
for item in get_lessons_url_list(url):
    try:
        get_lesson_sales_data(item)
    except:
        continue

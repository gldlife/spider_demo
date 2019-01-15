#导入所需要的模块
import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook

#起始网址
start_urlh='ttp://category.dangdang.com/cp01.22.00.00.00.00.html'

#获取网页源码
def get_html(url):
	r1=requests.get(url)
	r1.encoding='gbk'
	return r1.text

#获取图书列表
def get_product_list(html):
	soup=BeautifulSoup(html,'html.parser')
	ul=soup.find(id='component_59')
	return ul.find_all('li')

#获取商品信息
def get_book_info(item):
	#获取图书名称
	name=item.find('a').get('title')
	#获取图书价格
	price=item.find('span',class_='search_now_price').text
	#获取图书作者
	p=item.find('p',class_='search_book_author')
	author=p.find('a').get('title')
	detail=item.find('p',class_='detail').text
	return name,author,price,detail

#将数据存入excel
def save_xls(info):
	pass

#获取下一页网址
def get_next_url(html):
	base='http://category.dangdang.com'
	soup=BeautifulSoup(html,'html.parser')
	li=soup.find('li',class_='next')
	if li.find('a').get('href'):
		return base+li.find('a').get('href')
	else:
		return False


#管理
#next_page='http://category.dangdang.com/cp01.22.00.00.00.00.html'
#成功励志
next_page='http://category.dangdang.com/cp01.21.00.00.00.00.html'
wb=Workbook()
ws=wb.active
caption=['图书名称','作者','价格','简介']
ws.append(caption)
while(next_page):
	print(next_page)
	html=get_html(next_page)
	for item in get_product_list(html):
		ws.append(get_book_info(item))
	next_page=get_next_url(html)

wb.save('d:/dangdang_lizhi.xlsx')

"""
encoding:utf-8
author:李建飞
version:
"""
import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook

#获取网页源码
def get_html(url):
	headers={
		'Cookie':'_qddaz=QD.k32o58.nwbtxd.jaixfh0h; _ga=GA1.2.2125689912.1509600334; PS_DEVICEFEATURES=width:1440 height:900 pixelratio:1 touch:0 geolocation:1 websockets:1 webworkers:1 datepicker:1 dtpicker:1 timepicker:1 dnd:1 sessionstorage:1 localstorage:1 history:1 canvas:1 svg:1 postmessage:1 hc:0 maf:0; pgv_pvi=1727141888; SignOnDefault=lijf; UM_distinctid=1673a3aabaa4ef-0b26d96be19b51-3f3c5b02-100200-1673a3aabab755; Hm_lvt_3957fb8166a38239b57f22761e94950a=1545801904; _gid=GA1.2.2092059923.1547451581; ExpirePage=http://my.glodon.com/psp/ps/; PS_LOGINLIST=http://my.glodon.com/ps; PS_TOKEN=pAAAAAQDAgEBAAAAvAIAAAAAAAAsAAAABABTaGRyAk4AaQg4AC4AMQAwABR15hScd5x/TxnjgUMnBXP48jwdCmQAAAAFAFNkYXRhWHicJYoxCoAwFENfq4iTN6nY2iqOLuJY0MnFTah4RA/npwaSF0ISUBZaKeGryaofEjcX1cHKRhMlFnZOIjPe0WGZMJlGHHLvafE4yb8PjPIKsln4AGaCC1o=; http%3a%2f%2fmy.glodon.com%2fpsp%2fps%2femployee%2fempl%2frefresh=list:%20; PS_TOKENEXPIRE=15_Jan_2019_03:42:23_GMT; PHPSESSID=0neh8q4ih2uqjp1j21n23ha7c0; Hm_lvt_919b437c89ea35fb4a4f3254e58ac8b6=1547527202; __login_sid=UzdVMg9mAGs%3D; Hm_lpvt_919b437c89ea35fb4a4f3254e58ac8b6=1547528924',
		'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36',
		'Referer':url
	}
	response=requests.get(url,headers=headers)
	response.encoding='utf8'
	html=response.text
	return html

#获取合伙人的信息列表
def get_info_list(html):
	soup=BeautifulSoup(html,'html.parser')
	return soup.find_all('div',class_='list')

#获取单个合伙人信息
def get_partner_info(item):
	img=item.find('img').get('src')
	name=item.find('h1').text.strip().replace('\n','')
	grade=item.find_all('li')[1].text.strip().replace('\n','')
	assist=item.find('em').text
	return name,grade,assist,img


#将照片存储在本地
def save_jpg(info,save_path):
	url=info[-1]
	img_path=save_path+info[1]+"-"+info[0]+'.jpg' #设置图片保存完整路径
	content=requests.get(url).content #二进制读取图片信息
	with open(img_path,'wb') as f:
		f.write(content)
	return img_path+'下载成功！'

save_path='d:/partnerinfos/'
wb=Workbook()
ws=wb.active
caption=['姓名','级别','点赞数量','图片地址']
ws.append(caption)
for i in range(1,7):
	url='http://mxj.glodon.com/?c=partners&a=index&page={}'.format(i)
	for item in get_info_list(get_html(url)):
		info=get_partner_info(item)
		ws.append(info)
		print(save_jpg(info,save_path))

wb.save('d:/partnerinfos.xlsx')

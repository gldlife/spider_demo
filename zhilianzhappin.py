import requests
import json
from bs4 import BeautifulSoup
from openyxl import Workbook

def get_job_urls(url):
	urls_list=[]
	r1=requests.get(url)
	dict_json=json.loads(r1.content.decode())
	for item in dict_json['data']['results']:
		#print(item['positionURL'])
		urls_list.append(item['positionURL'])
	return urls_list

def get_job_info(url):
    jobs_info=[]
    response=requests.get(url)
    soup=BeautifulSoup(response.text,'html.parser')
    job=soup.find(name='div',class_='new-info')
    #print(job)
    job_name=job.find(class_='info-h3').text.strip().replace('\n','')
    job_xinzi=job.find(class_='info-money').text.replace('\n','')#.srtip()
    company=soup.find(class_='company').find(name='a').text.replace('\n','')
    job_info=soup.find(class_='responsibility pos-common').find(class_='pos-ul').text.strip().replace('\n','')
    print(job_name+'|'+job_xinzi+'|'+company+'|'+job_info)#,job_info)
    jobs_info.append(job_name)
    jobs_info.append(company)
    jobs_info.append(job_xinzi)
    jobs_info.append(jobs_info)
    return jobs_info
wb=Workbook()
ws=wb.active
item=['职位名称','公司','薪资','职位描述']
ws.append(item)
for i in range(60,300,60):
	url='https://fe-api.zhaopin.com/c/i/sou?start={}&pageSize=60&cityId=489&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kw=BIM%E5%B7%A5%E7%A8%8B%E5%B8%88&kt=3&rt=e3b33f9264344716b8c12010a533e05b&_v=0.55471521&x-zp-page-request-id=73c1e9add39e4db3a5c5a49936047f53-1542086646167-671450'.format(i)
	for item in get_job_urls(url):
		try:
			info=get_job_info(item)
            ws.append(info)
		except:
			continue

wb.save('d:/智联招聘.xlsx')

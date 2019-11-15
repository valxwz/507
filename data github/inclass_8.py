
import requests
from bs4 import BeautifulSoup





# print (len(content_div)) # to see if there's more than one

class Course:
	def __init__(self, course_num, course_name):
		self.course_num=course_num
		self.course_name=course_name

	def __str__(self):
		course_info=self.course_num +" " + self.course_name +" "+ self.description
		return course_info
	def get_course_info(self,details_url):
		page_content=requests.get(details_url,headers=header).text
		page_soup=BeautifulSoup(page_content,"html.parser")
		self.description=page_soup.find(class_='course2desc').text
		print ("decr",self.description)

baseurl = 'https://www.si.umich.edu'
catalog_url = baseurl + '/programs/courses/catalog'
header = {'User-Agent': 'SI_CLASS'}
page_text = requests.get(catalog_url, headers=header).text
page_soup = BeautifulSoup(page_text, 'html.parser')

content_div = page_soup.find(class_='view-content')
# print(content_div)


table_rows = content_div.find_all('tr')
# print (table_rows)
courses=[]
for tr in table_rows[:5]:
	table_cells = tr.find_all('td')
	if len(table_cells)==2:
		course_number = table_cells[0].text.strip()
		course_name = table_cells[1].text.strip()
		# print (course_name)
		details_url_end=table_cells[0].find('a')['href']
		details_url=baseurl + details_url_end
		course_list=Course(course_number,course_name)
		course_list.get_course_info(details_url)
		courses.append(course_list)
for i in courses:
	print (i)



# for tr in table_rows:
#     table_cells = tr.find_all('td')
#     course_number = table_cells[0].text.strip()
#     course_name = table_cells[1].text.strip()
#     print (table_cells)



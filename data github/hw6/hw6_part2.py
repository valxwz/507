# 507 Homework 6 Part 2
import requests
from bs4 import BeautifulSoup


#### Part 2 ####
print('\n*********** PART 2 ***********')
print('Michigan Daily -- MOST READ\n')



### Your Part 2 solution goes here

user_agent = {'User-agent': 'Mozilla/5.0'}
html = requests.get("https://www.michigandaily.com/", headers=user_agent).text


soup = BeautifulSoup(html, 'html.parser')

mostread_divs = soup.find_all("div", class_= "panel-pane pane-mostread")

a=mostread_divs[0].find_all("a")
titles=[]
for i in a:
	titles.append(i.contents)

for i in titles:
	print (i[0])



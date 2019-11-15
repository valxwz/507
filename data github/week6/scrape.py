from bs4 import BeautifulSoup

import requests

# f = open("hello.html")
# html = f.read()
# soup = BeautifulSoup(html, 'html.parser')

# all_li = soup.find_all('li')
# all_hellos=soup.find_all(id="hello-list")
# all_li=all_hellos[0].find('li')

# all_imgs=soup.find_all('img')
# print (all_imgs)
# print (all_imgs[0]['width'])
# print (all_li)
# print (all_li[0].string)
# print (all_hellos)
# print (all_li)
# for i in all_li:
# 	print (i.string)


html=requests.get("https://www.crummy.com/software/BeautifulSoup/bs4/doc/").text
soup=BeautifulSoup(html,'html.parser')

# print (soup.prettify())

search_div=soup.find(id="searching-the-tree")

# print (search_div)
h2=[]
h3=[]
all_hs=search_div.find_all(["h2","h3"])
for i in all_hs:
	if i.name=="h2":
		h2.append(i.text)
	else:
		h3.append(i.text)
print (h2)
print ("h3", h3)
# all_h3=search_div.find_all("h3")

# for i in all_h3:
# 	print (i.text)
# for i in all_h2:
# 	print ()

# h3=[]
# for i in all_divs:
# 	h3.append(i.find_all("h3"))

# print (h3)
# 507 Homework 6 Part 1
import requests
from bs4 import BeautifulSoup
import sys

#### Part 1 ####
print('\n*********** PART 1 ***********')
print("-------Alt tags-------\n")

### Your Part 1 solution goes here


url = sys.argv[1]

html = requests.get(url).text

alt_text =[]

soup = BeautifulSoup(html, 'html.parser')

searching_img = soup.find_all("img")
for i in searching_img:
	try:
		alt_text.append(i['alt'])
	except:
		alt_text.append("No alternative text provided!")
	
for alt in alt_text:
	print (alt)

if __name__ == "__main__":
    pass
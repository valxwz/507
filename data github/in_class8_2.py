import requests
from bs4 import BeautifulSoup





award_dict={}
award_url={}

baseurl = 'https://www.si.umich.edu'
awardlist_url = baseurl + '/news-events/awards-and-honors'
header = {'User-Agent': 'SI_CLASS'}
page_text = requests.get(awardlist_url, headers=header).text
page_soup = BeautifulSoup(page_text, 'html.parser')
end_url_lst=[]
award_name=[]

content_div = page_soup.find_all(class_='field-item even')
# print (content_div)
for div in content_div:
	if div.find_all('h3') !=[]:
		h3_list=div.find_all('h3')
		# print (h3_list)
		for i in h3_list:
			if i.find('a')!=None:
				award_url[i.find('a').contents[0]]=i.find('a')['href']
				# award_url.key=i.find('a').contents
				# award_url.value=i.find('a')['href']
				# end_url_lst.append(i.find('a')['href'])
				# award_name.append(i.find('a').contents)
# print (end_url_lst)
# print (award_name)
# print ("dict",award_url)

award_detail_url="https://www.si.umich.edu/newsandevents/"

for award in award_url:
	# print (award_url.get(award))
	award_detail_context=requests.get(award_detail_url+award_url.get(award), headers=header).text
	award_detail_soup=BeautifulSoup(award_detail_context,"html.parser")
	award_parag=award_detail_soup.find_all(_class="field-item even")
	# award_parag=award_detail_soup.find("div", {"id":"content-inside"})
	# award_p=award_parag.find_all("p")
	print (award_parag)

	# awards=content_div.find_all('h3')
# print (awards)


# class Find_award(end_url, ):
# 	def __init__(self,name,end_url):
# 		self.name=name
# 		self.end_url=end_url

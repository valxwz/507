# 507 Homework 7 Part 1
import requests
import json
from bs4 import BeautifulSoup

#### Your Part 1 solution goes here ####

# on startup, try to load the cache from file
CACHE_FNAME = 'cache.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()

# if there was no file, no worries. There will be soon!
except:
    CACHE_DICTION = {}



def make_request_using_cache(url, header):
    if url in CACHE_DICTION:
        # print("Getting cached data...")
        return CACHE_DICTION[url]
    else:
        # print("Making a request for new data...")
        # Make the request and cache the new data
        page_text = requests.get(url, headers=header).text
        CACHE_DICTION[url]= page_text
        dumped_json_cache=json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close()
        return CACHE_DICTION[url]

def get_umsi_data(page):
    #### Implement your function here ####
	baseurl="https://www.si.umich.edu"
	catalogurl = baseurl+'/directory?field_person_firstname_value=&field_person_lastname_value=&rid=All'+"&page="+str(page)
	header = {'User-Agent': 'SI_CLASS'}
	page_text = make_request_using_cache(catalogurl, header)
	page_soup = BeautifulSoup(page_text, 'html.parser')
	main_content=page_soup.find(class_="view-content")
	node_num_list=main_content.find_all('a',string="Contact Details")
	# get node url	
	my_sub_dict={}
	my_dict={}
	name_list=[]
	title_list=[]
	email_list=[]
	
	for link in node_num_list:
		node_url=link.get('href')
		person_url=baseurl+node_url
		person_page_text = make_request_using_cache(person_url, header)
		person_page_soup = BeautifulSoup(person_page_text, 'html.parser')
		person_main_content=person_page_soup.find(id="content-inside")
		name= person_main_content.find("h2").contents
		name_list.append(name[0])
		
		email=person_main_content.find("a")["href"].split(":")
		email_list.append(email[1])
		title=person_main_content.find("div",class_="field field-name-field-person-titles field-type-text field-label-hidden").contents[0].contents[0].contents
		title_list.append(title[0])
		for i in range(len(name_list)):
			my_dict[email_list[i]]={"name":name_list[i],"title":title_list[i]}
	return my_dict
	
#### Execute funciton, get_umsi_data, here ####
# dict_file = open("directory_dict.json","w")
final_dict={}
for i in range(14):
	final_dict.update(get_umsi_data(i))

	# write_dict=json.dumps(get_umsi_data(i))
	# with open('directory_dict.json','w') as fp:
	# 	json.dump(get_umsi_data(i),fp)
	# dict_file.write(write_dict)
# dict_file.close() # Close the open file

with open('directory_dict.json','w') as fp:
    json.dump(final_dict,fp)


#### Write out file here #####
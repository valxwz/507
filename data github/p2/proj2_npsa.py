## proj_nps.py
## Skeleton for Project 2 for SI 507
## ~~~ modify this file, but don't rename it ~~~
from secrets import google_places_key
from bs4 import BeautifulSoup
import requests
import json
import plotly.graph_objects as go


CACHE_FNAME = 'stateinfo.json'
try:
	cache_file = open(CACHE_FNAME, 'r')
	cache_contents = cache_file.read()
	CACHE_DICTION = json.loads(cache_contents)
	cache_file.close()

except:
	CACHE_DICTION = {}


def params_unique_combination(baseurl, params):
# 	# keys_list = list(params.keys())
# 	# res = []
# 	# for k in keys_list[2:]:
# 	# 	res.append("{}={}".format(k, params[k]))
	return baseurl + "/" + "/".join(params)



def make_request_using_cache(baseurl,params):
	url = params_unique_combination(baseurl,params)

	## first, look in the cache to see if we already have this data
	if url in CACHE_DICTION:
		print("Getting cached data...")
		return CACHE_DICTION[url]

	## if not, fetch the data afresh, add it to the cache,
	## then write the cache to file
	else:
		print("Making a request for new data...")
		# Make the request and cache the new data
		page_text = requests.get(url).text
		CACHE_DICTION[url]= page_text
		dumped_json_cache = json.dumps(CACHE_DICTION)
		fw = open(CACHE_FNAME,"w")
		fw.write(dumped_json_cache)
		fw.close() # Close the open file
		return CACHE_DICTION[url]




## you can, and should add to and modify this class any way you see fit
## you can add attributes and modify the __init__ parameters,
##   as long as tests still pass
##
## the starter code is here just to make the tests run (and fail)
class NationalSite():
	def __init__(self, park_type, name, desc=None, url=None,address_street=None,address_city=None,address_state=None,address_zip=None):
		self.type = park_type
		self.name = name
		self.description = desc
		self.url = url

		# needs to be changed, obvi.
		self.address_street = address_street
		self.address_city = address_city
		self.address_state = address_state
		self.address_zip = address_zip
	def __str__(self):
		s = "%s (%s): %s, %s, %s %s"%(self.name,self.type,self.address_street, self.address_city,self.address_state, self.address_zip)
		return s

## you can, and should add to and modify this class any way you see fit
## you can add attributes and modify the __init__ parameters,
##   as long as tests still pass
##
## the starter code is here just to make the tests run (and fail)
class NearbyPlace():
	def __init__(self, name,lat,lng):
		self.name = name
		self.lat=lat
		self.lng=lng
	def __str__(self):
		return self.name

## Must return the list of NationalSites for the specified state
## param: the 2-letter state abbreviation, lowercase
##        (OK to make it work for uppercase too)
## returns: list of all of the NationalSites
##        (e.g., National Parks, National Heritage Sites, etc.) that are listed
##        for the state at nps.gov
## first, look in the cache to see if we already have this data
def get_sites_for_state(state_abbr):
	state_abbr_lower=state_abbr.lower()
	baseurl="https://www.nps.gov"
	# site_url=baseurl+state_abbr+"/index.html"
	page_text=make_request_using_cache(baseurl,["state",state_abbr_lower,"index.htm"])
	page_soup=BeautifulSoup(page_text, 'html.parser')
	park_list=page_soup.find("ul",{"id":"list_parks"})
	park_names=[]
	for a in park_list.find_all('h3'):
		park_names.append(a)
	park_address_list=[]
	for i in park_names:
		name=i.find('a').contents
		link=i.find('a')['href']
		park_detail_text=make_request_using_cache(baseurl,[link,"index.htm"])
		site_detail_url=baseurl+"/"+link+"/index.htm"
		park_details_soup=BeautifulSoup(park_detail_text,'html.parser')
		park_name=park_details_soup.find(class_="Hero-title").contents[0]
		try:
			park_type=park_details_soup.find(class_="Hero-designation").contents[0]
		except:
			park_type=" "
		park_desc=park_details_soup.find("p")
		address=park_details_soup.find(class_="adr").find_all("span")
		try:
			street=park_details_soup.find(itemprop="streetAddress").contents[0].strip("\n")
		except:
			street=" "
		city=park_details_soup.find("span",itemprop="addressLocality").contents[0]
		state=address[3].contents[0]
		postcode=park_details_soup.find(itemprop="postalCode").contents[0].strip(" ")

		# test a park
		
		# full_address=[park_name,park_type,street,city,state,postcode]
		site_obj=NationalSite(park_type,park_name,park_desc,site_detail_url,street,city,state,postcode)
		park_address_list.append(site_obj)
	return park_address_list

		


## Must return the list of NearbyPlaces for the specific NationalSite
## param: a NationalSite object
## returns: a list of NearbyPlaces within 10km of the given site
##          if the site is not found by a Google Places search, this should
##          return an empty list


def get_url_for_gapi(park_detail_obj):
		baseurl = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input='"
		params=[]
		url=""
		type_param=""
		name_param=""
		name_list=park_detail_obj.name.split(" ")
		for i in name_list:
			name_param+=i+"%20"
		try:
			type_list=park_detail_obj.type.split(" ")
			for i in type_list:
				type_param+=i+"%20"
			url+=baseurl+name_param+"&inputtype=textquery&fields=name,geometry"+"&"+type_param+"&key="+google_places_key
		except:
			type_param=""
			url+=baseurl+name_param+"&inputtype=textquery&fields=name,geometry"+"&key="+google_places_key
		
		
		return url



GOOGLE_FCACHE="google_cache.json"
try:
	gcache_file = open(GOOGLE_FCACHE, 'r')
	gcache_contents = gcache_file.read()
	GCACHE_DICTION = json.loads(gcache_contents)
	gcache_file.close()
except:
	GCACHE_DICTION = {}

def call_google_with_cache(google_url):
	# print(google_url)
	page_text = requests.get(google_url).text

	if google_url in GCACHE_DICTION:
		print("Getting cached data...")
		return GCACHE_DICTION[google_url]

	else:
		print("Making a request for new data...")
		page_text = requests.get(google_url).text
		GCACHE_DICTION[google_url]= page_text
		gdumped_json_cache = json.dumps(GCACHE_DICTION)
		fw = open(GOOGLE_FCACHE,"w")
		fw.write(gdumped_json_cache)
		fw.close() # Close the open file
		return GCACHE_DICTION[google_url]


def get_nearby_places_for_site(national_site):
	url=get_url_for_gapi(national_site)
	park_geometry_text=call_google_with_cache(url)
	coordinate = json.loads(park_geometry_text)["candidates"][0]["geometry"]["location"]
	lat=coordinate['lat']
	lng=coordinate['lng']
	sear_nearby_url="https://maps.googleapis.com/maps/api/place/nearbysearch/json?location="
	sear_nearby_url+=str(lat)+","+str(lng)+"&radius=10000"+"&key="+google_places_key
	nearby_text=call_google_with_cache(sear_nearby_url)
	google_dict = json.loads(nearby_text)["results"]
	places_nearby=[]
	for i in google_dict:
		places_nearby.append(NearbyPlace(i["name"],i["geometry"]["location"]["lat"],i["geometry"]["location"]["lng"]))
	return places_nearby

# site1 = NationalSite('National Monument','Sunset Crater Volcano', 'A volcano in a crater.')
# for i in get_nearby_places_for_site(site1):
# 	print (i.name)
# site1 = NationalSite('National Monument','Sunset Crater Volcano', 'A volcano in a crater.')
# get_url_for_gapi(site1)







## Must plot all of the NationalSites listed for the state on nps.gov
## Note that some NationalSites might actually be located outside the state.
## If any NationalSites are not found by the Google Places API they should
##  be ignored.
## param: the 2-letter state abbreviation
## returns: nothing
## what it needs to do: launches a page with a plotly map in the web browser
def plot_sites_for_state(state_abbr):
	state_abbr_lower=state_abbr.lower()
	site_lst=get_sites_for_state(state_abbr_lower)
	latlst=[]
	lnglst=[]
	park_map_textlst=[]
	for i in site_lst:
		parkname=i.name
		parktype=i.type
		park_map_text=parkname+" "+parktype
		park_map_textlst.append(park_map_text)
		url=get_url_for_gapi(NationalSite(parktype,parkname))
		parks_geometry_text=call_google_with_cache(url)
		try:
			coordinate = json.loads(parks_geometry_text)["candidates"][0]["geometry"]["location"]
			lat=coordinate['lat']
			if lat!=" ":
				latlst.append(lat)
			else:
				print ("no lat")
			lng=coordinate['lng']
			if lng!=" ":
				lnglst.append(lng)
			else:
				print ("no lng")
		except:
			print ("This place doesn't have coordinate.")
	min_lat=min(latlst)
	min_lng=min(lnglst)
	max_lat=max(latlst)
	max_lng=max(lnglst)

	fig = go.Figure(data=go.Scattergeo(
		lon = lnglst,
		lat = latlst,
		mode = 'markers',
		marker_color = "red",
		text=park_map_textlst,
		marker=dict(size = 15,
			symbol = 'star')
		))
	fig.update_layout(
		title = 'Parks in '+state_abbr,
		geo_scope='usa',
		geo = dict(
			projection_type='albers usa',
			showland = True,
			landcolor = "rgb(254, 227, 136)",
			subunitcolor = "rgb(217, 217, 217)",
			countrycolor = "rgb(217, 100, 217)",
			lakecolor = "rgb(130, 160, 250)",
			showlakes = True,
			lataxis = dict(range = [min_lat-1,max_lat+1]),
			lonaxis = dict(range = [min_lng-1,max_lng+1]),
			center= {'lat': (min_lat+max_lat)/2, 'lon': (min_lng+max_lng)/2 },
			countrywidth = 3,
			subunitwidth = 3
		))
	fig.show()

## Must plot up to 20 of the NearbyPlaces found using the Google Places API
## param: the NationalSite around which to search
## returns: nothing
## what it needs to do: launches a page with a plotly map in the web browser



def plot_nearby_for_site(site_object):
	url=get_url_for_gapi(site_object)
	park_geometry_text=call_google_with_cache(url)
	coordinate = json.loads(park_geometry_text)["candidates"][0]["geometry"]["location"]
	site_name = json.loads(park_geometry_text)["candidates"][0]["name"]
	site_lat=coordinate['lat']
	site_lng=coordinate['lng']


	places_nearby=get_nearby_places_for_site(site_object)
	latlst=[]
	lnglst=[]	
	park_map_textlst=[]
	color_lst=[]
	make_symbol_lst=[]
	size_lst=[]
	latlst.append(site_lat)
	lnglst.append(site_lng)
	color_lst.append("blue")
	make_symbol_lst.append("star")
	park_map_textlst.append(site_name)
	size_lst.append(15)

	for objectitem in places_nearby:
		latlst.append(objectitem.lat)
		lnglst.append(objectitem.lng)
		park_map_textlst.append(objectitem.name)
		color_lst.append("red")
		make_symbol_lst.append("circle")
		size_lst.append(12)


	min_lat=min(latlst)
	min_lng=min(lnglst)
	max_lat=max(latlst)
	max_lng=max(lnglst)

	fig = go.Figure(data=go.Scattergeo(
		lon = lnglst,
		lat = latlst,
		text=park_map_textlst,
		mode = 'markers',
		marker_color=color_lst,

		marker = dict(
			opacity = 0.8,
			symbol = make_symbol_lst,
			color = color_lst,
			size=size_lst)
		))
	fig.update_layout(
		title = "Locations near "+site_name,
		geo_scope='usa',
		geo = dict(
			projection_type='albers usa',
			showland = True,
			landcolor = "rgb(254, 227, 136)",
			subunitcolor = "rgb(217, 217, 217)",
			countrycolor = "rgb(217, 100, 217)",
			lakecolor = "rgb(130, 160, 250)",
			showlakes = True,
			lataxis = dict(range = [min_lat-0.01,max_lat+0.01]),
			lonaxis = dict(range = [min_lng-0.01,max_lng+0.01]),
			center= {'lat': (min_lat+max_lat)/2, 'lon': (min_lng+max_lng)/2 },
			countrywidth = 3,
			subunitwidth = 3
		))
	fig.show()
site1 = NationalSite('National Monument',
			'Sunset Crater Volcano', 'A volcano in a crater.')



if __name__ == "__main__":
	sites = []
	state_abbr = ""
	site_objective = ""

	while True:
		userinput = input("Enter command or 'help' for options:")
		command = userinput.split()

		if command[0] == 'list':
			if len(command) != 2:
				print("The input is invalid, please try again.")
			else:
				state_abbr = command[1]
				# try:
				sites = get_sites_for_state(state_abbr)
				print("National Sites in " + state_abbr+"\n")
				number = 0
				for site in sites:
					number += 1
					site_address_str=NationalSite(site.name, site.type,site.address_street, site.address_city,site.address_state, site.address_zip)
					print(str(number) + ") " + str(site_address_str))
				# except:
				# 	print ("Check your input. Try again")

		elif command[0] == 'nearby':
			if len(sites) == 0:
				print("The result set is empty, please use 'list' command first.")
			elif len(command) != 2 or int(command[1]) < 1 or int(command[1]) > len(sites):
				print("The input is invalid, please try again.")
			else:
				site_type=sites[int(command[1])-1].type
				type_name=sites[int(command[1])-1].name
				site_objective = NationalSite(site_type,type_name)
				print("Places near " + site_objective.name + " " + site_objective.type+"\n")
				nearby_places = get_nearby_places_for_site(site_objective)
				number = 0
				for place in nearby_places:
					number += 1
					print(str(number) + ") " + str(place))

		elif command[0] == "map":
			if site_objective!="":
				plot_nearby_for_site(site_objective)
			if state_abbr!="":
				plot_sites_for_state(state_abbr)
			else:
				print("No related map can be showen. Please try 'list' or 'nearby' command first.")

		elif command[0] == 'exit':
			print('Thank you. Hope you enjoyed the program.')
			break

		elif command[0] == 'help':
			print('''
				If you want to search parks by state:
				type: list <state abbrevation>
					This will show you a list of parks in a state. 
					always available as possible input
					result:all National Sites in a state, with numbers beside them
					valid inputs: a two-letter state abbreviation

				If you want to check places around a park:
				type: nearby <result_number (of the park from the previous list>
					available only if there is an active result set
					result: lists all Places nearby a given result
					valid inputs: an integer (that is included in the list)

				If you want to view both the maps of parks in the state you entered 
				and the nearby places you searched:
				type: map
					available only if there is an active result set
					displays the current results (if any) on a map
				
				other options:

				exit
					exits the program
				help
					lists available commands
					''')

		else:
			print("The input is invalid, please try again.")










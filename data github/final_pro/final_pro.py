import requests
import json
import secret
import plotly
import plotly.graph_objs as go
import sqlite3
from bs4 import BeautifulSoup
import pandas as pd
import us_city_to_state as city_state
import webbrowser


# ----------------
# 1. Get information from Yelp Fusion
# ----------------

client_id=secret.CLIENT_ID
api_key=secret.API_KEY
headers={'Authorization': 'Bearer %s' % api_key}

search_url = 'https://api.yelp.com/v3/businesses/search'

CACHE_FNAME="sample.json"
print (
	""""
	Thinking about opening a new restaurant 
	and playing your fav songs at your site?
	You can checkout your competitors on a map, check parking space nearby, and save songs to play at your site!
	To start, answer the following questions.""")


# ------------
# 1. first get user's input of the following information 
# ---------

term=input("What type of food will you serve? eg. salad, coffee, etc... ").lower()
city=input("Which city do you plan to open your restaurant? ").lower()
state=input("Which state is it? Type its abbreviation, or type 'exit' to see other command ").lower()
states_lst = ['al', 'ak', 'az', 'ar', 'ca', 'co', 
'ct', 'dc', 'de', 'fl', 'ga', 'hi', 'id', 'il', 'in', 'ia', 
'ks', 'ky', 'la', 'me', 'md', 'ma', 'mi', 'mn', 'ms', 'mo', 
'mt', 'ne', 'nv', 'nh', 'nj', 'nm', 'ny', 'nc', 'nd', 'oh', 'ok', 'or', 
'pa', 'ri', 'sc', 'sd', 'tn', 'tx', 'ut', 'vt', 'va', 'wa', 'wv', 'wi', 'wy']

# validate city and state input
while city.title() not in city_state.city_to_state_dict.keys() or state not in states_lst:
	print ("Invalid state or city name. Try again.")
	city=input("Which city do you plan to open your restaurant? ").lower()
	state=input("Which state is it? Or type 'exit' to see other command ").lower()


# params that would be used in yelp fusion api
params = {'term':term,'location':city,'radius':'5000','limit':'15','sort_by':'rating'}

try:
	cache_file = open(CACHE_FNAME, 'r')
	cache_contents = cache_file.read()
	CACHE_DICTION = json.loads(cache_contents)
	cache_file.close()

except:
	CACHE_DICTION = {}

def params_unique_combination(baseurl, params):
	keys_list = list(params.keys())
	res = []
	for k in keys_list:
		res.append("{}={}".format(k, params[k]))
	return baseurl + "/" + "/".join(res)

def make_request_using_cache(baseurl,params):
	unique_ident = params_unique_combination(baseurl,params)

	## first, look in the cache to see if we already have this data
	if unique_ident in CACHE_DICTION:
		print ("Getting data from cache.")
		try:
			# if there's no result
			if CACHE_DICTION[unique_ident]['total']==0:
				print ("No results. Please try somthing else.")
			else:
				return CACHE_DICTION[unique_ident]
		except:
			# if there's an error
			if CACHE_DICTION[unique_ident]["error"]:
				print (CACHE_DICTION[unique_ident]["error"]["description"])
			else:
				print ("Somthing went wrong. Try again.")
		
	else:
		print("Making a request for new data...")
		# Make the request and cache the new data
		CACHE_FNAME = 'sample.json'
		req=requests.get(search_url, params=params, headers=headers)
		results=json.loads(req.text)
		CACHE_DICTION[unique_ident] = results
		dumped_json_cache = json.dumps(CACHE_DICTION)
		fw = open(CACHE_FNAME,"w")
		fw.write(dumped_json_cache)
		fw.close() # Close the open file
		
		# check if 0 result returned from api
		try:
			if results['total']==0:
				print ("No results. Please try somthing else.")
			else:
				print('Data saved')
		except:
			if results["error"]:
				print (results["error"]["description"])
			else:
				print ("Somthing went wrong. Try again.")

		

		return CACHE_DICTION[unique_ident]




# ---------------------
# 2. getting information from yelp and dump into a json file, which is also a cache file. 
# ---------------------

def get_venue_info(businesses_dict):
	venue_dict={}
	try:
		for bus in businesses_dict["businesses"]:
			venue_dict[bus["id"]]={"name":bus["name"],"img":bus["image_url"],
			"place_url":bus["url"],"price":bus["price"],"location":" ".join(bus["location"]["display_address"]),
			"rating":bus["rating"],
			"latitude":bus["coordinates"]["latitude"],"longitude":bus["coordinates"]["longitude"]}
	except:
		pass
	DB_FNAME = 'db.json'
	dumped_json_cache = json.dumps(venue_dict)
	fw = open(DB_FNAME,"w")
	fw.write(dumped_json_cache)
	fw.close() # Close the open file
	return venue_dict

# -------------
# # 4. user will later enter site address they wan to save. 
# here we get lat lng for your saved place
# ----------------
# NOTE!!!!
# I realized Google api will somehow auto correct the address input. for example, if I search 
# "800 n. liberty str, ann arbor, mo", 
# it would correct "mo" to "mi" and return "800 n. liberty str, ann arbor, mi" location


def get_url_for_gapi(choosen_address):
		baseurl = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input='"
		url=""
		name_param=""
		name_list=choosen_address.split(" ")
		for i in name_list:
			name_param+=i+"%20"
		url+=baseurl+name_param+"&inputtype=textquery&fields=name,geometry"+"&key="+secret.google_places_key		
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

def get_site_location(choosen_address):
	url=get_url_for_gapi(choosen_address)
	park_geometry_text=call_google_with_cache(url)
	coordinate = json.loads(park_geometry_text)["candidates"][0]["geometry"]["location"]
	lat=coordinate['lat']
	lng=coordinate['lng']
	return [lat,lng]

# -----------------
# # 5. get music from the Billboard webpage
# this function will load the real time first 100 songs into the a dictionary
# lator user will be able to pick a song from here
# # -------------------

def get_music(num_of_songs):
	music_dict={}
	rank_lst=[]
	name_lst=[]
	artist_lst=[]
	page_text=requests.get("https://www.billboard.com/charts/hot-100").text
	page_soup=BeautifulSoup(page_text, 'html.parser')
	name=page_soup.find_all(class_="chart-element__information__song text--truncate color--primary")[0:int(num_of_songs)]
	artist=page_soup.find_all(class_="chart-element__information__artist text--truncate color--secondary")[0:int(num_of_songs)]
	rank=page_soup.find_all(class_="chart-element__rank__number")[0:int(num_of_songs)]
	for i in rank:
		rank_lst.append(i.get_text())
	for i in name:
		name_lst.append(i.get_text())
	for i in artist:
		artist_lst.append(i.get_text())
	for i in range(len(name_lst)):
		music_dict[rank_lst[i]]={"name":name_lst[i],"artist":artist_lst[i]}
	return music_dict

# -------------------
# 6. create tables: 
		# 1. competitor table. user pick an competitor from results that's returned from yelp 
		# the competitor will be saved in db
		# 2. music table. user pick a song from top 100 music list, that's returned from Billboard webpage
		# The picked music will be saved in db
		# 3. choosen_site table. user will enter a site address where they plan to locate their
		#  new restaurant. This site address will be saved in this table.
		# 4. music_site table. 
		# user will be able to pick a music that has been saved at the music table.
		# and pick a site that has been saved at the choosen_site table.
		# the music and site will be mapped in this music_site table 
# ---------------------

DBNAME = 'site_choosing_music.db'
DBENTRY="db.json"

def create_table():
	conn = sqlite3.connect(DBNAME)
	cur = conn.cursor()
	cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='competitor' ''')
	result = cur.fetchone()
	if result[0]==1:
		print ("table competitor has been created.")
	else:
		statement="""
		CREATE TABLE 'competitor' (
	  'id' INTEGER PRIMARY KEY AUTOINCREMENT,
	  'name' TEXT,
	  'place_url' text,
	  'location' TEXT,
	  'rating' Real,
	  'price' Real
	); 
	"""
		cur.execute(statement)
		conn.commit()
		print ("Table Competitor just created.")

	cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='music' ''')
	result = cur.fetchone()
	if result[0]==1:
		print ("table music has been created.")
	else:
		statement="""
		CREATE TABLE music (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		name TEXT,
		artist INT,
		rank TEXT
		); 

		"""
		cur.execute(statement)
		conn.commit()
		print ("Table artist just created.")
	cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='choosen_site' ''')
	result = cur.fetchone()
	if result[0]==1:
		print ("table choosen_site has been created.")
	else:
		statement="""
		CREATE TABLE choosen_site (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		address TEXT
		); 

		"""
		cur.execute(statement)
		conn.commit()
		print ("Table choosen_site just created.")
	cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='music_site' ''')
	result = cur.fetchone()
	if result[0]==1:
		print ("table music_site has been created.")
	else:
		statement="""
		CREATE TABLE music_site (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		choosen_music_id INT,
		to_site_id INT,
		FOREIGN KEY (to_site_id) REFERENCES choosen_site(id)
		FOREIGN KEY (choosen_music_id) REFERENCES music(id)
		); 

		"""
		cur.execute(statement)
		conn.commit()
		print ("Table music_site just created.")
	# clear any old data
	# delete_stmt="DELETE FROM competitor"
	# cur.execute(delete_stmt)
	# conn.commit()
	# delete_stmt="DELETE FROM music"
	# cur.execute(delete_stmt)
	# conn.commit()
	# delete_stmt="DELETE FROM choosen_site"
	# cur.execute(delete_stmt)
	# conn.commit()
	# delete_stmt="DELETE FROM music_site"
	# cur.execute(delete_stmt)
	# conn.commit()

	conn.close()

create_table()


# create data entry

# competitors data
place_name=[]
place_url=[]
price=[]
location=[]
rating=[]

# load all data that's retturned from yelp to the list
try:
	with open('db.json') as json_file:
		data=json.load(json_file)
		# print (data)
	for i in data:
		data_entry=(data[i])
		place_name.append(data_entry["name"])
		place_url.append(data_entry["place_url"])
		location.append(data_entry["location"])
		rating.append(data_entry["rating"])
		price.append(data_entry["price"])
except:
	pass



saved_places=[]

# insert data into tables 	
def insert_to_competitor():
	# show available competitors from the city
	print (""""
		Here are some competitors in your city.
		Please pick one to save as your competitor.
		eg. '0' will save the frist competotor's information. 
		""")
	data = {'Name':place_name,
			'Address':location,
			"Rating":rating,
			"Price":price}
	df = pd.DataFrame(data)
	print(df)
	# clean the db before inserting any data
	conn = sqlite3.connect(DBNAME)
	cur = conn.cursor()
	num_picked=""
	while num_picked!="more":
		num_picked=input("Please type your choice, or type 'more' to see other command: ")
		try:
			num_picked=int(num_picked)
			# check to make sure the same competitor wasn't saved twice
			if num_picked not in saved_places:
				insertion = (None, place_name[num_picked], place_url[num_picked], location[num_picked],rating[num_picked],price[num_picked])
				statement='INSERT INTO "competitor" '
				statement+='VALUES(?,?,?,?,?,?)'
				cur.execute(statement, insertion)
				conn.commit()
				print ("New competitor has been saved.")
				# add the new competitor name into the competitor_name list
				saved_places.append(num_picked)
				# give user an option to view the competitor's detail on yelp
				view_comp_in_yelp=input("Would you like to view this competitor's detail on yelp? y/n? ")
				if view_comp_in_yelp.lower()=="y":
					webbrowser.open_new_tab(place_url[num_picked])
					webbrowser.open_new(url)
				elif view_comp_in_yelp.lower()=="n":
					print ("Sure.")
					break
				else:
					print ("Invalid input. Pass.")

			else:
				print ("This competitor has been saved. Try another one.")
		except:
			pass

	statement="""
	SELECT name from competitor where name='"""+place_name[int(num_picked)]+"'"
	print (statement)
	results=cur.execute(statement)
	conn.commit()
	competitor_saved=results.fetchall()
	conn.close()
	return competitor_saved

# music data

song=[]
artist=[]
rank=[]
try:
	music_dict=get_music(50)
	for i in music_dict:
		rank.append(i)
		song.append(music_dict[i]["name"])
		artist.append(music_dict[i]["artist"])
except:
	pass


# ------------
# users are able to pick a pop music to save in the db
# -------------
saved_music_id=[]
def insert_to_music():
	# show available competitors from the city
	print (""""
		Here are top 50 music on Billboard.
		Please pick one to save as your favorite music.
		eg. '1' will save the first song. 
		""")
	data = {'Rank':rank,
			'Song':song,
			"Artist":artist}
	df = pd.DataFrame(data)
	print(df.to_string(index=False))
	# clean the db before inserting any data
	conn = sqlite3.connect(DBNAME)
	cur = conn.cursor()
	num_picked=""
	while num_picked!="more":
			# load song's rank from existed music data. Check if the song has been saved
		num_picked=input("Please type your choice, or type 'more' to try other command: ")
		if num_picked!="more":
			select_stmt="select rank from music where rank ="+str((int(num_picked)))
			results=cur.execute(select_stmt)
			results=results.fetchall()
			if results==[]:
			# means the song picked has not been saved yet
				# try:
				num_picked=int(num_picked)			
				saved_music_id.append(num_picked)
				insertion = (None, song[num_picked], artist[num_picked], rank[num_picked])
				statement='INSERT INTO "music" '
				statement+='VALUES(?,?,?,?)'
				cur.execute(statement, insertion)
				conn.commit()
				print ("New song is saved in your list.")
				# except:
				# 	print ("Invalid input. Please try again.")
				# 	continue
			else:
				print ("This song has been saved. Try another one.")
		else:
			break
	return saved_music_id		
	conn.close()

# ---------
# users are able to enter an address as picked site and save into db
# ---------

choosen_address_list=[]

def insert_to_choosen_site():
	print ("""
		Where are you thinking to open the restaurant right now?
		Let's first save the site you chose.""")
	conn = sqlite3.connect(DBNAME)
	cur = conn.cursor()
	street=input(
		"Which street is it? Type the full street name. Or type 'pass' if you have no idea yet.")
	while street!="pass":	
		street_address=street.lower()+" "+city.lower()+" "+state.lower()	
		# check if the address input has been saved into db before 
		statement="SELECT address FROM choosen_site WHERE address='"+str(street_address)+"'"
		saved_addresses=cur.execute(statement).fetchall()
		conn.commit()	
		if saved_addresses==[]:
			print ("The address you entered is new. Saving to database now.")
			try:
				choosen_address_list.append(street_address)
				results=get_site_location(street_address)
				print (results)
				insertion = (None, street_address)
				statement='INSERT INTO "choosen_site" '
				statement+='VALUES(?,?)'
				cur.execute(statement, insertion)
				conn.commit()
				another_site=input("The site has been saved. Would you like to save another site you chose? Type 'y/n'. ")
				if another_site.lower()=="y":
					street=input("Which street is it? Type the full street name.")
				else:
					break
			except:
				print ("invalid address, try again")
				street=input("Which street is it? Type the full street name.")
		else:
			print ("The address you entered is existed in the database. Enter another new address to.")
			street=input(
		"Which street is it? Type the full street name. Or type 'pass' if you have no idea yet.")

	conn.close()
	return choosen_address_list

# first, ask user to save the site address he currently has in mind		
insert_to_choosen_site()


# empty list to track if user is keeping adding the same combination of song and site
chosen_pair=[]	
def insert_music_site():
	# show music and choosen_site table
	end=False
	valid_data_returned=True
	while end==False:
		conn = sqlite3.connect(DBNAME)
		cur = conn.cursor()
		# show music
		statement="""
			select id, name, artist, rank from music
			"""
		results=cur.execute(statement)
		conn.commit()
		results=results.fetchall()
		if results!=[]:
			print ("Here are the music you saved.")
			music_name=[]
			artist=[]
			rank=[]
			music_id=[]
			for i in results:
				music_id.append(i[0])
				music_name.append(i[1])
				artist.append(i[2])
				rank.append(i[3])
			data={"Music_id":music_id,
			"Song":music_name,
			"Artist":artist,
			"Rank":rank}
			df = pd.DataFrame(data)
			print(df.to_string(index=False))
			valid_data_returned=True
			# pick a song that you want to matched with a site you chose
			song_to_match=input("From the list above, pick a song that you want to matched with a site you chose. Type its number. ")
		else:
			print ("No music saved yet. Please pick some music first.")
			valid_data_returned=False
			break
		# show site you chose
		# pick a site to match the song to 
		statement="""
		select id, address from choosen_site
		"""
		site_results=cur.execute(statement)
		conn.commit()
		site_add=[]
		site_id=[]
		site_results=site_results.fetchall()
		if site_results!=[]:
			print ("Here are the site you chose.")
			for i in site_results:
				site_add.append(i[1])
				site_id.append(i[0])
			data={"Site_ID":site_id,
			"Address":site_add}
			df = pd.DataFrame(data)
			print(df.to_string(index=False))
			valid_data_returned=True
			site_to_match=input("From the site you chose above, pick a site you want to save the song to. Type its number. ")
		else:
			print ("No site saved yet. Please save some sties first.")
			valid_data_returned=False
			break
		# insert to music_site table
		if valid_data_returned==True:
			choosen_music_id=int(song_to_match)
			to_site_id=int(site_to_match)
			if choosen_music_id in music_id and to_site_id in site_id and [choosen_music_id,site_id] not in chosen_pair:
				# add chosen music-site combination
				chosen_pair.append([choosen_music_id,site_id])
				insertion = (None, int(int(song_to_match)),int(int(site_to_match)))
				statement='INSERT INTO "music_site" '
				statement+='VALUES(?,?,?)'
				cur.execute(statement, insertion)
				conn.commit()
				print ("A song has been matched to a site.")
				break
			else:
				print ("Invalid pick, please try again.")
		else:
			pass

	conn.close()
	return chosen_pair

# present choosen_site
def present_choosen_site():
	conn = sqlite3.connect(DBNAME)
	cur = conn.cursor()
	# show all choosen_site
	statement="""
			select address from choosen_site
			"""
	results=cur.execute(statement)
	conn.commit()
	if results!=[]:
		results=results.fetchall()
		saved_addresses=[]
		print ("Here're the addresses you saved as your choosen site: ")
		for i in results:
			saved_addresses.append(i[0])
		data = {
			'Site':saved_addresses}
		df = pd.DataFrame(data)
		print(df)
		return results
	else:
		return "You haven't save any site. Enter a site to save first."
	conn.close()

# present songs saved
def present_songs():
	conn = sqlite3.connect(DBNAME)
	cur = conn.cursor()
	# show all choosen_site
	statement="""
			select name, artist, rank from music
			"""
	results=cur.execute(statement)
	conn.commit()
	if results!=[]:
		song_name=[]
		artist_name=[]
		rank_saved=[]
		results=results.fetchall()
		print ("Here're the songs you saved")
		for i in results:
			song_name.append(i[0])
			artist_name.append(i[1])
			rank_saved.append(i[2])
				
		data = {
			"Rank":rank_saved,
			'Song':song_name,
			"Artist":artist_name}
		df = pd.DataFrame(data)
		print(df.to_string(index=False))
	else:
		print ("You haven't save any song. Save a song first.")
	conn.close()
	return results


# open the song's webpage in Billboard
def pick_a_song():
	conn = sqlite3.connect(DBNAME)
	cur = conn.cursor()
	# show music
	statement="""
		select name, artist, rank from music
		"""
	results=cur.execute(statement)
	conn.commit()
	results=results.fetchall()
	if results!=[]:
		print ("Here are the music you saved.")
		name=[]
		artist=[]
		rank=[]
		print (results)
		for i in results:
			name.append(i[0])
			artist.append(i[1])
			rank.append(i[2])
		data={"Rank":rank,
		"Song":name,
		"Artist":artist
		}
		df = pd.DataFrame(data)
		print(df.to_string(index=False))
	picked_rank=input("pick a you want to listen by typing its rank: ")
	url = 'https://www.billboard.com/charts/hot-100?rank='+picked_rank

	# Open URL in a new tab, if a browser window is already open.
	webbrowser.open_new_tab(url)

	# Open URL in new window, raising the window if possible.
	webbrowser.open_new(url)


	return picked_rank

# search parking lot

def search_parking(city):
	location=[]
	params = dict(
	client_id="OXYL1X2AN13UMGCPELY1V5S4JHUKIKLQX2SJI3SBCCYN5Y50", 
	client_secret="R3YJVCP2XG2AWF3H4L2T42GFDF2VHIY3BDDMSRILY2OWIHB1",
	v='20191206',
	near=city,
	query="parking lot",
	limit=20)
	CACHE_FNAME = 'parking.json'
	try:
		cache_file = open(CACHE_FNAME, 'r')
		cache_contents = cache_file.read()
		CACHE_DICTION = json.loads(cache_contents)
		cache_file.close()

	except:
		CACHE_DICTION = {}
	foursquare_url = 'https://api.foursquare.com/v2/venues/search'
	keys_list = list(params.keys())
	res = []
	for k in keys_list[2:]:
		res.append("{}={}".format(k, params[k]))
	unique_ident=foursquare_url + "/" + "/".join(res)
	# make parking lot cache
	if unique_ident in CACHE_DICTION:
		print("Getting cached data...")
		venue_lst=CACHE_DICTION[unique_ident]["response"]["venues"]

	else:
		print("Making a request for new data...")
		# Make the request and cache the new data
		resp = requests.get(foursquare_url, params)
		data = json.loads(resp.text)
		CACHE_DICTION[unique_ident] = json.loads(resp.text)
		dumped_json_cache = json.dumps(CACHE_DICTION)
		fw = open(CACHE_FNAME,"w")
		fw.write(dumped_json_cache)
		fw.close() # Close the open file
		try:
			venue_lst=CACHE_DICTION[unique_ident]["response"]["venues"]
		except:
			print ("Can't find any parking lot in this city.")
	try:
		for venue in venue_lst:
			parking_name=venue["name"]
			location_info=venue['location']
			lat=location_info['lat']
			lng=location_info['lng']
			location.append([parking_name,lat,lng])
	except:
		print ("Can't find any parking lot in this city.")
	return location



# ----------------
# 3. show places on plotly
# ----------------
# print ("Showing ", term, " places at ", location, " information...")

def show_map(venue_info_dict,choosen_site=[],city=city):
	lat_lst=[]
	lng_lst=[]
	text_lst=[]
	make_symbol_lst=[]
	color_lst=[]
	if venue_info_dict!={}:
		for venue_id in venue_info_dict:			
			value_info=venue_info_dict[venue_id]
			lat_lst.append(value_info["latitude"])
			lng_lst.append(value_info["longitude"])
			text_lst.append(value_info["name"]+", "+"Yelp rating "+str(value_info["rating"]))
			make_symbol_lst.append("circle")
			color_lst.append("red")
	else:
		print ("Check your input of restaurant. No such restaurant found.")
	parking_lst=search_parking(city)
	for i in parking_lst:
		lat_lst.append(i[1])
		lng_lst.append(i[2])
		make_symbol_lst.append("circle")
		color_lst.append("blue")
		text_lst.append(i[0])
	# if user has choosen site(s), show the site on map.
	if choosen_site!=[]:
		for i in choosen_site:
			choosen_site_location=get_site_location(i[0])
			lat_lst.append(choosen_site_location[0])
			lng_lst.append(choosen_site_location[1])
			make_symbol_lst.append("star")
			color_lst.append("orange")
			text_lst.append("Your choosen site "+i[0])
	else:
		pass


	mapbox_access_token = secret.MAPBOX_TOKEN
	fig = go.Figure(data=go.Scattergeo(
			lat=lat_lst,
			lon=lng_lst,
			mode='markers',
			marker=dict(
			opacity = 0.8,
			symbol = make_symbol_lst,
			color = color_lst),
			hoverinfo="text",
			hovertext=text_lst
		))

	try:
		min_lat=min(lat_lst)
		max_lat=max(lat_lst)
		min_lng=min(lng_lst)
		max_lng=max(lng_lst)
		print ("Maping your competitors, parking lot, and saved sites on the map.")
		fig.update_layout(
			title="Site Choosing",
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
			)
		)

		fig.show()
	except:
		print ("Something went wrong. Can't show the map.")



def interative_command():
	response=""
	while response.lower() != 'exit':
		response = input('Enter a command, "help", or "exit": ')
		if response.lower()=="help":
			with open('help.txt') as f:
				help_text=f.read()
			print(help_text)
			continue
		elif response.lower()=="exit":
			break
		else:
			if response.lower()=="map":
				show_map(venue_info_dict=get_venue_info(make_request_using_cache(search_url,params)),choosen_site=present_choosen_site(),city=city)
			elif response.lower()=="add_site":
				insert_to_choosen_site()
			elif response.lower()=="save_competitors":
				insert_to_competitor()
			elif response.lower()=="save_music":
				insert_to_music()
			elif response.lower()=="map_music_to_site":
				insert_music_site()
			elif response.lower()=="listen":
				pick_a_song()
			elif response.lower()=="show_my_songs":
				present_songs()
			elif response.lower()=="show_my_sites":
				present_choosen_site()
			else:
				print ("Invalid command. Please try another command. ")
				continue


if __name__=="__main__":
    interative_command()













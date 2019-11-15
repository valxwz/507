import requests
import json
import secret
import plotly
import plotly.graph_objs as go
from requests_oauthlib import OAuth1

# ----------------------------------------------
# Part 1: Get photo information using Flickr API
# ----------------------------------------------


print("----------------Part1--------------------")

city=input("Which city do you want to search for?")
place=input("What kind of places do you want to search?")


client_id=secret.CLIENT_ID
client_secret=secret.CLIENT_SECRET


search_url = 'https://api.foursquare.com/v2/venues/search'

params = dict(
	client_id=client_id, 
	client_secret=client_secret,
	v='20191103',
	near=city,
	query=place,
	limit=25)


params_photo = dict(
	client_id=client_id, 
	client_secret=client_secret,
	v='20191103',
	limit=1)

CACHE_FNAME = 'foursquare_cache.json'
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
    for k in keys_list[2:]:
        res.append("{}={}".format(k, params[k]))
    return baseurl + "/" + "/".join(res)



def make_request_using_cache(baseurl,params):
	unique_ident = params_unique_combination(baseurl,params)

	## first, look in the cache to see if we already have this data
	if unique_ident in CACHE_DICTION:
		print("Getting cached data...")
		return CACHE_DICTION[unique_ident]

	## if not, fetch the data afresh, add it to the cache,
	## then write the cache to file
	else:
		print("Making a request for new data...")
		# Make the request and cache the new data
		resp = requests.get(baseurl, params)
		data = json.loads(resp.text)
		CACHE_DICTION[unique_ident] = json.loads(resp.text)
		dumped_json_cache = json.dumps(CACHE_DICTION)
		fw = open(CACHE_FNAME,"w")
		fw.write(dumped_json_cache)
		fw.close() # Close the open file
		return CACHE_DICTION[unique_ident]

def get_venue_info(url,params):
	venue_dict={}
	try:
		venue_lst=make_request_using_cache(url,params)["response"]["venues"]
		for venue in venue_lst:
			venue_photo_url="https://api.foursquare.com/v2/venues/"+venue['id']+"/photos"
			photo_dict=make_request_using_cache(venue_photo_url,params_photo)
			if photo_dict['response']!={}:
				photo_item=photo_dict['response']['photos']['items']
				if photo_item!=[]:
					photo_id=photo_item[0]['id']
					photo_url=photo_item[0]['prefix']+str(photo_item[0]['width'])+"*"+str(photo_item[0]['height'])+photo_item[0]['suffix']
			else:
				photo_id=" "
				photo_url= " "
			location_info=venue['location']
			venue_dict[venue['id']]={"name":venue['name'], "location": " ".join(location_info['formattedAddress'][:-1]),'lat':location_info['lat'],
			'lng':location_info['lng'],'photo_id':photo_id, 'photo_url':photo_url}
	except:
		return "Invalid Input"

	return venue_dict


def print_info(venue_dict):
	if venue_dict!="Invalid Input" :
		for i in list(venue_dict.values()):
			print ("Venue: " + i['name']+"\nAddress: "+i['location']+'\nPhoto id: '+i['photo_id']+'\n\n')
	else:
		print ("asdadCheck your input city/place.")



venue_info_dict=get_venue_info(search_url,params)
if venue_info_dict!="Invalid Input":
	print_info(venue_info_dict)
else:
	print ("Invalid Input. No venue founded.")


# ----------------------------------------------
# Part 2: Map data onto Plotly
# ----------------------------------------------



lat_lst=[]
lng_lst=[]
text_lst=[]
if venue_info_dict!="Invalid Input":
	for i in list(venue_info_dict.values()):
		lat_lst.append(i['lat'])
		lng_lst.append(i['lng'])
		text_lst.append(i['name']+' '+i['photo_url'])
else:
	print ("Check your input. No vanue mapped.")

mapbox_access_token = secret.MAPBOX_TOKEN
fig = go.Figure(go.Scattermapbox(
        lat=lat_lst,
        lon=lng_lst,
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=9
        ),
        hovertext=text_lst,
    ))

try:
	min_lat=float(min(lat_lst))
	max_lat=float(max(lat_lst))
	min_lng=float(min(lng_lst))
	max_lng=float(max(lng_lst))
	fig.update_layout(
    autosize=True,
    hovermode='closest',
    mapbox=go.layout.Mapbox(
        accesstoken=mapbox_access_token,
        bearing=0,
        center=go.layout.mapbox.Center(
        	lat=float((min_lat+max_lat)/2),
        	lon=float((min_lng+max_lng)/2)),
        pitch=0,
        zoom=12),
	)

	fig.show()
except:
	pass












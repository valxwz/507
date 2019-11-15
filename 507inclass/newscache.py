#newscache.py
from secrets import *
import requests
import json

# on startup, try to load the cache from file
CACHE_FNAME = 'cache_news.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()

# if there was no file, no worries. There will be soon!
except:
    CACHE_DICTION = {}

# A helper function that accepts 2 parameters
# and returns a string that uniquely represents the request
# that could be made with this info (url + params)
def params_unique_combination(baseurl, params):
    alphabetized_keys = sorted(params.keys())
    res = []
    for k in alphabetized_keys:
        res.append("{}-{}".format(k, params[k]))
    return baseurl + "_".join(res)

# The main cache function: it will always return the result for this
# url+params combo. However, it will first look to see if we have already
# cached the result and, if so, return the result from cache.
# If we haven't cached the result, it will get a new one (and cache it)
def make_request_using_cache(baseurl, params):
    unique_ident = params_unique_combination(baseurl,params)

    ## first, look in the cache to see if we already have this data
    if unique_ident in CACHE_DICTION:
        if is_fresh(CACHE_DICTION[unique_ident]):
            print("Getting cached data...")
            return CACHE_DICTION[unique_ident]

    ## if not, fetch the data afresh, add it to the cache,
    ## then write the cache to file
        else:
            pass
    
    print("Making a request for new data...")
    # Make the request and cache the new data
    resp = requests.get(baseurl, params)
    CACHE_DICTION[unique_ident] = json.loads(resp.text)
    ### THE NEXT LINE IS NEW
    CACHE_DICTION[unique_ident]['cache_timestamp'] = datetime.now().timestamp()
    dumped_json_cache = json.dumps(CACHE_DICTION)
    fw = open(CACHE_FNAME,"w")
    fw.write(dumped_json_cache)
    fw.close() # Close the open file
    return CACHE_DICTION[unique_ident]


MAX_STALENESS = 30 ## 30 seconds--only for lecture demo!
def is_fresh(cache_entry):
    now = datetime.now().timestamp()
    staleness = now - cache_entry['cache_timestamp']
    return staleness < MAX_STALENESS

# gets headlines for today's news
def fetch_top_headlines(category=None):
    baseurl = 'https://newsapi.org/v2/top-headlines'
    params={'country': 'us'}
    if category is not None:
        params['category'] = category
    params['apiKey'] = newsapi_key
    return make_request_using_cache(baseurl, params)

# gets headlines for today's news
def fetch_on_source(source=None):
    baseurl = 'https://newsapi.org/v2/top-headlines'
    params={'source': {"id": null,"name": "Slate.com"}}
    if source is not None:
        params['source'] = source
    params['apiKey'] = newsapi_key
    return make_request_using_cache(baseurl, params)

def get_headlines(results_dict):
    results = results_dict['articles']
    headlines = []
    for r in results:
        headlines.append(r['title'])
    return headlines

science_list_json = fetch_top_headlines('science')
cnn_list_json=fetch_on_source({"id": "cnn","name": "CNN"})
headlines = get_headlines(science_list_json)
for h in headlines:
    print(h)

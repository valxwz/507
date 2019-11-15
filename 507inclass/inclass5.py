
#news.py
from secrets import *
import requests
import json

# gets headlines for today's news
def fetch_top_headlines(category=None):
    baseurl = 'https://newsapi.org/v2/top-headlines'
    params={'country': 'us'}
    if category is not None:
        params['category'] = category
    params['apiKey'] = newsapi_key
    return requests.get(baseurl, params).json()

def get_headlines(results_dict):
    results = results_dict['articles']
    headlines = []
    for r in results:
        headlines.append(r['title'])
    return headlines

science_list_json = fetch_top_headlines('science')
headlines = get_headlines(science_list_json)
for h in headlines:
    print(h)






# # on startup, try to load the cache from file
# CACHE_FNAME = 'datamuse_cache.json'
# try:
#     cache_file = open(CACHE_FNAME, 'r')
#     cache_contents = cache_file.read()
#     CACHE_DICTION = json.loads(cache_contents)
#     cache_file.close()

# # if there was no file, no worries. There will be soon!
# except:
#     CACHE_DICTION = {}

# # A helper function that accepts 2 parameters
# # and returns a string that uniquely represents the request
# # that could be made with this info (url + params)
# def params_unique_combination(baseurl, params):
#     alphabetized_keys = sorted(params.keys())
#     res = []
#     for k in alphabetized_keys:
#         res.append("{}-{}".format(k, params[k]))
#     return baseurl + "_" + "_".join(res)





# def make_request_using_cache(baseurl, params):
#     unique_ident = params_unique_combination(baseurl,params)

#     ## first, look in the cache to see if we already have this data
#     if unique_ident in CACHE_DICTION:
#         print("Getting cached data...")
#         return CACHE_DICTION[unique_ident]

#     ## if not, fetch the data afresh, add it to the cache,
#     ## then write the cache to file
#     else:
#         print("Making a request for new data...")
#         # Make the request and cache the new data
#         resp = requests.get(baseurl, params)
#         CACHE_DICTION[unique_ident] = json.loads(resp.text)
#         dumped_json_cache = json.dumps(CACHE_DICTION)
#         fw = open(CACHE_FNAME,"w")
#         fw.write(dumped_json_cache)
#         fw.close() # Close the open file
#         return CACHE_DICTION[unique_ident]

# # Gets data from the datamuse API, using the cache
# def get_rhymes_from_datamuse_caching(country):
#     baseurl = "https://newsapi.org/v2/top-headlines?"
#     params_diction = {}
#     params_diction["country"] = rhymes_with
#     return make_request_using_cache(baseurl, params_diction)

# # extract just the words from the data structures returned by datamuse
# def get_word_list(data_muse_word_list):
#     words = []
#     for word_dict in data_muse_word_list:
#         words.append(word_dict['word'])
#     return words

# # print up to 'max_rhymes' words that rhyme with 'word'
# def print_rhymes(word, max_rhymes=10):
#     rhymes = get_word_list(get_rhymes_from_datamuse_caching(word))
#     print('Words that rhyme with', word)
#     max2print = min(max_rhymes, len(rhymes))
#     for i in range(max2print):
#         print('\t', rhymes[i])
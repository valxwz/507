from requests_oauthlib import OAuth1
import json
import sys
import requests
import secret_data # file that contains OAuth credentials
# Uncomment following two lines after you install nltk
import nltk 
import operator


# import ssl

# try:
#     _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     pass
# else:
#     ssl._create_default_https_context = _create_unverified_https_context

# nltk.download()
# nltk.download('tokenize')

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 


## SI 507 - HW5
## COMMENT WITH:
## Your section day/time:
## Any names of people you worked with on this assignment:

#usage should be python3 hw5_twitter.py <username> <num_tweets>
username = sys.argv[1]
num_tweets = sys.argv[2]

consumer_key = secret_data.CONSUMER_KEY
consumer_secret = secret_data.CONSUMER_SECRET
access_token = secret_data.ACCESS_KEY
access_secret = secret_data.ACCESS_SECRET

#Code for OAuth starts
url = 'https://api.twitter.com/1.1/account/verify_credentials.json'

auth = OAuth1(consumer_key, consumer_secret, access_token, access_secret)
requests.get(url, auth=auth)
#Code for OAuth ends

#Write your code below:
#Code for Part 1:Get Tweets





CACHE_FNAME = 'tweeets_cache.json'
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
    return baseurl + "/" + "/".join(res)

# The main cache function: it will always return the result for this
# url+params combo. However, it will first look to see if we have already
# cached the result and, if so, return the result from cache.
# If we haven't cached the result, it will get a new one (and cache it)
def make_request_using_cache(baseurl, params):
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
        resp = requests.get(baseurl, params, auth=auth)
        CACHE_DICTION[unique_ident] = json.loads(resp.text)
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION[unique_ident]


def get_tweets_from_twitter(username,num_tweets):
    baseurl = "https://api.twitter.com/1.1/statuses/user_timeline.json"
    params_dict = {}
    params_dict["screen_name"] = username
    params_dict["count"] = num_tweets
    return make_request_using_cache(baseurl, params_dict)




def get_text_list(data_text_list):
    texts = []
    for text_dict in data_text_list:
        texts.append(text_dict['text'])
    return texts


test_list=get_text_list(get_tweets_from_twitter(username,num_tweets))
tokens_word_list=[]
for text in test_list:
    tokens=nltk.word_tokenize(str(text))
    for item in tokens:
        tokens_word_list.append(item)

# print (tokens_word_list)

def ignore_word(word_list):
    new_word_list=[]
    stop_words = set(stopwords.words('english'))
    new_word_list = [w for w in word_list if not w in stop_words] 
    for i in word_list:
        if not i[0].isalpha() or i in ['http', 'https', 'RT']:
            new_word_list.remove(i)

    return new_word_list


def frequency_distrubition(word_list):   
    wordfreq_dict={}
    most_frequent_five=[]
    for w in word_list:
        wordfreq_dict[w] = word_list.count(w) 
    sorted_words=sorted(wordfreq_dict.items(), key=lambda x: x[1], reverse=True)
    for i in sorted_words[0:5]:
        most_frequent_five.append(i[0])
    return most_frequent_five

print (frequency_distrubition(ignore_word(tokens_word_list)))


#Code for Part 2:Analyze Tweets

#Code for Part 3:Caching

if __name__ == "__main__":
    if not consumer_key or not consumer_secret:
        print("You need to fill in client_key and client_secret in the secret_data.py file.")
        exit()
    if not access_token or not access_secret:
        print("You need to fill in this API's specific OAuth URLs in this file.")
        exit()

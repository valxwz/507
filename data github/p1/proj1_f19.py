import json
import requests
import webbrowser

##part 1 and 2#####
class Media:

    def __init__(self,
                 title="No Title",
                 author="No Author",
                 release_year="No Release Year",
                 json_dict=None):
        self.json_dict = json_dict
        if json_dict is None:
            self.title = title
            self.author = author
            self.release_year = release_year
        else:
            self.process_json(json_dict)


    def process_json(self, json_dict):
        if json_dict["wrapperType"]=="track":
        	self.title=json_dict["trackName"]
        else:
            self.title = json_dict["collectionName"]
        self.author = json_dict["artistName"]
        self.release_year = json_dict["releaseDate"].split("-")[0]

    def __str__(self):
        return self.title + " by " + self.author + " (" + self.release_year + ")"

    def __len__(self):
        return int(0)


# Other classes, functions, etc. should go here


class Song(Media):

    def __init__(self,
                 title="No Title",
                 author="No Author",
                 release_year="No Release Year",
                 album="No Album",
                 genra="No Genra",
                 track_length=0,
                 json_dict=None):
        super().__init__(title, author, release_year,json_dict)
        if json_dict is None:
            self.album = album
            self.genra = genra
            self.track_length = track_length
        else:
            self.album = json_dict["collectionName"]
            self.genra = json_dict["primaryGenreName"]
            self.track_length = json_dict["trackTimeMillis"]

    def __str__(self):
        return super().__str__() + " [" + self.genra + "]"

    def __len__(self):
    	track_length = self.track_length / 1000
    	return int(track_length)



class Movie(Media):

    def __init__(self,
                 title="No Title",
                 author="No Author",
                 release_year="No Release Year",
                 rating="PG",
                 movie_length=0,
                 json_dict=None):
        super().__init__(title, author, release_year,json_dict)
        if json_dict is None:
            self.rating = rating
            self.movie_length = movie_length
        else:
            self.rating = json_dict["contentAdvisoryRating"]
            self.movie_length = json_dict["trackTimeMillis"]
    def __str__(self):
        return super().__str__() + " [" + self.rating + "]"

    def __len__(self):
    	movie_length = self.movie_length / 1000/60
    	return int(movie_length)
        





####part3####

def get_from_api(key_word,limit=10):
	base_url = "https://itunes.apple.com/search?term="
	key_word_list=key_word.split(" ")
	url = base_url + "+".join(key_word_list)
	if limit != None:
		url +="&limit="+str(limit)
	json_string = requests.get(url).text
	results_list = json.loads(json_string)['results']
	return results_list

###part4####

def run_on_query():
	user_input=input("Enter a search term, or “exit” to quit:")

	song_list=[]
	movie_list=[]
	others_list=[]
	if user_input.lower()=="exit":
		pass
		print ("Bye")
	else:
		results_from_request=get_from_api(user_input)
		for i in results_from_request:
			if "kind" in i.keys():
				if i['kind']=="song":
					song_list.append(str(Song(json_dict=i)))
				elif i['kind']=="feature-movie":
					movie_list.append(str(Movie(json_dict=i)))
				else:
					others_list.append(str(Media(json_dict=i)))
		song_len=len(song_list)
		movie_len=len(movie_list)
		others_len=len(others_list)

		all_media_list= song_list + movie_list + others_list

		if song_len>0:
			print ("SONGS")
			for i in range(song_len):
				print ("{} {}".format(i + 1, all_media_list[i]))
		if movie_len>0:
			print ("MOVIES")
			for j in range(song_len, song_len + movie_len):
				print ("{} {}".format(j + 1, all_media_list[j]))
		if others_len>0:
			print ("OTHERS")
			for k in range(song_len + movie_len, song_len + movie_len + others_len):
				print ("{} {}".format(k + 1, all_media_list[k]))
	while all_media_list!=[]:
		preview_input=input("Enter a number for more info, or another search term, or exit:")
		if preview_input.lower()=="exit":
			pass
			print ("Bye")
			break
		else:
			try:
				open_url=results_from_request[int(preview_input)-1]["trackViewUrl"]
				if open_url:
					print ("Launching ",open_url, " in web browser..." )
					webbrowser.open_new(open_url)
				else:
					preview_input=input("Sorry, there's no active link associated with your input. Enter a number for more info, or another search term, or exit:")
			except:
				print ("Invalid input. Try again.")
	if all_media_list==[]:
		print ("No result. Bye")

run_on_query()


if __name__ == "__main__":
    # your control code for Part 4 (interactive search) should go here
    pass

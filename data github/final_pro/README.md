Data source:
Yelp Fusion API
Billboard webpage top 100 songs - web scraping. 
Fusion API
Google Place API

Please install:
pip3 install pandas --no-build-isolation

The code is able to: 
Let's say the user is planning to open a new restaurant and looking for a site to choose.
The program is able to
1.  ask user to input:
	a. what type of restaurant he will open
	b. where he will open.
	c. any address he has in mind as the site to open the new restaurant. 

2. based user input, map out its competitors, parking lot nearby and site he chose 
3. user is also able to pick song from billboard top 50 songs list and save to the db, which can be used to later play in the new restaurant

Important functions: 
get_venue_info() -- will get restaurant information from Yelp, based on user's input. Lator user can pick restaurants and save as competitors. 

get_site_location() -- will get the cordinate of the site the user saved as future opening site.

get_music() -- will get music from the Billboard website.

create_table() -- will create 
choosen_site table -- save user's choosed site where he will open the restaurant in the future
competitor table -- save competitors users picked.
music table -- save song user picked
music_site table -- this table is a join table that link music table and choosen_site table.
It's a many-to-many relationship - multiple songs can be mathced to multiple sites. 

All insert functions -- will insert data as picked by user. 

show_map() -- will map out users competitors, parking lot, and site saved.   

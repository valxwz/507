import json 

# 507 Homework 7 Part 2
count = 0
#### Your Part 2 solution goes here ####

with open("directory_dict.json") as json_file:
	data=json.load(json_file)
values=data.values()
for i in values:
	if i["title"]=="PhD student":
		count+=1

#### Your answer output (change the value in the variable, count)####
print('The number of PhD students: ', count)
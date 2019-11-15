'''
SI 507 F19 homework 4: Classes and Inheritance

Your discussion section:
People you worked with:

######### DO NOT CHANGE PROVIDED CODE ############ 
'''

#######################################################################
#---------- Part 1: Class
#######################################################################

'''
Task A
'''
import random 
from random import randrange
class Explore_pet:
	boredom_decrement = -4
	hunger_decrement = -4
	boredom_threshold = 6
	hunger_threshold = 10
	def __init__(self, name="Coco"):
		self.name = name
		self.hunger = randrange(self.hunger_threshold)
		self.boredom = randrange(self.boredom_threshold)

	def mood(self):
		if self.hunger <= self.hunger_threshold and self.boredom <= self.boredom_threshold:
			return "happy"
		elif self.hunger > self.hunger_threshold:
			return "hungry"
		else:
			return "bored"

	def __str__(self):
		state = "I'm " + self.name + '. '
		state += 'I feel ' + self.mood() + '. '
		if self.mood() == 'hungry':
			state += 'Feed me.'
		if self.mood() == 'bored':
			state += 'You can teach me new words.'
		return state
coco = Explore_pet()


# #your code begins here . . . 
coco.hunger=8
coco.boredom=9
print (coco)

brian=Explore_pet("Brian")
brian.hunger=12
print (brian)


'''
Task B
'''
#add your codes inside of the Pet class
class Pet:
	boredom_decrement = -4
	hunger_decrement = -4
	boredom_threshold = 6
	hunger_threshold = 10

	def __init__(self, name="Coco"):
		self.name = name
		self.hunger = randrange(self.hunger_threshold)
		self.boredom = randrange(self.boredom_threshold)
		self.words_list=["Hello"]

	def mood(self):
		if self.hunger <= self.hunger_threshold and self.boredom <= self.boredom_threshold:
			return "happy"
		elif self.hunger > self.hunger_threshold:
			return "hungry"
		else:
			return "bored"
	def clock_tick(self):
		self.hunger+=2
		self.boredom+=2
	def say(self):
		for word in self.words_list:
			print ("I know how to say", word)

	def teach(self,word):
		self.words_list.append(word)
		if self.boredom>0:
			self.boredom+=self.boredom_decrement
		else: 
			self.boredom=0

	def feed(self):
		if self.hunger>0:
			self.hunger+=hunger_decrement
		else: 
			self.hunger=0
	def hi(self):
		print ("I know how to say", random.choice(self.words_list))

	def __str__(self):
		state = "I'm " + self.name + '. '
		state += 'I feel ' + self.mood() + '. '
		if self.mood() == 'hungry':
			state += 'Feed me.'
		if self.mood() == 'bored':
			state += 'You can teach me new words.'
		return state

'''
Task C
'''



def teaching_session(my_pet,new_words):
	for word in new_words:
		my_pet.teach(word)
	#print (my_pet.words_list)
		my_pet.hi()
		if my_pet.mood()=="hungry":
			my_pet.feed()
		my_pet.clock_tick()
	print (my_pet)



new_pet=Pet("Abby")


teaching_session(new_pet, ['I am sleepy', 'You are the best','I love you, too'])  




# #######################################################################
# #---------- Part 2: Inheritance - subclasses
# #######################################################################
# '''
# Task A: Dog and Cat    
# '''
# #your code begins here . . . 

class Dog(Pet):
	def __str__(self):
		state = "I'm " + self.name + ', arrrf! '
		state += 'I feel ' + self.mood() + ', arrrf! '
		if self.mood() == 'hungry':
			state += 'Feed me.'
		if self.mood() == 'bored':
			state += 'You can teach me new words.'
		return state

class Cat(Pet):
	def __init__(self,meow_count,name="Coco"):
		super().__init__(name)
		self.meow_count=meow_count
	def hi(self):
		meow_hi_words=""
		for num in range(int(self.meow_count)):
			meow_hi_words+=str(random.choice(self.words_list))
		print ("I know how to say",meow_hi_words)

# '''
# Task B: Poodle 
# '''
# #your code begins here . . . 

class Poodle(Dog):
	def dance(self):
		dance_saying="Dancing in circle like a poodles do!"
		return dance_saying
	def say(self):
	 	print (self.dance())
	 	super().say()

new_poodle=Poodle("Poo")
print (new_poodle)

#for test
new_poodle.say()

Cat(5,"Kitty").hi()





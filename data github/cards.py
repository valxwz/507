import random
import unittest

# SI 507 Fall 2018
# Homework 2 - Code

##COMMENT YOUR CODE WITH:
# Section Day/Time:
# People you worked with:

######### DO NOT CHANGE PROVIDED CODE #########
### Scroll down for assignment instructions.
#########

class Card(object):
	suit_names =  ["Diamonds","Clubs","Hearts","Spades"]
	rank_levels = [1,2,3,4,5,6,7,8,9,10,11,12,13]
	faces = {1:"Ace",11:"Jack",12:"Queen",13:"King"}

	def __init__(self, suit=0,rank=2):
		self.suit = self.suit_names[suit]
		if rank in self.faces: # self.rank handles printed representation
			self.rank = self.faces[rank]
		else:
			self.rank = rank
		self.rank_num = rank # To handle winning comparison

	def __str__(self):
		return "{} of {}".format(self.rank,self.suit)

class Deck(object):
	def __init__(self): # Don't need any input to create a deck of cards
		# This working depends on Card class existing above
		self.cards = []
		for suit in range(4):
			for rank in range(1,14):
				card = Card(suit,rank)
				self.cards.append(card) # appends in a sorted order

	def __str__(self):
		total = []
		for card in self.cards:
			total.append(card.__str__())
		# shows up in whatever order the cards are in
		return "\n".join(total) # returns a multi-line string listing each card

	def pop_card(self, i=-1):
		# removes and returns a card from the Deck
		# default is the last card in the Deck
		return self.cards.pop(i) # this card is no longer in the deck -- taken off

	def shuffle(self):
		random.shuffle(self.cards)

	def replace_card(self, card):
		card_strs = [] # forming an empty list
		for c in self.cards: # each card in self.cards (the initial list)
			card_strs.append(c.__str__()) # appends the string that represents that card to the empty list
		if card.__str__() not in card_strs: # if the string representing this card is not in the list already
			self.cards.append(card) # append it to the list

	def sort_cards(self):
		# Basically, remake the deck in a sorted way
		# This is assuming you cannot have more than the normal 52 cars in a deck
		self.cards = []
		for suit in range(4):
			for rank in range(1,14):
				card = Card(suit,rank)
				self.cards.append(card)


def play_war_game(testing=True):
	# Call this with testing = True and it won't print out all the game stuff -- makes it hard to see test results
	player1 = Deck()
	player2 = Deck()

	p1_score = 0
	p2_score = 0

	player1.shuffle()
	player2.shuffle()
	if not testing:
		print("\n*** BEGIN THE GAME ***\n")
	for i in range(52):
		p1_card = player1.pop_card()
		p2_card = player2.pop_card()
		print('p1 rank_num=', p1_card.rank_num, 'p1 rank_num=', p2_card.rank_num)
		if not testing:
			print("Player 1 plays", p1_card,"& Player 2 plays", p2_card)

		if p1_card.rank_num > p2_card.rank_num:

			if not testing:
				print("Player 1 wins a point!")
			p1_score += 1
		elif p1_card.rank_num < p2_card.rank_num:
			if not testing:
				print("Player 2 wins a point!")
			p2_score += 1
		else:
			if not testing:
				print("Tie. Next turn.")

	if p1_score > p2_score:
		return "Player1", p1_score, p2_score
	elif p2_score > p1_score:
		return "Player2", p1_score, p2_score
	else:
		return "Tie", p1_score, p2_score

if __name__ == "__main__":
	result = play_war_game()
	print("""\n\n******\nTOTAL SCORES:\nPlayer 1: {}\nPlayer 2: {}\n\n""".format(result[1],result[2]))
	if result[0] != "Tie":
		print(result[0], "wins")
	else:
		print("TIE!")


######### DO NOT CHANGE CODE ABOVE THIS LINE #########

## You can write any additional debugging/trying stuff out code here...
## OK to add debugging print statements, but do NOT change functionality of existing code.
## Also OK to add comments!

#########
		




##**##**##**##@##**##**##**## # DO NOT CHANGE OR DELETE THIS COMMENT LINE -- we use it for grading your file
###############################################

### Write unit tests below this line for the cards code above.

class TestCard(unittest.TestCase):


	# this is a "test"
	def test_create(self):
		#test 1 Test that if you create a card with rank 12, its rank will be "Queen"
		queen_card=Card(rank=12)
		self.assertEqual(queen_card.rank, "Queen")
		#test 2
		clubs_card=Card(suit=1)
		self.assertEqual(clubs_card.suit,"Clubs")
		#test 3
		king_spade_card=Card(suit=3, rank=13)
		self.assertEqual(str(king_spade_card),"King of Spades")
		#test 4
		deck1=Deck()
		self.assertEqual(len(deck1.cards),52)
		#test 5
		pop_test_card=Deck().pop_card()
		popcard_item_list=str(pop_test_card).split()
		#now we have a list of word like ["King", "of", "Spade"]
		#check if the 1st word is in rank_levels/faces, and check if the 3rd word is in suit_names
		#check if the rank has face value
		if popcard_item_list[0] in Card.faces.values():
			#if the rank has a face value, turns it to num
			#to do so, create a dictionary whose key is the face, value is the number
			face_num={"Ace":1,"Jack":11,"Queen":12,"King":13}
			rank_num=face_num[popcard_item_list[0]]

			#print (popcard_item_list[0], "rank is in faces")
		else:
			rank_num=popcard_item_list[0]
		self.assertIn(rank_num,Card.rank_levels)
		self.assertIn(popcard_item_list[2],Card.suit_names)

		#test 6 if pop_card will reduce cards' num
		deck2=Deck()
		#print ("length of origianl cards", len(deck.cards))
		#run popcard
		deck2.pop_card()
		#print ("length afterward", len(deck2.cards))
		self.assertTrue(len(deck2.cards)<52)
		#print ("deck2 num of cards", len(deck2.cards))

		#test 7 test if replace_card will increase the num of cards
		deck3=Deck()
		#first pop a card
		deck3_pop_card=deck3.pop_card()
		#create an instance - length before replacing
		len_before_replacing=len(deck3.cards)
		#print("length before replacing ", len_before_replacing)
		#put the pop card back
		deck3.replace_card(deck3_pop_card)
		#create an instance - length after replacing
		len_after_replacing=len(deck3.cards)
		#print("length after replacing ", len_after_replacing)
		self.assertTrue(len_before_replacing<len_after_replacing)
		#test 8 test if we can replace a card that's in the deck
		deck4=Deck()
		#choose a card existed in the deck
		existed_card=deck4.cards[1]
		self.assertIsNone(deck4.replace_card(existed_card))
		#test 9

		game_result=play_war_game()
		#test if the game_result is a tuple
		self.assertTrue(isinstance(game_result, tuple))
		#test if there's 3 elements in the tuple 
		self.assertEqual(len(game_result),3)
		#test if the 1st element is a string
		self.assertTrue(game_result[0],str)

		#test 10
		#to test if the shuffle works
		#create a deck
		deck5=Deck()
		cards_before_shuffle=deck5.cards
		#create an empty list to save the first card of the deck 5 into the list
		card_list=[]
		card_list.append(cards_before_shuffle[0])
		deck5.shuffle()
		cards_after_shuffle=deck5.cards
		#save the the first card of the shuffled deck 5 into the list
		card_list.append(cards_after_shuffle[0])
		#compare the 2 1st card before & after shuffle
		self.assertNotEqual(card_list[1],card_list[0])









#############
## The following is a line to run all of the tests you include:
if __name__ == "__main__":
	unittest.main(verbosity=2)
## verbosity 2 to see detail about the tests the code fails/passes/etc.

# Milestone Project 2 -- BlackJack
import random

#Globals for the game
playing = False
chip_pool = 100
bet = 1
max_players = 8
restart_phrase = "Press 'd' to deal some cards again, or press 'q' to quit"

#Globals for the cards
suits = ('H', 'S', 'C', 'D')
ranks = ('A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K')
card_val = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'J':10, 'Q':10, 'K':10}

class Card:
	
	def __init__(self,suit,rank):
		self.suit = suit
		self.rank = rank
	
	def __str__(self):
		return "Card is the %s of %s." %(self.rank, self.suit)
	
	def grab_rank(self, rank):
		return self.rank
		
	def grab_suit(self, suit):
		return self.suit
		
	def draw(self):
		print(self.rank + self.suit)

class Hand:

	def __init__(self):
		self.cards = []
		self.value = 0
		self.ace = False
		
	def __str__(self):
		hand_comp = ""
		
		for card in self.cards:
			card_name = card.__str__()
			hand_comp += " "+ card_name
		
		return "The hand has %s" %hand_comp
			
	def card_add(self, card):
		self.cards.append(card)
		
		if card.rank == 'A':
			self.ace = True
			
		self.value += card_val[card.rank]
	
	def calc_val(self):
		if(self.ace == True and self.value < 12):
			return self.value + 10
		else:
			return self.value
		
	def draw(self,hidden):
		if hidden == True and playing == True:
			starting_card = 1
		else:
			starting_card = 0
		for x in range(starting_card, len(self.cards)):
			self.cards[x].draw()
	
class Deck:

	def __init__(self):
		self.deck = []
		for suit in suits:
			for rank in ranks:
				self.deck.append(Card(suit,rank))
	
	def shuffle(self):
		random.shuffle(self.deck)
		
	def deal(self):
		single_card = self.deck.pop()
		return single_card
		
	def __str__(self):
		deck_comp = ""
		for card in self.cards:
			deck_comp += " " + deck_comp.__str__()
		return "The deck has"+ deck_comp

'''class Player(object):
	
	def __init__(self, bankroll = 100):
		self.bankroll = bankroll
		
	def add_bankroll(self, amount):
		self.bankroll += amount
		
	def sub_bankroll(self, amount):
		self.bankroll -= amount'''
		
def make_bet():
	global bet
	bet = 0
	print("Chip Total: "+ str(chip_pool))
	if chip_pool == 0:
		print("Whoa, hold on there. You ran out of chips. You can't play anymore. Sorry about that.")
		game_exit()
	
	print("How many chips would you like to bet? Only whole integers. (We can't deal in half chips.) ")
	
	while bet == 0:
		bet_comp = input()
		bet_comp = int(bet_comp)
		if bet_comp >= 1 and bet_comp <= chip_pool:
			bet = bet_comp
		else:
			print("Invalid bet, you only have "+ str(chip_pool) +" remaining.")

def deal_cards():
	
	global result,playing,deck,player_hand,dealer_hand,chip_pool,bet
	
	deck = Deck()
	deck.shuffle()
	make_bet()
	
	player_hand = Hand()
	dealer_hand = Hand()
	
	player_hand.card_add(deck.deal())
	player_hand.card_add(deck.deal())
	dealer_hand.card_add(deck.deal())
	dealer_hand.card_add(deck.deal())
	
	result = "\nHit or Stand? Press h or s: "
	
	if playing == True:
		print("Fold, Sorry")
		chip_pool -= bet
	
	playing = True
	game_step()

def hit():
	global playing, chip_pool, deck, player_hand, dealer_hand, result, bet
	
	if playing:
		if player_hand.calc_val() <= 21:
			player_hand.card_add(deck.deal())
			
		print("Player hand is %s" %player_hand)
		
		if player_hand.calc_val() > 21:
			result = "Busted! "+ restart_phrase
			chip_pool -= bet
			playing = False
		
	else:
		result = "Sorry, can't hit." + restart_phrase
	
	game_step()
	
def stand():
	global playing, chip_pool, deck, player_hand, dealer_hand, result, bet
	
	if playing == False:
		if player_hand.calc_val() > 0:
			result = "Sorry, you can't stand!"
		
	else:
		while dealer_hand.calc_val() < 17:
			dealer_hand.card_add(deck.deal())
		if dealer_hand.calc_val() > 21:
			result = "Dealer busts! You win! " + restart_phrase
			chip_pool += bet
			playing = False
		elif dealer_hand.calc_val() < player_hand.calc_val():
			result = "You beat the dealer! Nice job! "+ restart_phrase
			chip_pool += bet
			playing = False
		else:
			result = "Dealer wins! "+ restart_phrase
			chip_pool -= bet
			playing = False
	game_step()

def game_step():
	print("\nPlayer Hand is: "),player_hand.draw(hidden = False)
	print("Player hand total is: "+ str(player_hand.calc_val()))
	
	print("Dealer Hand is: "),dealer_hand.draw(hidden = True)
	
	if playing == False:
		print(" --- for a total of "+ str(dealer_hand.calc_val()))
		print("Chip Total: "+ str(chip_pool))
	else:
		print("with another card hidden face down.")
	
	print(result)
	
	player_input()

def player_input():
	plin = input().lower()
	
	if plin == 'h':
		hit()
	elif plin == 's':
		stand()
	elif plin == 'd':
		deal_cards()
	elif plin == 'q':
		game_exit()
	else:
		print("Invalid input. Enter either h, s, d, or q: ")
		player_input()

def game_exit():
	print("Thank you for playing! More functionality coming soon!")
	exit()
	
def intro():
	statement = '''\nWelcome to BlackJack! The goal of the game is to get as close to 21 as you can without going over!
Dealer hits until a total of at least 17 is reached. Aces count as 1 or 11.
Card output goes a number of face notation followed by the suit, such as 4H (4 of Hearts)'''
	print(statement)

#Actual game start
deck = Deck()
deck.shuffle()
player_hand = Hand()
dealer_hand = Hand()

intro()
deal_cards()
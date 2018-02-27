import numpy as np
from collections import Counter
import scipy.stats as sps

class Hand:
	def __init__(self, deck_name = "none"):
		if deck_name != "none":
			self.deck, self.decklist = self.process(deck_name)
		else:
			self.deck = ["Storm Crow"] * 60
			self.decklist = dict(Counter(deck))

		self.new_hand(7)

	def process(self, filename):
		with open(filename,"r") as file:
			file_read = [line.strip().split(" ", 1) for line in file if len(line.split()) > 0]
		deck = []
		for [number, card] in file_read:
			deck += [card] * int(number)
		decklist = dict(Counter(deck))
		return deck, decklist

	def set_deck(self, new_deck):
		if isinstance(new_deck, list):
			self.deck = new_deck
			self.decklist = dict(Counter(new_deck))
		elif isinstance(new_deck, dict):
			deck = []
			for card, number in new_deck.items():
				deck += [card] * int(number)
			self.deck = deck
			self.decklist = dict(Counter(new_deck))
		elif isinstance(new_deck, str):
			self.deck, self.decklist = self.process(new_deck)
		else:
			print("ERROR: invalid deck format")
			return False
		return True

	def get_deck(self):
		return self.deck.copy()

	def get_decklist(self):
		return dict(self.decklist.copy())

	def new_hand(self, size = 7):
		draws = np.random.choice(len(self.deck),size,replace = False)
		self.card_counts = Counter([self.deck[i] for i in draws])
		self.cards = set(self.card_counts.keys())
		return self.card_counts.copy()

	def has_tron(self):
		check = [0] * 4
		if "Urza's Tower" in self.cards:
			check[0] = 1
		if "Urza's Mine" in self.cards:
			check[1] = 1
		if "Urza's Power Plant" in self.cards:
			check[2] = 1
		if "Expedition Map" in self.cards:
			check[3] = 1
		return float(sum(check) >= 3)

	def contains(self,cards):
		if isinstance(cards, str):
			return 1.0*(cards in self.cards)
		return float(len(self.cards & set(cards)) > 0)

	def count_of(self,cards):
		if isinstance(cards, str):
			return float(self.card_counts[cards])
		return float(sum([self.card_counts[card] for card in cards]))

	def expect(self,cards,size = 7):
		if isinstance(cards, str):
			n = self.decklist[cards]
		elif isinstance(cards, list):
			n = sum([self.decklist[card] for card in cards])
		else: 
			return 0
		if n == 0: return 0
		return sps.hypergeom.mean(len(self.deck),n,size)


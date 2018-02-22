import numpy as np
from collections import Counter

def newHand(deck = ["Storm Crow"] * 60, size = 7):
	assert(size <= len(deck))
	draws = np.random.choice(len(deck),size,replace = False)
	hand = Counter(deck[draws])
	return hand

def process(filename):
	file = open(filename,"r")
	decklist = [str.strip(line).split(" ", 1) for line in file if len(line.split()) > 0]
	deck = []
	for [number, card] in decklist:
		deck += [card] * int(number)
	return deck

def hasTron(hand):
	check = [0] * 4
	cards = hand.keys()
	if "Urza's Tower" in cards:
		check[0] = 1
	if "Urza's Mine" in cards:
		check[1] = 1
	if "Urza's Power Plant" in cards:
		check[2] = 1
	if "Expedition Map" in cards:
		check[3] = 1
	return float(sum(check) >= 3)

def contains(hand,cards):
	if type(cards) is str:
		return 1.0*(cards in hand.keys())
	return float(len(set(hand.keys()) & set(cards)) > 0)

def countOf(hand,cards):
	if type(cards) is str:
		return float(hand[cards])
	return float(sum([hand[card] for card in cards]))

iterations = 500000
mullto = 3
deck = process("eTron.txt")
success = 0.0
early_success = 0.0
good_counts = np.zeros(8 - mullto)
hand_counts = np.zeros((8 - mullto,5))
totals = np.zeros(8 - mullto)

landNames = ["Cavern of Souls", "Sea Gate Wreckage", "Wastes", "Eldrazi Temple", "Urza's Mine", "Urza's Power Plant", "Urza's Tower", "Ghost Quarter"]

for i in range(iterations):
	flag = False
	early_flag = False
	for j in range(0,8 - mullto):
		hand = newHand(deck, 7 - j)

		tron = hasTron(hand)
		lands = countOf(hand,landNames)
		has_TKS = contains(hand,"Thought-Knot Seer")
		has_Reshaper = contains(hand,"Matter Reshaper")
		has_Chalice = contains(hand,"Chalice of the Void")
		temples = countOf(hand,"Eldrazi Temple") 
		has_Map = float(hand["Expedition Map"] > 0 and lands >= 2)

		# tron, Chalice + lands, t3 TKS, t2 Reshaper, 2 temples and any spell
		types = np.array([tron, has_Chalice * (lands >= 2), has_TKS * (has_Map or (temples > 0)) * (lands >= 2), has_Reshaper * (temples > 0) * (lands >= 2), (temples + has_Map >= 2) * (lands < (7 - j))])
		good_counts[7 - j - mullto] += (np.sum(types) > 0)
		hand_counts[:,7 - j - mullto] += types
		totals[7 - j - mullto] += 1
		if not flag:
			if (np.sum(types) > 0):
				flag = True
				if(j <= 2):
					early_flag = True
	success += flag
	early_success += early_flag

p_good = good_counts / totals
p_hands = hand_counts / totals.reshape(8 - mullto,1)
p_early_success = early_success / iterations
p_success = success / iterations

with open('output.csv','wb') as file:
	file.write(str(iterations) + " iterations,cards\n")

	# hand size headers
	for i in range(mullto,8):
		file.write(str(i) + ",")
	file.write("\n")

	#results
	for p in p_good:
		file.write(str(p) + ",")
	file.write("\n")
	for type in p_hands:
		for p in type:
			file.write(str(p) + ",")
		file.write("\n")

	file.write("p of good hand by 5\n")
	file.write(str(p_early_success) + "\n")
	file.write("p of good hand by 3\n")
	file.write(str(p_success) + "\n")
	file.close()

print(p_good)
print(p_hands)
print(p_early_success)
print(p_success)

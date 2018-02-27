import numpy as np
from hand import Hand

iterations = 250000
starting_size = 8 #inclusive
mullto = 7	#inclusive
hand = Hand("decklists/affinity.txt")
hand_types = ["t1 2-drop", "t1 3-drop"]
hand_counts = np.zeros(((starting_size + 1) - mullto,len(hand_types)))
totals = np.zeros(((starting_size + 1) - mullto,1))

zero_creatures = ["Memnite", "Ornithopter"]
zero_others = "Welding Jar"
ones = ["Signal Pest", "Vault Skirge"]
twos = ["Arcbound Ravager", "Cranial Plating", "Steel Overseer"]
threes = ["Etched Champion", "Master of Etherium"]
lands = ["Darksteel Citadel", "Spire of Industry", "Glimmervoid", "Inkmoth Nexus", "Blinkmoth Nexus", "Island"]

for i in range(iterations):
	for j in range(0,(starting_size + 1) - mullto):
		hand.new_hand(starting_size - j)

		count_opal = hand.count_of("Mox Opal")
		count_lands = hand.count_of(lands)
		has_drum = hand.contains("Springleaf Drum")
		count_zero_creatures = hand.count_of(zero_creatures)
		count_zeros = count_zero_creatures + hand.count_of(zero_others) + hand.contains("Darksteel Citadel")
		count_ones = hand.count_of(ones) + has_drum * 1
		has_two = hand.contains(twos)
		has_three = hand.contains(threes)

		t1_opal = (count_zeros >= 2) or (has_drum and (count_zero_creatures > 0) and (count_lands > 0))
		t1_pay_opal = (count_ones > 0) and (count_zeros > 0) and (count_lands > 0)
		t1_mana = count_opal * t1_opal + (count_lands > 0) + ((not t1_opal) * t1_pay_opal * max((count_opal - 1),0))
		# t2_accel = t1_accel or (has_drum and (count_zero_creatures > 0)) or ((count_ones > 0) and (count_zeros > 0) and (count_opal > 0)) \

		results = [(t1_mana >= 2) and has_two, (t1_mana >= 3) and has_three]

		hand_counts[starting_size - j - mullto,:] += results
		totals[starting_size - j - mullto,:] += 1

# print(np.flip(hand_counts, axis = 0))
# print(np.flip(totals, axis = 0))
p_hands = hand_counts / totals

with open("output/affinity_output.csv","wb") as file:
	file.write(str(iterations) + " iterations\n\n")

	# hand size headers
	file.write("hand sizes/types,")
	for type in hand_types:
		file.write(str(type) + ",")

	#results
	file.write("\n")
	for size in reversed(range(len(p_hands))):
		file.write(str(size + mullto) + ",")
		for p in p_hands[size,:]:
			 file.write(str(p) + ",")
		file.write("\n")
	file.close()

print(np.flip(p_hands, axis = 0))
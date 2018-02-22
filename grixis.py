import numpy as np
from hand import Hand

iterations = 1000
starting_size = 10 #inclusive
mullto = 4	#not inclusive
hand = Hand("decklists/grixis.txt")
hand_types = ["Tapped Summit", "Tapped Catacombs", "All Tapped"]
hand_counts = np.zeros(((starting_size + 1) - mullto,len(hand_types)))
totals = np.zeros(((starting_size + 1) - mullto,len(hand_types)))

islands = ["Fetid Pools", "Island"]
swamps = ["Fetid Pools", "Canyon Slough", "Swamp"]
mountains = ["Canyon Slough", "Mountain"]

for i in range(iterations):
	for j in range(0,(starting_size + 1) - mullto):
		hand.new_hand(starting_size - j)

		has_island = hand.contains(islands)
		has_swamp = hand.contains(swamps)
		has_mountain = hand.contains(mountains)

		has_summit = hand.contains("Dragonskull Summit")
		has_combs = hand.contains("Drowned Catacomb")

		tapped_summit = has_summit and not (has_mountain or has_swamp)
		tapped_combs = has_combs and not (has_swamp or has_island)

		all_tapped = (tapped_summit and tapped_combs) or (tapped_summit and (not has_combs)) or ((not has_summit) and tapped_combs)

		results = [tapped_summit*1, tapped_combs*1, all_tapped*1]
		count = [has_summit*1, has_combs*1, (has_summit or has_combs)*1]

		hand_counts[starting_size - j - mullto,:] += results
		totals[starting_size - j - mullto,:] += count

# print(np.flip(hand_counts, axis = 0))
# print(np.flip(totals, axis = 0))
p_hands = hand_counts / totals

with open("output/grixis_output.csv","wb") as file:
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
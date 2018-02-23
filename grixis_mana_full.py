import numpy as np
from hand import Hand

# hyperparameters
iterations_per = 500
epsilon = 10**-8 # offset to prevent division from blowing up
# R, B, U
lambd_colors = (1., 17./21, 13./21)
# Summit, Catacombs
lambd_checks = (0.4, 0.4)
# value of drawing Field of Ruin
lambd_field = 0.035
# penalty for drawing tapped lands (ie. cycling lands)
lamdb_tapped = 0.5
# hand sizes
starting_size = 8 #inclusive
mullto = 6	#inclusive

# initialization
hand = Hand("decklists/grixis.txt")
hand_types = ["has R", "has B", "has U", "tapped Summit", "tapped Catacombs", "has Field", "count tapped"]

# classes of cards
R = ["Canyon Slough", "Mountain", "Dragonskull Summit", "Aether Hub", "Spirebluff Canal"]
B = ["Fetid Pools", "Canyon Slough", "Swamp", "Aether Hub", "Dragonskull Summit", "Drowned Catacomb"]
U = ["Fetid Pools", "Island", "Spirebluff Canal", "Aether Hub", "Drowned Catacomb"]
islands = ["Fetid Pools", "Island"]
swamps = ["Fetid Pools", "Canyon Slough", "Swamp"]
mountains = ["Canyon Slough", "Mountain"]
tapped = ["Fetid Pools", "Canyon Slough"]

# list of land counts we control
lands = ["Mountain", "Swamp", "Island", "Dragonskull Summit", "Drowned Catacomb", "Field of Ruin", 
		 "Canyon Slough", "Fetid Pools", "Spirebluff Canal", "Aether Hub"]
total = 0
for land in lands: 
	total += hand.decklist[land]

results = {}
for mtn_ct in range(0,6):
	for swamp_ct in range(0,5):
		for island_ct in range(0,3):
			for field_ct in range(0,3):
				for slough_ct in range(0,5):
					for pool_ct in range(0,5):
						for bluff_ct in range(0,5):
							for hub_ct in range(0,5):	
								for summit_ct in range(0,5):
									combs_ct = total - (mtn_ct + swamp_ct + island_ct + field_ct + slough_ct \
														+ pool_ct + bluff_ct + hub_ct + summit_ct)
									if combs_ct > 4 or combs_ct < 0: continue
									config = {"Mountain":mtn_ct, "Swamp":swamp_ct, "Island":island_ct, "Dragonskull Summit":summit_ct, 
									          "Drowned Catacomb":combs_ct, "Field of Ruin":field_ct, "Canyon Slough":slough_ct,
									          "Fetid Pools":pool_ct, "Spirebluff Canal": bluff_ct, "Aether Hub": hub_ct}
									new_decklist = hand.decklist
									new_decklist.update(config)
									hand.set_deck(new_decklist)

									hand_counts = np.zeros(len(hand_types))
									totals = np.zeros(len(hand_types)) + epsilon

									for hand_size in range(mullto,(starting_size + 1)):
										hand_counts[0] += hand.expect(R, hand_size) 
										hand_counts[1] += hand.expect(B, hand_size) 
										hand_counts[2] += hand.expect(U, hand_size)
										hand_counts[5] += hand.expect("Field of Ruin", hand_size)
										hand_counts[6] += hand.expect(tapped, hand_size)  
									hand_counts = hand_counts / (starting_size - mullto + 1)

									for i in range(iterations_per):
										for hand_size in range(mullto,(starting_size + 1)):
											hand.new_hand(hand_size)

											has_island = hand.contains(islands)
											has_swamp = hand.contains(swamps)
											has_mountain = hand.contains(mountains)
											has_summit = hand.contains("Dragonskull Summit")
											has_combs = hand.contains("Drowned Catacomb")

											tapped_summit = min(has_summit,max(has_mountain, has_swamp))
											tapped_combs = min(has_combs,max(has_swamp, has_island))

											bools = [0, 0, 0, tapped_summit, tapped_combs, 0, 0]
											counts = [0, 0, 0, has_summit, has_combs, 0, 0]

											hand_counts += bools
											totals += counts

									hand_counts[3:4] = hand_counts[3:4] / totals[3:4]
									utility = lambd_colors[0]*hand_counts[0] + lambd_colors[1]*hand_counts[1] + lambd_colors[2]*hand_counts[2] \
											- lambd_checks[0]*hand_counts[3] - lambd_checks[1]*hand_counts[4] + lambd_field*hand_counts[5] \
											- lamdb_tapped*hand_counts[6]

									key = (mtn_ct, swamp_ct, island_ct, summit_ct, combs_ct, field_ct, slough_ct, pool_ct, bluff_ct, hub_ct)
									results[utility] = key

print("Order of lands:")
for land in lands:
	print(str(land) + ", ", end="")

sorted_results = sorted(results.keys(), key=lambda v:-v)
top_ten = sorted_results[:10]
print("\n\nTop ten configurations:")
for utility in top_ten:
	print(str(results[utility]) + "\t" + str(utility))

print("\nAverage of top twenty:")
top_twenty = sorted_results[:20]
avg = np.zeros(len(lands), dtype=float)
for utility in top_twenty:
	avg += np.array(results[utility], dtype=float)
avg = avg / 20
print(avg)





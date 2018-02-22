import numpy as np
from hand import Hand
import pdb

# hyperparameters
iterations_per = 3000
epsilon = 10**-8 # offset to prevent division from blowing up
# R, B, U
lambd_colors = (1, 2.5/4, 0.25)
# Summit, Catacombs
lambd_checks = (0.15, 0.15)
# value of drawing Field of Ruin
lambd_field = 0.25/3
# penalty for drawing Fetid Pools
lamdb_pool = 0.5
# hand sizes
starting_size = 9 #inclusive
mullto = 5	#not inclusive

# initialization
hand = Hand("decklists/grixis.txt")
hand_types = ["has R", "has B", "has U", "tapped Summit", "tapped Catacombs", "has Field", "has Pool"]

# classes of cards
R = ["Canyon Slough", "Mountain", "Dragonskull Summit", "Aether Hub", "Spirebluff Canal"]
B = ["Fetid Pools", "Canyon Slough", "Swamp", "Aether Hub", "Dragonskull Summit", "Drowned Catacomb"]
U = ["Fetid Pools", "Island", "Spirebluff Canal", "Aether Hub", "Drowned Catacomb"]
islands = ["Fetid Pools", "Island"]
swamps = ["Fetid Pools", "Canyon Slough", "Swamp"]
mountains = ["Canyon Slough", "Mountain"]

# list of land counts we change
flex_lands = ["Mountain", "Swamp", "Island", "Dragonskull Summit", "Drowned Catacomb", "Field of Ruin", "Fetid Pools"]
total = 0
for land in flex_lands: 
	total += hand.decklist[land]

results = {}
for mtn_ct in range(1,5):
	for swamp_ct in range(0,5):
		for island_ct in range(0,2):
			for field_ct in range(0,3):
				for pool_ct in range(2,5):
					checks = total - (mtn_ct + swamp_ct + island_ct + field_ct + pool_ct)
					if checks > 8 or checks < 0: continue
					for summit_ct in range(0,min(checks, 5)):
						combs_ct = checks - summit_ct
						if combs_ct > 4: continue
						config = {"Mountain":mtn_ct, "Swamp":swamp_ct, "Island":island_ct, "Dragonskull Summit":summit_ct, 
						          "Drowned Catacomb":combs_ct, "Field of Ruin":field_ct, "Fetid Pools":pool_ct}
						new_decklist = hand.get_decklist()
						new_decklist.update(config)
						hand.set_deck(new_decklist)

						hand_counts = np.zeros(len(hand_types))
						totals = np.zeros(len(hand_types))

						for i in range(iterations_per):
							for j in range(0,(starting_size + 1) - mullto):
								hand.new_hand(starting_size - j)

								has_island = hand.contains(islands)
								has_swamp = hand.contains(swamps)
								has_mountain = hand.contains(mountains)
								tapped_summit = hand.contains("Dragonskull Summit") and not (has_mountain or has_swamp)
								tapped_combs = hand.contains("Drowned Catacomb") and not (has_swamp or has_island)

								bools = [hand.contains(R), hand.contains(B), hand.contains(U), 
										 tapped_summit, tapped_combs, hand.contains("Field of Ruin"), 
										 hand.contains("Fetid Pool")]
								counts = [1, 1, 1, 1, 1, 1, 1]

								hand_counts += bools
								totals += counts

						probs = hand_counts / totals
						utility = lambd_colors[0]*probs[0] + lambd_colors[1]*probs[1] + lambd_colors[2]*probs[2] \
								- lambd_checks[0]*probs[3] - lambd_checks[1]*probs[4] + lambd_field*probs[5] \
								- lamdb_pool*probs[6]

						key = (mtn_ct, swamp_ct, island_ct, summit_ct, combs_ct, field_ct, pool_ct)
						results[utility] = key

top_utilties = sorted(results.keys(), key=lambda v:-v)[:10]
for land in flex_lands:
	print(str(land) + ", ", end="")
print("")
for utility in top_utilties:
	print(str(results[utility]) + "\t" + str(utility))
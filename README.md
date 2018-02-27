# hand-simulator

## Usage

__hand.py__ contains a Hand class that accepts a filename as input, generates a deck from the given file, and generates hands from that deck. It supports several functions:

### new_hand(size)

Generates a new hand of the given size, contained within the Hand object, and returns a copy. Defaults to 7. 

### contains(cards)

Accepts the name of a card or a list of names, returns 1 if the current hand contains any of those cards, 0 otherwise.

### count_of(cards)

Accepts the name of a card or a list of names, returns the total number of those cards in the current hand. 

### expect(cards, size)

Accepts the name of a card or a list of names and a hand size, returns the hypergeometric expectation of those cards in a hand of the given size.

### set_deck(new_deck)

Accepts a filename, a list of individual cards, or a dictionary of card names and quantities. Sets the deck and decklist to the input. 

### get_deck()

Returns a copy of the internal deck, a list of individual cards.

### get_decklist()

Returns a copy of the internal decklist, a dictionary of card names and quantities. 

### has_tron()

Returns whether the current hand contains Tron, counting the first Expedition Map. Will be deprecated when I find the motivation. 

## Examples

__grixis_mana.py__, __grixis_mana_full__, __eldrazi_tron.py__, and __affinity.py__ contain applications. They all work essentially the same way. The main thing is implementing logic to classify the kinds of hands you're looking for. 

__grixis_mana.py__ tests to see how often checklands come into play untapped with a standard Grixis energy manabase. __grixis_mana_full__ tries to find the optimal grixis manabase given a set of parameters that characterize an utility function. __eldrazi_tron.py__ finds how often Eldrazi Tron gets its best draws. __affinity.py__ finds how often Affinity plays a 2- or 3-drop on turn 1. 
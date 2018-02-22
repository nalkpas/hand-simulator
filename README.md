This is outdated. I'll update it over the weekend maybe. 

# hand-simulator

## Usage

__hand.py__ contains a Hand class that accepts a filename as input, generates a deck from the given file, and generates hands from that deck. It supports four functions:

### new_hand(size)

Generates a new hand of the given size, contained within the Hand object, and returns a copy. Defaults to 7. 

### contains(cards)

Accepts the name of a card or a list of names and returns 1 if the current hand contains any of those cards, 0 otherwise.

### count_of(cards)

Accepts the name of a card or a list of names and returns the total number of those cards in the current hand. 


### has_tron()

Returns 1 if the hand has turn 3 Tron, 0 otherwise.

## Examples

__grixis.py__, __eldrazi_tron.py__, and __affinity.py__ contain applications. They're all essentially the same. The main thing is implementing logic to classify the kinds of hands you're looking for. 

__grixis.py__ tests to see how often checklands come into play untapped with a standard Grixis energy manabase. __eldrazi_tron.py__ finds how often Eldrazi Tron gets its best draws. __affinity.py__ finds how often Affinity plays a 2- or 3-drop on turn 1. 
# Utilities

import random

from eval7 import Card

def randint(low, high=None, size=None):
    if high is None:
        # If only one argument is provided, treat it as the 'high' value and set low to 0
        high = low
        low = 0

    if size is None:
        return random.randint(low, high - 1)
    else:
        return [random.randint(low, high - 1) for _ in range(size)]
    
def argmax(collection): # index of max value
    return max(enumerate(collection), key=lambda x: x[1])[0]

def mean(collection):
    return sum(collection)/len(collection)



def is_flush(cards):
    cards = [Card(s) for s in cards]
    suits = set([card.suit for card in cards])
    return len(suits) == 1

def is_straight(cards):
    cards = [Card(s) for s in cards]
    
    values = [
        card.rank for card in cards
    ]

    values = set(values)

    if len(values) != len(cards):
        return False
    
    sorted_vals = list(sorted(values))
    
    if sorted_vals[-1] - sorted_vals[0] == len(sorted_vals) - 1:
        return True
    
    if sorted_vals[-1] == 14 and (sorted_vals[-2] - sorted_vals[0] == len(sorted_vals) - 2) and sorted_vals[0] == 2:
        return True

    return False


if __name__ == "__main__":
    pass
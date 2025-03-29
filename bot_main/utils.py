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


RANK_VALUES = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
    '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11,
    'Q': 12, 'K': 13, 'A': 14
}


# def is_straight(card1, card2, card3):
#     values = {
#         RANK_VALUES[card1.rank],
#         RANK_VALUES[card2.rank],
#         RANK_VALUES[card3.rank]
#     }

#     if len(values) != 3:
#         return False
    
#     sorted_vals = list(sorted(values))
    
#     if sorted_vals[-1] - sorted_vals[0] == 2:
#         return True
    
#     return False

# if __name__ == "__main__":
#     # Write some tests for is_straight
#     assert is_straight(Card('2h'), Card('3h'), Card('4h'))
#     assert is_straight(Card('2H'), Card('4H'), Card('3H'))
#     assert is_straight(Card('3H'), Card('2H'), Card('4H'))
#     assert is_straight(Card('3H'), Card('4H'), Card('2H'))
#     assert is_straight(Card('4H'), Card('2H'), Card('3H'))
#     assert is_straight(Card('4H'), Card('3H'), Card('2H'))
#     assert not is_straight(Card('2H'), Card('2H'), Card('4H'))
#     assert not is_straight(Card('2H'), Card('3H'), Card('3H'))
#     assert not is_straight(Card('2H'), Card('2H'), Card('2H'))
#     assert not is_straight(Card('2H'), Card('3H'), Card('5H'))
#     assert not is_straight(Card('2H'), Card('4H'), Card('6H'))
#     assert not is_straight(Card('2H'), Card('5H'), Card('7H'))
#     assert not is_straight(Card('2H'), Card('6H'), Card('8H'))
#     assert not is_straight(Card('2H'), Card('7H'), Card('9H'))
#     assert not is_straight(Card('2H'), Card('8H'), Card('TH'))
#     assert not is_straight(Card('2H'), Card('9H'), Card('JH'))
#     assert not is_straight(Card('2H'), Card('TH'), Card('QH'))
#     assert not is_straight(Card('2H'), Card('JH'), Card('KH'))
#     assert not is_straight(Card('2H'), Card('KH'), Card('AH'))
#     assert not is_straight(Card('2H'), Card('AH'), Card('2H'))
#     assert not is_straight(Card('2H'), Card('AH'), Card('3H'))
#     assert not is_straight(Card('2H'), Card('AH'), Card('4H'))
#     assert not is_straight(Card('2H'), Card('AH'), Card('5H'))
#     assert not is_straight(Card('2H'), Card('AH'), Card('6H'))
#     assert not is_straight(Card('2H'), Card('AH'), Card('7H'))
#     assert not is_straight(Card('2H'), Card('AH'), Card('8H'))
#     assert not is_straight(Card('2H'), Card('AH'), Card('9H'))
#     assert not is_straight(Card('2H'), Card('AH'), Card('TH'))
#     assert not is_straight(Card('2H'), Card('AH'), Card('JH'))
#     assert not is_straight(Card('2H'), Card('AH'), Card('KH'))
#     assert not is_straight(Card('2H'), Card('AH'), Card('AH'))
#     assert not is_straight(Card('2H'), Card('AH'), Card('2H'))
#     assert not is_straight(Card('2H'), Card('AH'), Card('3H'))
#     assert not is_straight(Card('2H'), Card('AH'), Card('4H'))
#     assert not is_straight(Card('2H'), Card('AH'), Card('5H'))
#     assert not is_straight(Card('2H'), Card('AH'), Card('6H'))
#     assert not is_straight(Card('2H'), Card('AH'), Card('7H'))
#     assert not is_straight(Card('2H'), Card('AH'), Card('8H'))
#     assert not is_straight(Card('2H'), Card('AH'), Card('9H'))
#     assert not is_straight(Card('2H'), Card('AH'), Card('TH'))
#     assert not is_straight(Card('2H'), Card('AH'), Card('JH'))
#     assert not is_straight(Card('2H'), Card('AH'), Card('KH'))
#     assert not is_straight(Card('2H'), Card('AH'), Card('AH'))
#     assert not is_straight(Card('2H'), Card('AH'), Card('2H'))
#     assert not is_straight(Card('2H'), Card('AH'), Card('3H'))
#     assert not is_straight(Card('2H'), Card('AH'), Card('4H'))
#     assert not is_straight(Card('2H'), Card('AH'), Card('5H'))
#     assert not is_straight(Card('2H'), Card('AH'), Card('6H'))
    
    
    

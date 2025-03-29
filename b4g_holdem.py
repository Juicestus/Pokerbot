import eval7

# Use a monte carlo simulation to estimate the strength
# using the win rate of the hand
def hand_strength(my_cards, board_cards, k):
    # assert len(board_cards) in [0, 2, 4]
    
    MC_ITER = 100
    #my_cards = [eval7.Card(card) for card in my_cards]
    #board_cards = [eval7.Card(card) for card in board_cards]
    deck = eval7.Deck()
    for card in my_cards + board_cards:
        deck.cards.remove(card)
        
    score = 0
    for _ in range(MC_ITER):
        deck.shuffle()
        draw_number = 3 + (4 - len(board_cards))
        draw = deck.peek(draw_number)
        print(draw)
        opp_draw = draw[:k] # give the opp first 3
        board_draw = draw[k:]  
        
        my_hand = my_cards + board_cards + board_draw
        opp_hand = opp_draw + board_cards + board_draw
        
        my_value = eval7.evaluate(my_hand)
        opp_value = eval7.evaluate(opp_hand)
        
        if my_value > opp_value:
            score += 1
        elif my_value < opp_value:
            score += 0
        else:
            score += 0.5
    win_rate = score / MC_ITER
    # print(f"win rate: {win_rate}")
    return win_rate

if __name__ == '__main__':
    deck = eval7.Deck()
    my_cards = [ ]
    board_cards = ["Ah", "Qh","5h", "5d"]
    x = hand_strength(my_cards, board_cards, 2)
    print(x)
    
    
    
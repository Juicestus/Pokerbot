'''
P2 - PotOdds
'''
from skeleton.actions import FoldAction, CallAction, CheckAction, RaiseAction
from skeleton.states import GameState, TerminalState, RoundState
from skeleton.states import NUM_ROUNDS, STARTING_STACK, BIG_BLIND, SMALL_BLIND
from skeleton.bot import Bot
from skeleton.runner import parse_args, run_bot
import eval7

import random

class Player(Bot): 

    def __init__(self): # Called when a new game starts. Called exactly once.

        pass

    def handle_new_round(self, game_state, round_state, active):            
        #my_bankroll = game_state.bankroll  # the total number of chips you've gained or lost from the beginning of the game to the start of this round
        #game_clock = game_state.game_clock  # the total number of seconds your bot has left to play this game
        #round_num = game_state.round_num  # the round number from 1 to NUM_ROUNDS
        #my_cards = round_state.hands[active]  # your cards
        #big_blind = bool(active)  # True if you are the big blind
        return

    def handle_round_over(self, game_state, terminal_state, active):        
        #my_delta = terminal_state.deltas[active]  # your bankroll change from this round
        previous_state = terminal_state.previous_state  # RoundState before payoffs
        #street = previous_state.street  # 0, 3, 4, or 5 representing when this round ended
        #my_cards = previous_state.hands[active]  # your cards
        #opp_cards = previous_state.hands[1-active]  # opponent's cards or [] if not revealed
        return
    
    
    # Use a monte carlo simulation to estimate the strength
    # using the win rate of the hand
    def hand_strength(self, my_cards, board_cards):
        # assert len(board_cards) in [0, 2, 4]
        MC_ITER = 100
        my_cards = [eval7.Card(card) for card in my_cards]
        board_cards = [eval7.Card(card) for card in board_cards]
        deck = eval7.Deck()
        for card in my_cards + board_cards:
            deck.cards.remove(card)
        score = 0
        for _ in range(MC_ITER):
            deck.shuffle()
            draw_number = 3 + (4 - len(board_cards))
            draw = deck.peek(draw_number)
            print(draw)
            opp_draw = draw[:2] # give the opp first 3
            board_draw = draw[2:]  
            
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


    def get_action(self, game_state, round_state, active):
        '''
        Arguments:
            game_state: the GameState object.
            round_state: the RoundState object.
            active: your player's index.
        Returns:
            Your action.
        '''
        legal_actions = round_state.legal_actions()  # the actions you are allowed to take
        street = round_state.street  # 0, 3, 4, or 5 representing pre-flop, flop, turn, or river respectively
        my_cards = round_state.hands[active]  # your cards
        board_cards = round_state.deck[:street]  # the board cards
        my_pip = round_state.pips[active]  # the number of chips you have contributed to the pot this round of betting
        opp_pip = round_state.pips[1-active]  # the number of chips your opponent has contributed to the pot this round of betting
        # my_stack = round_state.stacks[active]  # the number of chips you have remaining
        # opp_stack = round_state.stacks[1-active]  # the number of chips your opponent has remaining
        # continue_cost = opp_pip - my_pip  # the number of chips needed to stay in the pot
        # my_contribution = STARTING_STACK - my_stack  # the number of chips you have contributed to the pot
        # opp_contribution = STARTING_STACK - opp_stack  # the number of chips your opponent has contributed to the pot

        # if RaiseAction in legal_actions:
        #    min_raise, max_raise = round_state.raise_bounds()  # the smallest and largest numbers of chips for a legal bet/raise
        #    min_cost = min_raise - my_pip  # the cost of a minimum bet/raise
        #    max_cost = max_raise - my_pip  # the cost of a maximum bet/raise
        # if RaiseAction in legal_actions:
        #     if random.random() < 0.5:
        #         return RaiseAction(min_raise)
        # if CheckAction in legal_actions:  # check-call
        #     return CheckAction()
        # if random.random() < 0.25:
        #     return FoldAction()
        # return CallAction()  # If we can't raise, call if possible

        continue_cost = opp_pip - my_pip  
        pot_odds = continue_cost / (my_pip + opp_pip + 0.1)

        P_RAISE = 0.8
        P_FOLD = 0.15

        if RaiseAction in legal_actions:
            min_raise, max_raise = round_state.raise_bounds()
            continue_cost = opp_pip - my_pip  
            pot_odds = continue_cost / (my_pip + opp_pip + 0.1)
            strength = self.hand_strength(my_cards, board_cards)
            if random.random() < P_RAISE:
                if strength > 2 * pot_odds:
                    raise_amount = int(min_raise + 0.1 * (max_raise - min_raise))
                    return RaiseAction(raise_amount)
                return RaiseAction(min_raise)
        if CheckAction in legal_actions: 
            return CheckAction()
        if random.random() < P_FOLD:
            return FoldAction()
        if CallAction in legal_actions:
            return CallAction()
        return FoldAction()
            


if __name__ == '__main__':
    run_bot(Player(), parse_args())

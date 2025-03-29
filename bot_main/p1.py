'''
Simple example pokerbot, written in Python.
'''
from skeleton.actions import FoldAction, CallAction, CheckAction, RaiseAction
from skeleton.states import GameState, TerminalState, RoundState
from skeleton.states import NUM_ROUNDS, STARTING_STACK, BIG_BLIND, SMALL_BLIND
from skeleton.bot import Bot
from skeleton.runner import parse_args, run_bot

import random

class Player(Bot): 

    def __init__(self): # Called when a new game starts. Called exactly once

        pass

    

    def handle_new_round(self, game_state, round_state, active):            
        #my_bankroll = game_state.bankroll  # the total number of chips you've gained or lost from the beginning of the game to the start of this round
        #game_clock = game_state.game_clock  # the total number of seconds your bot has left to play this game
        #round_num = game_state.round_num  # the round number from 1 to NUM_ROUNDS
        #my_cards = round_state.hands[active]  # your cards
        #big_blind = bool(active)  # True if you are the big blind
        
        
        my_cards = round_state.hands[active]  # your cards

        self.strong_hole = False

        card1 = my_cards[0]     # str of len 2
        card2 = my_cards[1]
        card3 = my_cards[2]

        card1_rank = card1[0]
        card2_rank = card2[0]
        card3_rank = card3[0]
        
        if (card1_rank == card2_rank and card2_rank == card3_rank)          \
            or (card1_rank == card2_rank and (card3_rank in "AKQJ"))        \
            or (card2_rank == card3_rank and (card1_rank in "AKQJ"))        \
            or (card1_rank == card3_rank and (card2_rank in "AKQJ"))        \
            or (card1_rank in "AKQJ" and card2_rank in "AKQJ" and card3_rank in "AKQJ"): 
            self.strong_hole = True
    

    def handle_round_over(self, game_state, terminal_state, active):        
        #my_delta = terminal_state.deltas[active]  # your bankroll change from this round
        previous_state = terminal_state.previous_state  # RoundState before payoffs
        #street = previous_state.street  # 0, 3, 4, or 5 representing when this round ended
        #my_cards = previous_state.hands[active]  # your cards
        #opp_cards = previous_state.hands[1-active]  # opponent's cards or [] if not revealed
        pass

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
        my_stack = round_state.stacks[active]  # the number of chips you have remaining
        opp_stack = round_state.stacks[1-active]  # the number of chips your opponent has remaining
        continue_cost = opp_pip - my_pip  # the number of chips needed to stay in the pot
        my_contribution = STARTING_STACK - my_stack  # the number of chips you have contributed to the pot
        opp_contribution = STARTING_STACK - opp_stack  # the number of chips your opponent has contributed to the pot

        P_RAISE = .8
        P_FOLD =  .2
        P_BLUFF = .2
        
        if RaiseAction in legal_actions:
           min_raise, max_raise = round_state.raise_bounds()  # the smallest and largest numbers of chips for a legal bet/raise
           min_cost = min_raise - my_pip  # the cost of a minimum bet/raise
           max_cost = max_raise - my_pip  # the cost of a maximum bet/raise
           
        if RaiseAction in legal_actions and self.strong_hole:

            raise_amt = int(min_raise + (max_raise - min_raise) * 0.5)

            if random.random() < P_RAISE:
                return RaiseAction(raise_amt)
            
        if RaiseAction in legal_actions:
            if random.random() < P_BLUFF:
                return RaiseAction(min_raise)

        if CheckAction in legal_actions:
            return CheckAction()
        
        if random.random() < P_FOLD:
            return FoldAction()
        
        return CallAction()

if __name__ == '__main__':
    run_bot(Player(), parse_args())

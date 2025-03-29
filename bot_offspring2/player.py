'''
P2 - PotOdds
'''
from skeleton.actions import FoldAction, CallAction, CheckAction, RaiseAction
from skeleton.states import GameState, TerminalState, RoundState
from skeleton.states import NUM_ROUNDS, STARTING_STACK, BIG_BLIND, SMALL_BLIND
from skeleton.bot import Bot
from skeleton.runner import parse_args, run_bot
import eval7
from collections import Counter


import random

class Player(Bot): 

    def __init__(self):
        '''
        Called when a new game starts. Called exactly once.
        '''
        self.opponent_actions = []
        self.hand_history = []
        self.RANKS = '23456789TJQKA'

    def handle_new_round(self, game_state, round_state, active):
        '''
        Called when a new round starts.
        '''
        self.opponent_actions = []
        self.my_cards = round_state.hands[active]
        self.big_blind = bool(active)
        self.round_num = game_state.round_num

    def handle_round_over(self, game_state, terminal_state, active):
        '''
        Called when a round ends.
        '''
        my_cards = terminal_state.previous_state.hands[active]
        opp_cards = terminal_state.previous_state.hands[1-active]
        board_cards = terminal_state.previous_state.deck[:terminal_state.previous_state.street]
        my_delta = terminal_state.deltas[active]
        
        # Store hand result for potential future analysis
        self.hand_history.append({
            'my_cards': my_cards,
            'opp_cards': opp_cards if opp_cards else [],
            'board_cards': board_cards,
            'result': my_delta
        })

    def rank_to_value(self, rank):
        """Convert card rank to numeric value."""
        return self.RANKS.index(rank)

    def evaluate_hand_strength(self, my_cards, board_cards):
        """
        Evaluate the current hand strength based on hole cards and community cards.
        Returns a value between 0 and 1, where 1 is the strongest possible hand.
        """
        if not board_cards:  # Preflop
            return self._evaluate_preflop_strength(my_cards)
        else:
            all_cards = my_cards + board_cards
            return self._evaluate_postflop_strength(all_cards)

    def _evaluate_preflop_strength(self, cards):
        """Evaluate the strength of the 3 hole cards."""
        # Check for pairs or three of a kind
        rank_counts = Counter([card[0] for card in cards])
        
        # Three of a kind
        if 3 in rank_counts.values():
            return 0.95
        
        # Pair
        if 2 in rank_counts.values():
            # Value of the pair
            pair_rank = [r for r, count in rank_counts.items() if count == 2][0]
            pair_value = self.rank_to_value(pair_rank) / (len(self.RANKS) - 1)
            # Kicker value
            kicker_rank = [r for r, count in rank_counts.items() if count == 1][0]
            kicker_value = self.rank_to_value(kicker_rank) / (len(self.RANKS) - 1)
            return 0.5 + 0.3 * pair_value + 0.1 * kicker_value
        
        # Check for flush potential
        suits = [card[1] for card in cards]
        flush_potential = len(set(suits)) == 1
        
        # Check for straight potential
        ranks = sorted([self.rank_to_value(card[0]) for card in cards])
        straight_potential = ranks[2] - ranks[0] <= 4
        
        # Check for high cards
        high_card_value = max([self.rank_to_value(card[0]) for card in cards]) / (len(self.RANKS) - 1)
        
        # Base value on high cards, with bonuses for straight/flush potential
        base_value = 0.2 + 0.3 * high_card_value
        if flush_potential:
            base_value += 0.15
        if straight_potential:
            base_value += 0.1
            
        return base_value

    def _evaluate_postflop_strength(self, all_cards):
        """Evaluate the strength of the hand after community cards are revealed."""
        # Count ranks and suits
        ranks = [card[0] for card in all_cards]
        suits = [card[1] for card in all_cards]
        rank_values = [self.rank_to_value(card[0]) for card in all_cards]
        
        rank_counts = Counter(ranks)
        suit_counts = Counter(suits)
        
        # Check for four of a kind
        if 4 in rank_counts.values():
            return 0.95
            
        # Check for full house
        has_three = 3 in rank_counts.values()
        has_pair = 2 in rank_counts.values()
        if has_three and has_pair:
            return 0.9
        
        # Check for flush (simplified - just checks if 5+ cards of same suit exist)
        if any(count >= 5 for count in suit_counts.values()):
            flush_cards = [c for c in all_cards if c[1] == max(suit_counts, key=suit_counts.get)]
            high_rank = max([self.rank_to_value(c[0]) for c in flush_cards])
            flush_strength = 0.85 + (high_rank / (len(self.RANKS) * 10))
            return flush_strength
            
        # Check for straight (simplified)
        sorted_ranks = sorted(set(rank_values))
        has_straight = False
        for i in range(len(sorted_ranks) - 4):
            if sorted_ranks[i+4] - sorted_ranks[i] == 4:
                has_straight = True
                break
        if has_straight:
            return 0.8
            
        # Check for three of a kind
        if 3 in rank_counts.values():
            trips_rank = [r for r, count in rank_counts.items() if count == 3][0]
            trips_value = self.rank_to_value(trips_rank) / (len(self.RANKS) - 1)
            return 0.7 + 0.05 * trips_value
            
        # Check for two pair
        if list(rank_counts.values()).count(2) >= 2:
            pair_ranks = [self.rank_to_value(r) for r, count in rank_counts.items() if count == 2]
            top_pair_value = max(pair_ranks) / (len(self.RANKS) - 1)
            return 0.6 + 0.05 * top_pair_value
            
        # Check for one pair
        if 2 in rank_counts.values():
            pair_rank = [r for r, count in rank_counts.items() if count == 2][0]
            pair_value = self.rank_to_value(pair_rank) / (len(self.RANKS) - 1)
            return 0.3 + 0.2 * pair_value 
            
        # High card
        high_card = max(rank_values)
        return 0.1 + 0.2 * (high_card / (len(self.RANKS) - 1))


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

        continue_cost = opp_pip - my_pip  

        P_RAISE = 0.8
        
        pot_odds = continue_cost / (my_pip + opp_pip + 0.1)
        strength = self.evaluate_hand_strength(my_cards, board_cards)

        if RaiseAction in legal_actions:
            min_raise, max_raise = round_state.raise_bounds()
            continue_cost = opp_pip - my_pip  
            
            if random.random() < P_RAISE:
                if strength > 2 * pot_odds:
                    raise_amount = int(min_raise + 0.1 * (max_raise - min_raise))
                    return RaiseAction(raise_amount)
        if CheckAction in legal_actions: 
            return CheckAction()
        return CallAction()
            


if __name__ == '__main__':
    run_bot(Player(), parse_args())

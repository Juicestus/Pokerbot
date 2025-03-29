'''
Simple example pokerbot, written in Python.
'''
from skeleton.actions import FoldAction, CallAction, CheckAction, RaiseAction
from skeleton.states import GameState, TerminalState, RoundState
from skeleton.states import NUM_ROUNDS, STARTING_STACK, BIG_BLIND, SMALL_BLIND
from skeleton.bot import Bot
from skeleton.runner import parse_args, run_bot

import random
import utils

# DEBUG ONLY
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
# ^ REMOVE FOR FINAL

import p0, p1, p2   



BOTS = {
    "Skeleton": p0.Player,
    "StrongHole": p1.Player,
    "PotOdds": p2.Player,
}

class Player(Bot):      # THIS IS THE BANDIT

    def __init__(self): # Called when a new game starts. Called exactly once.
        self.bot_names = list(BOTS.keys())
        self.bot_list = list(BOTS.values())
        self.n_bots = len(self.bot_list)
        
        self.history = []
        self.score = []
        
        for i in range(self.n_bots):
            self.history.append([]) # initialize each history with empty list
            self.score.append(0)    # initialize each score at 0

        self.current_bot = None
        self.current_bot_index = None

        self.chosen_bots = []       # history of chosen bot over time for plotting
        
        self.n_rounds = 1

    def handle_new_round(self, game_state, round_state, active):            
        #my_bankroll = game_state.bankroll  # the total number of chips you've gained or lost from the beginning of the game to the start of this round
        #game_clock = game_state.game_clock  # the total number of seconds your bot has left to play this game
        #round_num = game_state.round_num  # the round number from 1 to NUM_ROUNDS
        #my_cards = round_state.hands[active]  # your cards
        #big_blind = bool(active)  # True if you are the big blind
        
        #if game_state.round_num <= 0.2 * NUM_ROUNDS:           # biphasic approach

        P_RANDOM = 0.2

        if random.random() <= min(25/self.n_rounds, 1):         #  eplison greedy
        # if random.random() <= P_RANDOM:
            current_bot_index = utils.randint(self.n_bots)  # random bot
        else:
            current_bot_index = utils.argmax(self.score)           # empirically best bot
            

        self.current_bot_index = current_bot_index
        self.chosen_bots.append(current_bot_index)

        self.current_bot = self.bot_list[current_bot_index]()
        self.current_bot.handle_new_round(game_state, round_state, active)
        
        self.n_rounds += 1

    def handle_round_over(self, game_state, terminal_state, active):        
        #my_delta = terminal_state.deltas[active]  # your bankroll change from this round
        previous_state = terminal_state.previous_state  # RoundState before payoffs
        #street = previous_state.street  # 0, 3, 4, or 5 representing when this round ended
        #my_cards = previous_state.hands[active]  # your cards
        #opp_cards = previous_state.hands[1-active]  # opponent's cards or [] if not revealed
        
        
        my_delta = terminal_state.deltas[active]
        current_bot_history = self.history[self.current_bot_index]
        
        # update history and stats
        current_bot_history.append(my_delta)
        self.score[self.current_bot_index] = utils.mean(current_bot_history)


        # DEBUG ONLY: visualize actions at end of match
        try:
            if game_state.round_num == NUM_ROUNDS:
                plt.figure(figsize=(10, 3))
                plt.scatter(range(NUM_ROUNDS), self.chosen_bots, marker="|", alpha=0.4)
                plt.xlabel("Step")
                plt.ylabel("Chosen Bot")
                plt.title("Bandit Bot: Chosen Bots Over Time")
                plt.yticks(range(self.n_bots), labels=[f"{self.bot_names[i]}" for i in range(self.n_bots)])
                plt.savefig("../epsilon_greedy.png")
        except Exception as e:
            print("Plot errored out: ", e)
            

    def get_action(self, game_state, round_state, active):
        '''
        Arguments:
            game_state: the GameState object.
            round_state: the RoundState object.
            active: your player's index.
        Returns:
            Your action.
        '''

        # Forward the information to the current bot
        return self.current_bot.get_action(game_state, round_state, active)

if __name__ == '__main__':
    run_bot(Player(), parse_args())

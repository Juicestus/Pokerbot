# PARAMETERS TO CONTROL THE BEHAVIOR OF THE GAME ENGINE
# DO NOT REMOVE OR RENAME THIS FILE
PLAYER_1_NAME = "PotOdds3"
PLAYER_1_PATH = "./bot_potodds3"
# NO TRAILING SLASHES ARE ALLOWED IN PATHS
PLAYER_2_NAME = "Claude"
PLAYER_2_PATH = "./bot_claude"  
# GAME PROGRESS IS RECORDED HERE
GAME_LOG_FILENAME = "gamelog"
# PLAYER_LOG_SIZE_LIMIT IS IN BYTES
PLAYER_LOG_SIZE_LIMIT = 524288
# STARTING_GAME_CLOCK AND TIMEOUTS ARE IN SECONDS
ENFORCE_GAME_CLOCK = True
STARTING_GAME_CLOCK = 180.0
BUILD_TIMEOUT = 30.0
CONNECT_TIMEOUT = 30.0
# THE GAME VARIANT FIXES THE PARAMETERS BELOW
# CHANGE ONLY FOR TRAINING OR EXPERIMENTATION
NUM_ROUNDS = 5000
STARTING_STACK = 500
BIG_BLIND = 10
SMALL_BLIND = 5

PLAYER_TIMEOUT = 180.0

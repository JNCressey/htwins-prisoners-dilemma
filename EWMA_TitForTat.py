# Reminder: For the history array, "cooperate" = 1, "defect" = 0

##  ## STRATEGY ##
# * Will use the EWMA of the opponent's moves.
# * This average will be used as the probability to cooperate.
# * On the first round will be cooprative.
##  ##############

# An Exponentially Weighted Moving Average (EWMA) monitors the entire history
# while giving more weight to more recent data.

# Like tit-for-tat or forgiving-tit-for-tat, this strategy will base its
# decision on what the opponent has previously done. But instead of looking at
# one or two previous moves, it will use a moving average.

# EWMA can be iteratively calculated from the latest data point and the EWMA at
# the previous step like so:
#   memory = alpha*datapoint + (1-alpha)*memory

# The volatility of EWMA depends on a chosen constant `alpha`.
# `alpha = 2/(N+1)` puts the centre of mass of the weighting similar to if it
# were a simple average of the last N terms.
# I chose N=88 on the whim that 1/e might be a good portion to consider, and
# there will be on average 240 rounds. This makes alpha = 0.02247191011235955.
# ( Each pairing runs for `200-40*np.log(random.random())` turns.
#   random.random() is uniformly distributed in the range [0,1).
#   And Integrate[200-40*log(x),{x,0,1}] is 240.
#   Therefore the expected number of rounds is 240.)

import random

def strategy(history, memory):
    if (history.shape[1]>0): # if not first round
        # Update the moving average with the latest opponent move.
        opponent_last_move = history[1,-1]
        if memory is None:
            memory = opponent_last_move
        else:
            alpha = 0.02247191011235955
            memory = alpha*opponent_last_move + (1-alpha)*memory

    if memory is None:
        choice = "cooperate"
        # Try for the both cooperate outcome if we know nothing.
    else:
        # choose cooperate with probability of the value of `memory`.
        choice = (
            "cooperate"
            if (random.random()<memory)
            else "defect"
            )

    return choice, memory

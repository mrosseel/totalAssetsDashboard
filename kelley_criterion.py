# https://en.wikipedia.org/wiki/Kelly_criterion

# odds is how many multiples: 2 to 1 (give 2), 3 to one (give 3)
# winning_prob is chance of winning, from 0 to 1
def bet_raw(odds, winning_prob):
    losing_prob = 1 - winning_prob
    return (odds*winning_prob - losing_prob)/odds

# pretty print version of bet_raw
def bet(odds, winning_prob):
    return str(round(100*bet_raw(odds, winning_prob), 2)) + ' %'

import numpy as np

# Normalize_Action is a function which normalizes inputs based on their actions. We normalize in the range of [0, 5]
# Where 0 is the minimum for a positive/negative reaction to be considered
def Normalize_Action(severity):

    return severity / 5

# Following formula calculates karma based on the severity of the action and the current karma a character has for another character/user
def Calculate_Karma(score, severity):
    # M represents Maximum karma one could acquire
    M = 40
    karma_scale = abs(score) / 100

    karma_cap = M + (100 - M) * karma_scale
    rel_scale = 1 + 9 * karma_scale
    norm_sev = Normalize_Action(severity)

    formula = round(karma_cap * (np.exp(rel_scale * norm_sev)- 1) / (np.exp(rel_scale) - 1), 2)

    return formula


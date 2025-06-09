import numpy as np

# Normalize_Action is a function which normalizes inputs based on their actions. We normalize in the range of [0, 5]
# Where 0 is the minimum for a positive/negative reaction to be considered
def Normalize_Action(severity):

    return severity / 5

# Following formula calculates karma based on the severity of the action and the current karma a character has for another character/user
def Calculate_Karma(score, severity):

    def Normalize_Action(score):
        norm_score = (score - 0.51) / (1 - 0.51)
        return norm_score

    def Calculate_Karma(score, k):
        # M represents Maximum karma one could acquire
        M = 100

        return M * (np.exp(1) ** (k * Normalize_Action(score)) - 1) / (np.exp(1) ** k - 1)



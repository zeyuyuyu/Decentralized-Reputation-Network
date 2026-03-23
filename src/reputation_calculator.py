import math

class ReputationCalculator:
    def __init__(self, decay_rate=0.95, initial_reputation=1.0):
        self.decay_rate = decay_rate
        self.initial_reputation = initial_reputation

    def calculate_reputation(self, actions, time_elapsed):
        total_reputation = self.initial_reputation
        for action in actions:
            total_reputation += action.reputation_impact
        total_reputation *= math.pow(self.decay_rate, time_elapsed)
        return total_reputation

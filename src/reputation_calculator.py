import math

class ReputationCalculator:
    def __init__(self, decay_factor=0.95, min_reputation=0.1):
        self.decay_factor = decay_factor
        self.min_reputation = min_reputation

    def calculate_reputation(self, interactions, time_weights):
        total_reputation = 0
        for interaction, weight in zip(interactions, time_weights):
            total_reputation += interaction * weight

        return max(total_reputation * self.decay_factor, self.min_reputation)

    def calculate_time_weights(self, timestamps):
        weights = []
        for timestamp in timestamps:
            time_diff = time.time() - timestamp
            weights.append(math.exp(-time_diff / 86400))  # Decay over 1 day
        return weights

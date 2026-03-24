import time

class ReputationCalculator:
    def __init__(self, initial_reputation=100, decay_rate=0.01):
        self.initial_reputation = initial_reputation
        self.decay_rate = decay_rate
        self.last_updated = time.time()

    def calculate_reputation(self, time_delta):
        """
        Calculates the current reputation based on the initial reputation and the decay rate.
        
        Args:
            time_delta (float): The time in seconds since the last reputation update.
        
        Returns:
            float: The current reputation score.
        """
        reputation = self.initial_reputation * (1 - self.decay_rate) ** (time_delta)
        self.last_updated = time.time()
        return reputation

    def update_reputation(self, new_reputation):
        """
        Updates the initial reputation and resets the last updated time.
        
        Args:
            new_reputation (float): The new initial reputation value.
        """
        self.initial_reputation = new_reputation
        self.last_updated = time.time()

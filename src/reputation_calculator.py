import numpy as np

class ReputationCalculator:
    def __init__(self, num_dimensions):
        self.num_dimensions = num_dimensions
        self.reputation_matrix = np.zeros((num_dimensions, num_dimensions))

    def update_reputation(self, user_a, user_b, ratings):
        """Update the reputation matrix based on ratings between users."""
        for i in range(self.num_dimensions):
            self.reputation_matrix[user_a, i] += ratings[i]
            self.reputation_matrix[i, user_b] += ratings[i]

    def get_reputation(self, user):
        """Get the reputation vector for the given user."""
        return self.reputation_matrix[:, user]

    def get_total_reputation(self, user):
        """Get the total reputation score for the given user."""
        return np.sum(self.get_reputation(user))

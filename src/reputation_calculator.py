from datetime import datetime, timedelta
import math

class ReputationCalculator:
    def __init__(self):
        self.decay_factor = 0.1  # Reputation decay per day
        self.min_score = 0
        self.max_score = 100
        self.weight_factors = {
            'peer_reviews': 0.4,
            'successful_transactions': 0.3, 
            'network_participation': 0.2,
            'stake_time': 0.1
        }

    def calculate_temporal_score(self, actions, current_time=None):
        """Calculate reputation score with temporal decay
        
        Args:
            actions (list): List of tuples (timestamp, action_type, value)
            current_time (datetime): Reference time for decay calculation
        """
        if not current_time:
            current_time = datetime.now()

        weighted_score = 0
        for timestamp, action_type, value in actions:
            # Calculate time decay
            time_diff = (current_time - timestamp).days
            decay = math.exp(-self.decay_factor * time_diff)
            
            # Apply weight factor based on action type
            weight = self.weight_factors.get(action_type, 0.1)
            weighted_score += value * weight * decay

        # Normalize score
        normalized_score = max(min(weighted_score, self.max_score), self.min_score)
        return normalized_score

    def update_reputation(self, current_score, new_actions):
        """Update reputation score with new actions
        
        Args:
            current_score (float): Current reputation score
            new_actions (list): New reputation-affecting actions
        """
        temporal_impact = self.calculate_temporal_score(new_actions)
        
        # Blend new score with existing using exponential moving average
        alpha = 0.7  # Smoothing factor
        updated_score = (alpha * temporal_impact) + ((1 - alpha) * current_score)
        
        return max(min(updated_score, self.max_score), self.min_score)

    def calculate_confidence(self, actions_history):
        """Calculate confidence level in reputation score
        
        Args:
            actions_history (list): Historical actions used for score
        """
        if not actions_history:
            return 0.0

        # Consider quantity and recency of actions
        action_count = len(actions_history)
        recent_actions = sum(1 for t, _, _ in actions_history 
                           if (datetime.now() - t).days <= 30)
        
        # Confidence increases with more actions but requires recent activity
        base_confidence = 1 - math.exp(-0.1 * action_count)
        recency_factor = recent_actions / max(action_count, 1)
        
        return base_confidence * recency_factor

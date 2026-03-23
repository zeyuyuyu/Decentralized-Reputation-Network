import math
from datetime import datetime

class ReputationCalculator:
    def __init__(self):
        self.decay_factor = 0.1  # Controls how quickly old interactions lose weight
        self.min_interactions = 5  # Minimum interactions needed for reliable score
        
    def calculate_reputation(self, interactions, current_time=None):
        """
        Calculate reputation score with temporal decay weighting
        
        Args:
            interactions: List of dicts with keys:
                - timestamp: datetime of interaction
                - score: float score (-1.0 to 1.0)
                - weight: float importance weight of interaction
            current_time: datetime to calculate decay from (defaults to now)
        
        Returns:
            float: Reputation score from -1.0 to 1.0
            None: If insufficient data
        """
        if not interactions or len(interactions) < self.min_interactions:
            return None
            
        if current_time is None:
            current_time = datetime.now()
            
        weighted_sum = 0.0
        weight_sum = 0.0
        
        for interaction in interactions:
            # Calculate time decay
            time_diff = (current_time - interaction['timestamp']).days
            temporal_weight = math.exp(-self.decay_factor * time_diff)
            
            # Combine interaction weight with temporal decay
            final_weight = interaction['weight'] * temporal_weight
            
            weighted_sum += interaction['score'] * final_weight
            weight_sum += final_weight
        
        if weight_sum == 0:
            return None
            
        # Normalize to -1.0 to 1.0 range
        reputation = weighted_sum / weight_sum
        return max(min(reputation, 1.0), -1.0)
        
    def get_confidence_score(self, interactions):
        """
        Calculate confidence in the reputation score
        
        Args:
            interactions: List of interaction dicts
            
        Returns:
            float: Confidence score from 0.0 to 1.0
        """
        if not interactions:
            return 0.0
            
        # More interactions = higher confidence, up to a point
        interaction_confidence = min(len(interactions) / 20.0, 1.0)
        
        # More recent interactions = higher confidence
        recency_sum = 0.0
        current_time = datetime.now()
        
        for interaction in interactions:
            days_old = (current_time - interaction['timestamp']).days
            recency_sum += math.exp(-self.decay_factor * days_old)
            
        recency_confidence = min(recency_sum / 10.0, 1.0)
        
        # Combine factors
        return (interaction_confidence + recency_confidence) / 2.0
import math
from datetime import datetime, timedelta

class ReputationCalculator:
    def __init__(self):
        self.decay_factor = 0.1  # Controls how quickly old scores decay
        self.min_interactions = 5  # Minimum interactions needed for reliable score
        self.max_age_days = 365  # Maximum age of interactions to consider
        
    def calculate_reputation_score(self, interactions, current_time=None):
        """
        Calculate reputation score using weighted temporal decay and reliability factors
        
        Args:
            interactions: List of tuples (timestamp, score, weight)
            current_time: Current timestamp for decay calculation (defaults to now)
        
        Returns:
            float: Computed reputation score between 0 and 1
        """
        if not interactions:
            return 0.0
            
        if len(interactions) < self.min_interactions:
            return 0.0
            
        if current_time is None:
            current_time = datetime.now()
            
        weighted_sum = 0
        weight_sum = 0
        
        for timestamp, score, weight in interactions:
            if isinstance(timestamp, str):
                timestamp = datetime.fromisoformat(timestamp)
                
            age = (current_time - timestamp).days
            
            if age > self.max_age_days:
                continue
                
            # Calculate temporal decay
            decay = math.exp(-self.decay_factor * age)
            
            # Apply temporal decay to both score and weight
            effective_weight = weight * decay
            weighted_sum += score * effective_weight
            weight_sum += effective_weight
            
        if weight_sum == 0:
            return 0.0
            
        raw_score = weighted_sum / weight_sum
        
        # Apply sigmoid normalization to keep score between 0 and 1
        normalized_score = 1 / (1 + math.exp(-raw_score))
        
        return round(normalized_score, 3)
        
    def update_reputation(self, old_score, new_interaction, current_time=None):
        """
        Update reputation score with new interaction
        
        Args:
            old_score: Previous reputation score
            new_interaction: Tuple of (timestamp, score, weight)
            current_time: Current timestamp for decay calculation
            
        Returns:
            float: Updated reputation score
        """
        if current_time is None:
            current_time = datetime.now()
            
        # Blend old score with new interaction using temporal weighting
        timestamp, score, weight = new_interaction
        age = (current_time - timestamp).days if isinstance(timestamp, datetime) else 0
        
        decay = math.exp(-self.decay_factor * age)
        blend_factor = 0.7  # Controls how much new interactions affect total score
        
        updated_score = (old_score * (1 - blend_factor) + 
                        score * blend_factor * decay)
                        
        return round(updated_score, 3)
        
    def get_reliability_factor(self, num_interactions):
        """
        Calculate reliability factor based on number of interactions
        
        Args:
            num_interactions: Number of interactions for this entity
            
        Returns:
            float: Reliability factor between 0 and 1
        """
        if num_interactions < self.min_interactions:
            return num_interactions / self.min_interactions
        return 1.0
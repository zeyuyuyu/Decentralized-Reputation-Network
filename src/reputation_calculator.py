from datetime import datetime, timedelta
import math

class ReputationCalculator:
    def __init__(self):
        self.decay_factor = 0.1  # Controls how quickly old interactions lose weight
        self.max_age_days = 365  # Maximum age to consider for reputation

    def calculate_reputation_score(self, interactions, current_time=None):
        """Calculate a weighted reputation score that factors in:
        - Recency of interactions (exponential decay)
        - Interaction weight/importance
        - Positive vs negative feedback ratio
        
        Args:
            interactions (list): List of dicts containing:
                - timestamp: datetime of interaction
                - score: int/float score (-1 to +1)
                - weight: float importance weight of interaction
            current_time (datetime): Reference time (defaults to now)
        """
        if not interactions:
            return 0.0
            
        if current_time is None:
            current_time = datetime.now()

        total_weighted_score = 0.0
        total_weight = 0.0

        for interaction in interactions:
            age = (current_time - interaction['timestamp']).days
            
            # Skip if interaction is too old
            if age > self.max_age_days:
                continue
                
            # Calculate temporal decay factor
            decay = math.exp(-self.decay_factor * age)
            
            # Apply decay to interaction weight
            effective_weight = interaction['weight'] * decay
            
            total_weighted_score += interaction['score'] * effective_weight
            total_weight += effective_weight

        if total_weight == 0:
            return 0.0

        # Normalize final score to -1 to +1 range
        return total_weighted_score / total_weight

    def calculate_confidence(self, interactions, current_time=None):
        """Calculate confidence level in the reputation score based on:
        - Number of interactions
        - Age distribution of interactions
        - Consistency of scores
        
        Returns float 0-1 representing confidence level
        """
        if not interactions:
            return 0.0

        if current_time is None:
            current_time = datetime.now()

        # Factor 1: Number of interactions (more is better)
        n = len(interactions)
        num_factor = 1 - math.exp(-0.1 * n)

        # Factor 2: Recent activity
        ages = [(current_time - i['timestamp']).days for i in interactions]
        avg_age = sum(ages) / len(ages)
        recency_factor = math.exp(-0.01 * avg_age)

        # Factor 3: Score consistency
        scores = [i['score'] for i in interactions]
        variance = sum((s - sum(scores)/len(scores))**2 for s in scores) / len(scores)
        consistency_factor = math.exp(-2 * variance)

        # Combine factors
        confidence = (num_factor * 0.4 + 
                     recency_factor * 0.4 + 
                     consistency_factor * 0.2)

        return min(1.0, max(0.0, confidence))

    def get_reputation_metrics(self, interactions):
        """Calculate comprehensive reputation metrics
        
        Returns dict with:
            - score: float (-1 to +1)
            - confidence: float (0 to 1)
            - num_interactions: int
            - latest_interaction: datetime
        """
        if not interactions:
            return {
                'score': 0.0,
                'confidence': 0.0,
                'num_interactions': 0,
                'latest_interaction': None
            }

        current_time = datetime.now()
        score = self.calculate_reputation_score(interactions, current_time)
        confidence = self.calculate_confidence(interactions, current_time)
        
        latest = max(i['timestamp'] for i in interactions)

        return {
            'score': score,
            'confidence': confidence,
            'num_interactions': len(interactions),
            'latest_interaction': latest
        }
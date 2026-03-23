from datetime import datetime, timedelta
import math

class ReputationCalculator:
    def __init__(self):
        self.DECAY_FACTOR = 0.1  # 10% decay per day
        self.WEIGHT_TRANSACTIONS = 0.4
        self.WEIGHT_ENDORSEMENTS = 0.3 
        self.WEIGHT_PARTICIPATION = 0.3

    def calculate_reputation_score(self, user_data):
        """
        Calculate a user's reputation score based on weighted factors with time decay
        
        Args:
            user_data (dict): Dictionary containing:
                - transactions: List of transaction records
                - endorsements: List of endorsement records 
                - participation: List of participation records
                Each record should have a timestamp field
        
        Returns:
            float: Reputation score between 0-100
        """
        current_time = datetime.now()
        
        # Calculate component scores
        transaction_score = self._calc_transaction_score(user_data['transactions'], current_time)
        endorsement_score = self._calc_endorsement_score(user_data['endorsements'], current_time)
        participation_score = self._calc_participation_score(user_data['participation'], current_time)
        
        # Apply weights
        weighted_score = (
            transaction_score * self.WEIGHT_TRANSACTIONS +
            endorsement_score * self.WEIGHT_ENDORSEMENTS + 
            participation_score * self.WEIGHT_PARTICIPATION
        )
        
        # Normalize to 0-100 range
        return min(100, max(0, weighted_score))
    
    def _apply_time_decay(self, timestamp, current_time):
        """Apply exponential decay based on time difference"""
        days_passed = (current_time - timestamp).days
        decay = math.exp(-self.DECAY_FACTOR * days_passed)
        return decay
    
    def _calc_transaction_score(self, transactions, current_time):
        if not transactions:
            return 0
            
        score = 0
        for tx in transactions:
            decay = self._apply_time_decay(tx['timestamp'], current_time)
            score += tx['value'] * decay
        return score / len(transactions)
    
    def _calc_endorsement_score(self, endorsements, current_time):
        if not endorsements:
            return 0
            
        score = 0
        for endorsement in endorsements:
            decay = self._apply_time_decay(endorsement['timestamp'], current_time)
            score += endorsement['rating'] * decay
        return score / len(endorsements)
    
    def _calc_participation_score(self, participation, current_time):
        if not participation:
            return 0
            
        score = 0
        for activity in participation:
            decay = self._apply_time_decay(activity['timestamp'], current_time)
            score += activity['value'] * decay
        return score / len(participation)

import math
from datetime import datetime, timezone

class ReputationCalculator:
    def __init__(self, decay_factor=0.1, contribution_weights=None):
        self.decay_factor = decay_factor
        self.contribution_weights = contribution_weights or {
            'code_commits': 1.0,
            'reviews': 0.5,
            'issues': 0.3,
            'comments': 0.2
        }
        
    def calculate_reputation(self, user_contributions):
        """
        Calculate reputation score based on weighted contributions with time decay
        
        Args:
            user_contributions: dict containing contribution history
            {
                'code_commits': [(timestamp, value), ...],
                'reviews': [(timestamp, value), ...],
                'issues': [(timestamp, value), ...],
                'comments': [(timestamp, value), ...]
            }
        Returns:
            float: Calculated reputation score
        """
        total_score = 0
        current_time = datetime.now(timezone.utc).timestamp()

        for contrib_type, contributions in user_contributions.items():
            if contrib_type not in self.contribution_weights:
                continue
                
            weight = self.contribution_weights[contrib_type]
            
            for timestamp, value in contributions:
                time_diff = current_time - timestamp
                decay = math.exp(-self.decay_factor * time_diff / (30 * 24 * 3600))  # 30 day decay
                total_score += value * weight * decay
                
        return round(total_score, 2)
    
    def calculate_percentile(self, user_score, all_scores):
        """Calculate percentile ranking of a user's reputation"""
        if not all_scores:
            return 0
        below_score = sum(1 for score in all_scores if score <= user_score)
        return round((below_score / len(all_scores)) * 100, 1)
    
    def get_contribution_breakdown(self, user_contributions):
        """Get detailed breakdown of reputation by contribution type"""
        breakdown = {}
        current_time = datetime.now(timezone.utc).timestamp()
        
        for contrib_type, contributions in user_contributions.items():
            if contrib_type not in self.contribution_weights:
                continue
                
            weight = self.contribution_weights[contrib_type]
            type_score = 0
            
            for timestamp, value in contributions:
                time_diff = current_time - timestamp
                decay = math.exp(-self.decay_factor * time_diff / (30 * 24 * 3600))
                type_score += value * weight * decay
                
            breakdown[contrib_type] = round(type_score, 2)
            
        return breakdown
    
    def adjust_weights(self, new_weights):
        """Update contribution type weights"""
        if not isinstance(new_weights, dict):
            raise ValueError('Weights must be provided as a dictionary')
        
        for k, v in new_weights.items():
            if not isinstance(v, (int, float)) or v < 0:
                raise ValueError(f'Invalid weight value for {k}')
                
        self.contribution_weights.update(new_weights)
    
    def set_decay_factor(self, decay_factor):
        """Update the time decay factor"""
        if not isinstance(decay_factor, (int, float)) or decay_factor < 0:
            raise ValueError('Decay factor must be a positive number')
        self.decay_factor = decay_factor
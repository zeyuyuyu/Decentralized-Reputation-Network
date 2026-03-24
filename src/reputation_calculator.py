import math
from datetime import datetime, timezone

class ReputationCalculator:
    def __init__(self):
        self.base_score = 100
        self.time_decay_factor = 0.1
        self.min_score = 1
        
    def calculate_reputation(self, contributions, peer_ratings, timestamp):
        """Calculate reputation score based on weighted contributions and time decay
        
        Args:
            contributions (dict): Map of contribution_id to contribution metrics
            peer_ratings (dict): Map of contribution_id to list of peer ratings (0-1)
            timestamp (datetime): Current timestamp for decay calculation
            
        Returns:
            float: Calculated reputation score
        """
        if not contributions:
            return self.min_score
            
        total_score = 0
        for contrib_id, metrics in contributions.items():
            # Calculate base contribution score
            impact = metrics.get('impact', 1)
            complexity = metrics.get('complexity', 1)
            quality = metrics.get('quality', 1)
            
            contrib_score = (impact * complexity * quality)
            
            # Apply peer rating modifier
            if contrib_id in peer_ratings:
                avg_rating = sum(peer_ratings[contrib_id]) / len(peer_ratings[contrib_id])
                contrib_score *= (0.5 + avg_rating)
                
            # Apply time decay
            contrib_time = metrics.get('timestamp', timestamp)
            if isinstance(contrib_time, str):
                contrib_time = datetime.fromisoformat(contrib_time)
            
            time_diff = (timestamp - contrib_time).total_seconds() / (24 * 60 * 60) # Days
            decay = math.exp(-self.time_decay_factor * time_diff)
            contrib_score *= decay
            
            total_score += contrib_score
            
        # Normalize to base score
        final_score = self.base_score * (1 + math.log(1 + total_score))
        
        return max(self.min_score, final_score)
        
    def update_contribution(self, contribution_id, metrics):
        """Update contribution metrics
        
        Args:
            contribution_id (str): Unique identifier for contribution
            metrics (dict): Updated metrics including impact, complexity, quality
        """
        # Validate metrics
        required = {'impact', 'complexity', 'quality'}
        if not all(m in metrics for m in required):
            raise ValueError(f'Missing required metrics: {required}')
            
        for metric in ('impact', 'complexity', 'quality'):
            if not 0 <= metrics[metric] <= 1:
                raise ValueError(f'{metric} must be between 0 and 1')
                
        # Add timestamp if not present
        if 'timestamp' not in metrics:
            metrics['timestamp'] = datetime.now(timezone.utc)
            
        return metrics
        
    def add_peer_rating(self, contribution_id, rating, ratings_dict):
        """Add a peer rating for a contribution
        
        Args:
            contribution_id (str): ID of contribution being rated
            rating (float): Rating value between 0-1
            ratings_dict (dict): Dictionary storing all ratings
            
        Returns:
            dict: Updated ratings dictionary
        """
        if not 0 <= rating <= 1:
            raise ValueError('Rating must be between 0 and 1')
            
        if contribution_id not in ratings_dict:
            ratings_dict[contribution_id] = []
            
        ratings_dict[contribution_id].append(rating)
        return ratings_dict
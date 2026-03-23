from typing import Dict, List, Optional
from datetime import datetime
import math

class ReputationCalculator:
    def __init__(self):
        self.evidence_weights = {
            'transaction': 0.4,
            'review': 0.3, 
            'certification': 0.2,
            'attestation': 0.1
        }
        self.time_decay_factor = 0.1
        
    def calculate_reputation_score(self,
                                  address: str,
                                  evidence_list: List[Dict],
                                  min_required_evidence: int = 3) -> Optional[float]:
        """Calculate weighted reputation score with evidence validation
        
        Args:
            address: Blockchain address to calculate score for
            evidence_list: List of reputation evidence records
            min_required_evidence: Minimum pieces of evidence needed
            
        Returns:
            Calculated reputation score between 0-1, or None if invalid
        """
        if not evidence_list or len(evidence_list) < min_required_evidence:
            return None
            
        total_score = 0
        total_weight = 0
        
        for evidence in evidence_list:
            if not self._validate_evidence(evidence):
                continue
                
            evidence_type = evidence['type']
            evidence_weight = self.evidence_weights.get(evidence_type, 0)
            evidence_timestamp = datetime.fromisoformat(evidence['timestamp'])
            
            # Apply time decay
            time_delta = datetime.now() - evidence_timestamp
            decay = math.exp(-self.time_decay_factor * time_delta.days/365)
            
            # Calculate weighted score
            evidence_score = evidence['score'] * evidence_weight * decay
            total_score += evidence_score
            total_weight += evidence_weight
        
        if total_weight == 0:
            return None
            
        final_score = total_score / total_weight
        return max(0, min(1, final_score)) # Clamp between 0-1
    
    def _validate_evidence(self, evidence: Dict) -> bool:
        """Validate evidence record structure and data"""
        required_fields = ['type', 'timestamp', 'score', 'source']
        
        # Check required fields exist
        if not all(field in evidence for field in required_fields):
            return False
            
        # Validate evidence type
        if evidence['type'] not in self.evidence_weights:
            return False
            
        # Validate score range
        if not 0 <= evidence['score'] <= 1:
            return False
            
        # Validate timestamp format
        try:
            datetime.fromisoformat(evidence['timestamp'])
        except ValueError:
            return False
            
        return True
        
    def update_evidence_weights(self, new_weights: Dict[str, float]) -> None:
        """Update evidence type weights"""
        if not new_weights:
            return
            
        # Validate weights sum to 1
        if abs(sum(new_weights.values()) - 1.0) > 0.0001:
            raise ValueError('Evidence weights must sum to 1.0')
            
        self.evidence_weights = new_weights

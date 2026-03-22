import hashlib
import datetime
import json
from typing import Dict, List

class ReputationNode:
    def __init__(self, user_id: str, initial_reputation: float = 1.0):
        self.user_id = user_id
        self.reputation = initial_reputation
        self.staked_amount = 0.0
        self.staking_history = []

    def stake(self, amount: float):
        self.staked_amount += amount
        self.staking_history.append({
            'timestamp': datetime.datetime.now().isoformat(),
            'amount': amount
        })

    def unstake(self, amount: float):
        self.staked_amount -= amount
        self.staking_history.append({
            'timestamp': datetime.datetime.now().isoformat(),
            'amount': -amount
        })

    def update_reputation(self, delta: float):
        self.reputation += delta

class ReputationNetwork:
    def __init__(self):
        self.nodes: Dict[str, ReputationNode] = {}

    def add_node(self, user_id: str, initial_reputation: float = 1.0):
        if user_id not in self.nodes:
            self.nodes[user_id] = ReputationNode(user_id, initial_reputation)

    def stake(self, user_id: str, amount: float):
        if user_id in self.nodes:
            self.nodes[user_id].stake(amount)

    def unstake(self, user_id: str, amount: float):
        if user_id in self.nodes:
            self.nodes[user_id].unstake(amount)

    def update_reputation(self, user_id: str, delta: float):
        if user_id in self.nodes:
            self.nodes[user_id].update_reputation(delta)

    def get_reputation(self, user_id: str) -> float:
        if user_id in self.nodes:
            return self.nodes[user_id].reputation
        return 0.0

    def get_staked_amount(self, user_id: str) -> float:
        if user_id in self.nodes:
            return self.nodes[user_id].staked_amount
        return 0.0

    def get_staking_history(self, user_id: str) -> List[Dict]:
        if user_id in self.nodes:
            return self.nodes[user_id].staking_history
        return []

    def serialize(self) -> str:
        return json.dumps({
            'nodes': {
                user_id: {
                    'reputation': node.reputation,
                    'staked_amount': node.staked_amount,
                    'staking_history': node.staking_history
                }
                for user_id, node in self.nodes.items()
            }
        })

    @classmethod
    def deserialize(cls, data: str):
        obj = json.loads(data)
        network = ReputationNetwork()
        for user_id, node_data in obj['nodes'].items():
            network.add_node(user_id, node_data['reputation'])
            network.nodes[user_id].staked_amount = node_data['staked_amount']
            network.nodes[user_id].staking_history = node_data['staking_history']
        return network

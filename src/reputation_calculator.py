import datetime

class ReputationCalculator:
    def __init__(self, decay_rate=0.95):
        self.decay_rate = decay_rate

    def calculate_reputation(self, user_actions, time_decay=True):
        reputation = 0
        for action in user_actions:
            reputation += action.get('reputation_value', 0)
            if time_decay:
                time_delta = datetime.datetime.now() - action.get('timestamp', datetime.datetime.now())
                reputation *= self.decay_rate ** (time_delta.total_seconds() / (60 * 60 * 24 * 30))
        return reputation

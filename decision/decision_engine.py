from decision.scoring import score_decision
from decision.constraints import apply_constraints
from app.config import Config

class DecisionEngine:
    def select(self, actions):
        actions = apply_constraints(actions)

        scored = [(a, score_decision(a)) for a in actions]
        ranked = sorted(scored, key=lambda x: x[1], reverse=True)

        selected = [a for a, _ in ranked[:Config.MAX_ACTIONS_PER_RUN]]
        return selected, ranked
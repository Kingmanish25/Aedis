from app.config import Config

def apply_constraints(actions):
    # allow only whitelisted types
    return [a for a in actions if a.get("type") in Config.ALLOWED_ACTIONS]
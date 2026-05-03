def score_decision(action):
    # simple heuristic: priority + expected impact
    priority = action.get("priority", 1)
    impact = action.get("expected_impact", "0")
    try:
        impact_val = int(impact.split("-")[0].replace("%",""))
    except:
        impact_val = 0
    return priority * 2 + impact_val / 10.0
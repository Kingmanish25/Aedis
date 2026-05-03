def score_decision(action):
    """
    Score an action based on priority and expected impact.
    
    Args:
        action: Dict containing action details
        
    Returns:
        Float score (higher is better)
    """
    if not action or not isinstance(action, dict):
        return 0.0
    
    # Get priority (default to 1 if not specified)
    priority = action.get("priority", 1)
    if not isinstance(priority, (int, float)):
        priority = 1
    
    # Parse expected impact
    impact = action.get("expected_impact", "0")
    impact_val = 0.0
    
    try:
        if isinstance(impact, str):
            # Handle formats like "10-15%", "10%", "15"
            impact_str = impact.replace("%", "").strip()
            if "-" in impact_str:
                # Take the first value from range
                impact_val = float(impact_str.split("-")[0])
            else:
                impact_val = float(impact_str)
        elif isinstance(impact, (int, float)):
            impact_val = float(impact)
    except (ValueError, AttributeError, IndexError):
        impact_val = 0.0
    
    # Calculate score: priority weighted more heavily than impact
    # Priority range: 1-5, Impact range: 0-100
    # Formula: (priority * 20) + (impact / 10)
    # This gives priority scores of 20-100 and impact scores of 0-10
    score = (priority * 20) + (impact_val / 10.0)
    
    return max(0.0, score)  # Ensure non-negative


def validate_action_for_scoring(action):
    """
    Validate that an action has required fields for scoring.
    
    Args:
        action: Dict containing action details
        
    Returns:
        (is_valid, error_message)
    """
    if not action:
        return False, "Action is None or empty"
    
    if not isinstance(action, dict):
        return False, "Action must be a dictionary"
    
    if "name" not in action:
        return False, "Action missing 'name' field"
    
    if "type" not in action:
        return False, "Action missing 'type' field"
    
    return True, None
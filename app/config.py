class Config:
    # Database configuration
    DB_PATH = "data/finance.db"
    
    # Reasoning loop configuration
    MAX_LOOPS = 2
    CONFIDENCE_THRESHOLD = 0.8
    
    # Autonomous mode configuration
    AUTONOMOUS_MODE = True          # toggle from UI later
    MAX_ACTIONS_PER_RUN = 2         # guardrail
    ALLOWED_ACTIONS = ["notify", "report", "simulate"]  # no destructive ops
    
    # Bob AI Assistant configuration
    BOB_ENABLED = True              # Enable/disable Bob orchestration
    BOB_ORCHESTRATION_MODE = "hybrid"  # "full", "hybrid", or "fallback"
    BOB_CONFIDENCE_THRESHOLD = 0.7  # Minimum confidence for Bob decisions
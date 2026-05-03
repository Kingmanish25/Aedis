class Config:
    #OLLAMA_URL = "http://localhost:11434/api/generate"
    #MODEL = "gpt-oss:120b-cloud"
    DB_PATH = "data/finance.db"
    MAX_LOOPS = 2
    CONFIDENCE_THRESHOLD = 0.8
    # 🔥 Autonomous mode
    AUTONOMOUS_MODE = True          # toggle from UI later
    MAX_ACTIONS_PER_RUN = 2         # guardrail
    ALLOWED_ACTIONS = ["notify", "report", "simulate"]  # no destructive ops
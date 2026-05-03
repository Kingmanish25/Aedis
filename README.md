# Aedis AI

Autonomous Enterprise Decision Intelligence System using Multi-Agent Architecture.

## Overview

Aedis AI is a sophisticated multi-agent system designed for autonomous decision-making in financial analysis. It uses a workflow-based architecture with specialized agents that collaborate to analyze data, generate insights, and recommend actions.

## Architecture

### Core Components

- **Agents**: Specialized AI agents (Planner, SQL, ML, Insight, Critic, Strategy, Explanation)
- **Orchestration**: Workflow management with dependency tracking and error handling
- **Decision Engine**: Autonomous action selection and ranking
- **Memory System**: Knowledge graph and vector store for learning from past decisions
- **Event Bus**: Pub/sub system for agent communication
- **Execution Layer**: Safe action execution with constraint validation

### Key Features

- ✅ Multi-agent collaboration with dependency management
- ✅ Autonomous mode with safety constraints
- ✅ Comprehensive error handling and recovery
- ✅ Knowledge graph for causal reasoning
- ✅ Service availability validation
- ✅ Structured state management
- ✅ Event-driven architecture

## Setup

### Prerequisites

- Python 3.8+
- Groq API account (for LLM access)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Aedis
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   
   Create a `.env` file or set environment variables:
   ```bash
   export GROQ_API_KEY="your_groq_api_key_here"
   ```
   
   **Important**: Never commit API keys to version control!

4. **Generate sample database**
   ```bash
   python data/generate_data.py
   ```

## Running the Application

### Start the Streamlit UI

```bash
streamlit run app/main.py
```

The application will:
1. Validate all required services (API, database, documents)
2. Initialize agents and workflow
3. Launch the interactive UI

### Configuration

Edit `app/config.py` to customize:

```python
class Config:
    DB_PATH = "data/finance.db"
    MAX_LOOPS = 2                    # Max reasoning iterations
    CONFIDENCE_THRESHOLD = 0.8       # Confidence threshold to stop iteration
    
    # Autonomous Mode Settings
    AUTONOMOUS_MODE = True           # Enable/disable autonomous execution
    MAX_ACTIONS_PER_RUN = 2         # Maximum actions per workflow run
    ALLOWED_ACTIONS = ["notify", "report", "simulate"]  # Permitted action types
```

## Architecture Details

### Agent Dependencies

Agents execute in a specific order based on dependencies:

```
planner → sql → ml → insight → critic → strategy → explanation
    ↓       ↓     ↓       ↓
    └───────┴─────┴───────→ retrieval (optional)
```

### Workflow Execution

1. **Analysis Loop**: Iterative refinement until confidence threshold is met
2. **Strategy Generation**: Create actionable recommendations
3. **Autonomous Execution**: (Optional) Execute approved actions with safety checks
4. **Memory Storage**: Store results in knowledge graph for future learning

### Safety Features

- **Constraint Validation**: Actions validated against allowed types
- **Execution Limits**: Maximum actions per run enforced
- **Error Recovery**: Graceful degradation on agent failures
- **Service Checks**: Pre-flight validation of dependencies

## Project Structure

```
Aedis/
├── agents/              # Specialized AI agents
├── app/                 # Application entry point and config
├── data/                # Database and documents
├── decision/            # Decision engine and scoring
├── event_bus/           # Event-driven communication
├── execution/           # Action execution layer
├── ibm/                 # IBM integration (placeholder)
├── llm/                 # LLM client (Groq API)
├── memory/              # Knowledge graph and memory management
├── orchestration/       # Workflow and state management
├── tools/               # Utility tools for agents
├── ui/                  # Streamlit interface
└── utils/               # Helper utilities and service checker
```

## Development

### Adding New Agents

1. Create agent class in `agents/` inheriting from `BaseAgent`
2. Define dependencies in `orchestration/agent_dependencies.py`
3. Register agent in `app/main.py`

### Adding New Actions

1. Add action type to `Config.ALLOWED_ACTIONS`
2. Implement execution logic in `execution/executor.py`

## Security Notes

- **Never commit API keys** - Use environment variables
- **Review autonomous actions** - Check `Config.ALLOWED_ACTIONS` for permitted operations
- **Validate inputs** - All user inputs are validated before processing
- **Monitor execution** - Event bus tracks all agent activities

## Troubleshooting

### Service Check Failures

Run the service checker manually:
```python
from utils.service_checker import ServiceChecker
print(ServiceChecker.get_service_report())
```

### Database Issues

Regenerate the database:
```bash
python data/generate_data.py
```

### API Connection Issues

Verify your API key:
```bash
echo $GROQ_API_KEY
```

## Recent Improvements

- ✅ Fixed hardcoded API key security vulnerability
- ✅ Renamed OllamaClient to GroqClient for clarity
- ✅ Fixed datetime import bug in memory manager
- ✅ Improved reasoning controller logic
- ✅ Added comprehensive error handling to workflow
- ✅ Implemented event bus with bounded queue and cleanup
- ✅ Added constraint validation in executor
- ✅ Enhanced knowledge graph to preserve structured data
- ✅ Added service availability checks
- ✅ Implemented state validation schema
- ✅ Added agent dependency management

## License

Manish Rathi
EX-IBMER

## Contributing

IBM Bob Hackathon

from dataclasses import dataclass
from typing import Any
import time

@dataclass
class Event:
    agent: str
    step: str
    message: str
    data: Any = None
    timestamp: float = time.time()
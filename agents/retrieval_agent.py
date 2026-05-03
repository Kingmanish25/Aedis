from tools.retrieval_tool import RetrievalTool
from .base_agent import BaseAgent

class RetrievalAgent(BaseAgent):
    def __init__(self, name, llm, bob, event_bus=None):
        super().__init__(name, llm, bob, event_bus)
        self.tool = RetrievalTool()

    def run(self, state):
        self.emit("start", "Retrieving documents")

        query = state["query"]
        docs = self.tool.retrieve(query)

        state["docs"] = docs

        self.emit("retrieved", f"{len(docs)} documents", docs)
        self.bob.log("Retrieval", f"{len(docs)} documents retrieved")

        return state
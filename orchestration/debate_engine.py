class DebateEngine:
    def run(self, planner_output, critic_agent, strategy_agent, state):
        debate = {}

        # Planner proposal
        debate["proposal"] = planner_output

        # Critic challenges
        critique = critic_agent.llm.generate(f"Critique this plan:\n{planner_output}")
        debate["critique"] = critique

        # Strategy selects best decision
        decision = strategy_agent.llm.generate(f"""
        Proposal:
        {planner_output}

        Critique:
        {critique}

        Choose best decision and justify.
        """)

        debate["final_decision"] = decision

        return debate
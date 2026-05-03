class WorkflowTrigger:
    def trigger(self, workflow, query):
        return workflow.run(query)
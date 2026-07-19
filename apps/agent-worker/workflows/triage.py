from temporalio import workflow
from core.state import IncidentState
from agents.tier1_triage import Tier1TriageAgent
import asyncio

# --- DURABLE AI EXECUTION ---
# Why Temporal? If the LLM API crashes, or an agent needs to wait 4 hours 
# for a malware sandbox analysis to finish, Temporal guarantees the workflow 
# will pause and resume without losing the AI's state or memory.

@workflow.defn
class IncidentResponseWorkflow:
    
    @workflow.run
    async def run(self, initial_state: IncidentState) -> IncidentState:
        workflow.logger.info(f"Started Durable AI Investigation for {initial_state['incident_id']}")
        
        state = initial_state
        tier1_agent = Tier1TriageAgent()
        
        # Step 1: Tier 1 Triage
        # In a real LangGraph, this would be a compiled graph execution: `app.invoke(state)`
        # We simulate the node execution here.
        state = tier1_agent.run(state)
        
        if state["next_action"] == "close_incident":
            workflow.logger.info(f"Incident {state['incident_id']} closed by Tier 1.")
            return state
            
        if state["next_action"] == "escalate_to_tier2":
            workflow.logger.info(f"Incident {state['incident_id']} escalated to Tier 2. (Phase 6 implementation)")
            # In Phase 6, we will call the Tier2ResponderAgent here.
            
        return state

from temporalio import workflow
from core.state import IncidentState
from agents.tier1_triage import Tier1TriageAgent
from agents.tier2_responder import Tier2ResponderAgent

@workflow.defn
class IncidentResponseWorkflow:
    
    @workflow.run
    async def run(self, initial_state: IncidentState) -> IncidentState:
        workflow.logger.info(f"Started Durable AI Investigation for {initial_state['incident_id']}")
        
        state = initial_state
        tier1_agent = Tier1TriageAgent()
        tier2_agent = Tier2ResponderAgent()
        
        # --- Step 1: Tier 1 Triage ---
        state = tier1_agent.run(state)
        
        if state["next_action"] == "close_incident":
            workflow.logger.info(f"Incident {state['incident_id']} closed by Tier 1.")
            return state
            
        # --- Step 2: Handoff to Tier 2 Responder ---
        if state["next_action"] == "escalate_to_tier2":
            workflow.logger.info(f"Incident {state['incident_id']} escalated to Tier 2. Initiating deep investigation.")
            
            # Tier 2 uses MCP Tool Calling (CrowdStrike/Splunk)
            state = tier2_agent.run(state)
            
        if state["next_action"] == "await_human_review":
            workflow.logger.info(f"Incident {state['incident_id']} paused. Awaiting Human Approval for containment actions.")
            # In a real temporal workflow, this uses workflow.wait_condition to pause indefinitely
            # until a human clicks "Approve" in the React Dashboard.
            
        return state

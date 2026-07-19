from core.state import IncidentState
import json

class Tier1TriageAgent:
    """
    Tier 1 AI Analyst.
    Goal: Read raw SIEM alerts, weed out obvious false positives, 
    and escalate real threats to Tier 2.
    """
    
    def run(self, state: IncidentState) -> IncidentState:
        # In production, this calls an LLM (Claude/GPT-4) with a strict system prompt.
        # Here we simulate the LLM's reasoning engine.
        
        print(f"[Tier 1 Agent] Triaging Incident: {state['incident_id']}")
        payload = state["raw_alert_payload"]
        
        # Simulate LLM reasoning
        scratchpad_entry = f"Analyzed raw payload from {payload.get('source_vendor', 'Unknown')}."
        state["agent_scratchpad"].append(scratchpad_entry)
        
        # Basic heuristic logic for the mock
        if "test" in str(payload).lower() or payload.get("event_type") == "routine_backup":
            state["classification"] = "False Positive"
            state["next_action"] = "close_incident"
            state["agent_scratchpad"].append("Conclusion: Alert is a routine event. Closing.")
        else:
            state["classification"] = "True Positive"
            state["severity"] = "High"
            state["next_action"] = "escalate_to_tier2"
            state["agent_scratchpad"].append("Conclusion: Suspicious activity detected. Escalating to Tier 2 Incident Responder.")
            
        return state

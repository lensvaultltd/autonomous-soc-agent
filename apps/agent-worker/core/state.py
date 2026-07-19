from typing import TypedDict, List, Dict, Any, Optional

# --- HIERARCHICAL STATE GRAPH ---
# This is the single source of truth for the AI SOC.
# Agents do not "chat" with each other. They receive this IncidentState,
# mutate it, and pass it to the next node in the LangGraph state machine.

class IncidentState(TypedDict):
    incident_id: str
    tenant_id: str
    raw_alert_payload: Dict[str, Any]
    
    # Classification assigned by Tier 1
    classification: Optional[str]  # e.g., "True Positive", "False Positive"
    severity: Optional[str]        # e.g., "Critical", "High"
    
    # Evidence collected by Tier 2 (via MCP tools)
    collected_evidence: Dict[str, List[str]] # e.g., {"iocs": ["1.1.1.1"], "mitre_tactics": []}
    
    # The chronological thought process of the AI agents
    agent_scratchpad: List[str]
    
    # Routing instructions
    next_action: str # e.g., "escalate_to_tier2", "close_incident", "request_human_approval"

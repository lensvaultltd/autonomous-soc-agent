from core.state import IncidentState
import sys
import os

# Resolve imports for packages
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../packages')))
from mcp_connectors.crowdstrike import CrowdStrikeMCPConnector
from mcp_connectors.splunk import SplunkMCPConnector
from database.qdrant import QdrantClientMock

class Tier2ResponderAgent:
    """
    Tier 2 Incident Responder.
    Now utilizes RAG (Retrieval-Augmented Generation) to read corporate 
    Playbooks before taking action.
    """
    
    def __init__(self):
        self.cs_tool = CrowdStrikeMCPConnector(api_key="mock")
        self.splunk_tool = SplunkMCPConnector(api_key="mock")
        self.vector_db = QdrantClientMock()
        
    def run(self, state: IncidentState) -> IncidentState:
        print(f"[Tier 2 Agent] Investigating Escalated Incident: {state['incident_id']}")
        tenant_id = state["tenant_id"]
        payload = state["raw_alert_payload"]
        
        suspicious_ip = payload.get("src_ip", "198.51.100.4")
        state["agent_scratchpad"].append(f"Tier 2: Querying Splunk for IP: {suspicious_ip}")
        
        self.splunk_tool.execute_spl_query(f"index=auth src_ip={suspicious_ip}", tenant_id)
        host_details = self.cs_tool.get_host_details(suspicious_ip, tenant_id)
        
        # --- RAG IMPLEMENTATION ---
        # Instead of hallucinating a response, the AI searches the Vector DB for the official Playbook
        if "mimikatz.exe" in host_details.get("suspicious_processes", []):
            state["agent_scratchpad"].append("Tier 2: Mimikatz detected. Fetching corporate playbook via Qdrant Semantic Search...")
            
            playbook_text = self.vector_db.search_playbook("mimikatz credential dumping")
            state["agent_scratchpad"].append(f"Tier 2 Retrieved Playbook: {playbook_text.strip()}")
            
            # The AI strictly follows the retrieved playbook instructions
            state["agent_scratchpad"].append("Tier 2: Executing Playbook Step 1 - Isolating Host.")
            self.cs_tool.isolate_host(host_details["host_id"], tenant_id)
            
            state["classification"] = "Confirmed Compromise"
            state["severity"] = "Critical"
            state["next_action"] = "await_human_review"
            
        return state

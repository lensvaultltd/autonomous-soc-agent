from core.state import IncidentState
import sys
import os

# Resolve imports for MCP connectors
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../packages')))
from mcp_connectors.crowdstrike import CrowdStrikeMCPConnector
from mcp_connectors.splunk import SplunkMCPConnector

class Tier2ResponderAgent:
    """
    Tier 2 Incident Responder.
    Goal: Take incidents escalated by Tier 1, use MCP Tools to investigate
    evidence (CrowdStrike/Splunk), and decide on a response action (e.g., Containment).
    """
    
    def __init__(self):
        # Initialize MCP Connectors
        self.cs_tool = CrowdStrikeMCPConnector(api_key="mock")
        self.splunk_tool = SplunkMCPConnector(api_key="mock")
        
    def run(self, state: IncidentState) -> IncidentState:
        print(f"[Tier 2 Agent] Investigating Escalated Incident: {state['incident_id']}")
        tenant_id = state["tenant_id"]
        payload = state["raw_alert_payload"]
        
        # --- AI TOOL CALLING EXECUTION ---
        # The LLM decides it needs more info about the Source IP.
        suspicious_ip = payload.get("src_ip", "198.51.100.4")
        state["agent_scratchpad"].append(f"Tier 2: Need to query Splunk for recent logins from IP: {suspicious_ip}")
        
        spl_query = f"index=auth src_ip={suspicious_ip} | stats count by action"
        logs = self.splunk_tool.execute_spl_query(spl_query, tenant_id)
        
        # Store evidence
        if "iocs" not in state["collected_evidence"]:
            state["collected_evidence"]["iocs"] = []
        state["collected_evidence"]["iocs"].append(suspicious_ip)
        
        # The LLM decides the host is compromised based on the logs.
        state["agent_scratchpad"].append(f"Tier 2: Splunk logs confirm brute force attack. Querying CrowdStrike for host details on IP: {suspicious_ip}")
        
        host_details = self.cs_tool.get_host_details(suspicious_ip, tenant_id)
        
        if "mimikatz.exe" in host_details.get("suspicious_processes", []):
            state["agent_scratchpad"].append(f"Tier 2: CRITICAL THREAT DETECTED. Mimikatz found on {host_details['hostname']}.")
            state["agent_scratchpad"].append("Tier 2: Executing CrowdStrike Network Isolation protocol.")
            
            # The LLM calls the Isolation tool
            self.cs_tool.isolate_host(host_details["host_id"], tenant_id)
            
            state["classification"] = "Confirmed Compromise"
            state["severity"] = "Critical"
            state["next_action"] = "await_human_review"
            state["agent_scratchpad"].append("Tier 2: Host Isolated. Awaiting Tier 3 / SOC Manager final review.")
            
        return state

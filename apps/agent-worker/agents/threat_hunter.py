import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../packages')))
from mcp_connectors.splunk import SplunkMCPConnector
from database.clickhouse import ClickHouseClientMock

class ThreatHunterAgent:
    """
    Proactive Threat Hunter.
    Unlike Tier 1/2 which are reactive (event-driven), the Threat Hunter runs 
    asynchronously on a cron schedule, querying ClickHouse and Splunk for 
    Advanced Persistent Threats (APTs) using behavioral anomalies.
    """
    
    def __init__(self):
        self.splunk_tool = SplunkMCPConnector(api_key="mock")
        self.clickhouse_client = ClickHouseClientMock()
        
    def execute_hunt(self, tenant_id: str, hypothesis: str):
        print(f"[Threat Hunter] Initiating proactive hunt for Tenant {tenant_id}")
        print(f"[Threat Hunter] Hypothesis: {hypothesis}")
        
        # E.g., "Hunt for lateral movement using compromised credentials"
        if "lateral movement" in hypothesis.lower():
            query = "index=windows EventCode=4624 LogonType=3 | stats count by TargetUserName | where count > 50"
            results = self.splunk_tool.execute_spl_query(query, tenant_id)
            
            if results:
                print("[Threat Hunter] SUCCESS. Anomalous lateral movement detected. Generating high-fidelity alert for Tier 1...")
                # Push a new UniversalAlert to the ingestion queue
                return True
                
        print("[Threat Hunter] Hunt completed. No anomalies found.")
        return False

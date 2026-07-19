from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List
from datetime import datetime

# --- NORMALIZED SIEM/EDR ALERT SCHEMA ---
# Lens Vault orchestrates multiple vendors (Splunk, CrowdStrike, SentinelOne).
# All incoming webhooks must be normalized into this Universal Alert Schema
# before they are written to ClickHouse or evaluated by the AI Agents.

class UniversalAlert(BaseModel):
    alert_id: str = Field(..., description="Unique ID provided by the source vendor")
    tenant_id: str = Field(..., description="The Customer ID this alert belongs to")
    source_vendor: str = Field(..., description="e.g., 'CrowdStrike', 'Wazuh', 'Splunk'")
    event_type: str = Field(..., description="e.g., 'malware_detected', 'failed_login'")
    severity: str = Field(..., description="Critical, High, Medium, Low, Info")
    
    # Unified Indicators of Compromise (IOCs)
    src_ip: Optional[str] = None
    dst_ip: Optional[str] = None
    file_hash: Optional[str] = None
    username: Optional[str] = None
    hostname: Optional[str] = None
    
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    # Original raw payload for deep AI investigation if needed
    raw_payload: Dict[str, Any] = Field(default_factory=dict)

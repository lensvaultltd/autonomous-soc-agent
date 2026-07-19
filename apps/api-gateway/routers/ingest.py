from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Request
import json
import uuid
import sys
import os

# Append the packages directory to sys.path to resolve core_models
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../packages')))
from core_models.alerts import UniversalAlert

router = APIRouter(prefix="/api/v1/ingest", tags=["Ingestion"])

# Mock Message Queue (Redis / Kafka)
def push_to_kafka_queue(alert: UniversalAlert):
    """
    Push normalized alert to Kafka/Redis.
    The Python Temporal AI Agents will consume from this queue asynchronously.
    """
    print(f"[KAFKA PUBLISH] Topic: soc-alerts | Tenant: {alert.tenant_id} | Vendor: {alert.source_vendor}")

@router.post("/webhook/{tenant_id}/{vendor_id}")
async def receive_vendor_webhook(tenant_id: str, vendor_id: str, request: Request, background_tasks: BackgroundTasks):
    """
    High-throughput webhook endpoint for external vendors (CrowdStrike, Sentinel, Wazuh).
    It immediately returns a 202 Accepted to prevent vendor timeouts,
    and delegates normalization and queuing to a background worker.
    """
    try:
        raw_payload = await request.json()
    except:
        raise HTTPException(status_code=400, detail="Invalid JSON Payload")
        
    # --- Asynchronous Pipeline ---
    # 1. Normalize the vendor-specific JSON into our UniversalAlert schema
    # 2. Push to Kafka for AI Agents to process
    # 3. Write to ClickHouse for long-term telemetry
    
    normalized_alert = UniversalAlert(
        alert_id=str(uuid.uuid4()), # Generate or extract from payload
        tenant_id=tenant_id,
        source_vendor=vendor_id,
        event_type="generic_alert", # Extracted from payload in reality
        severity="High",
        raw_payload=raw_payload
    )
    
    # Defer heavy processing to background (or Kafka) to keep API latency < 10ms
    background_tasks.add_task(push_to_kafka_queue, normalized_alert)
    
    return {"status": "accepted", "message": "Alert queued for AI processing"}

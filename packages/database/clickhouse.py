# This file contains the ClickHouse schema definitions.
# ClickHouse is used because PostgreSQL cannot handle the high write-throughput 
# required for raw SIEM logs and telemetry across thousands of tenants.

CLICKHOUSE_SCHEMA = """
CREATE TABLE IF NOT EXISTS security_telemetry (
    tenant_id String,
    timestamp DateTime,
    source_vendor String,
    event_type String,
    severity String,
    src_ip String,
    hostname String,
    raw_payload String
) ENGINE = MergeTree()
PARTITION BY toYYYYMM(timestamp)
ORDER BY (tenant_id, timestamp, source_vendor);
"""

# The MergeTree engine is optimized for massive time-series data.
# We partition by Month, and Order By Tenant ID -> Timestamp, 
# ensuring lightning-fast localized queries when the AI Threat Hunter needs 
# to scan a specific customer's network traffic over the last 24 hours.

class ClickHouseClientMock:
    """Mock client demonstrating writing high-velocity alerts to ClickHouse."""
    def insert_alert(self, alert_dict: dict):
        # In production, this uses clickhouse-driver to execute bulk inserts.
        pass

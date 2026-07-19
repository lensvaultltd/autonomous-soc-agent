import stripe
from typing import Dict

# Lens Vault is an MSSP SaaS. We charge customers based on the number of endpoints 
# monitored and the volume of logs ingested.

class BillingEngine:
    """
    Usage-Based Billing Engine.
    Integrates with Stripe Metered Billing API to charge tenants at the end of the month.
    """
    def __init__(self, stripe_api_key: str):
        stripe.api_key = stripe_api_key
        
    def report_endpoint_usage(self, tenant_id: str, endpoint_count: int):
        """
        Runs daily. Reports the number of active CrowdStrike/SentinelOne 
        agents deployed by the customer.
        """
        print(f"[Billing] Reporting {endpoint_count} active endpoints for Tenant {tenant_id}")
        # stripe.SubscriptionItem.create_usage_record(
        #     "si_endpoint_item_id",
        #     quantity=endpoint_count,
        #     timestamp=int(time.time()),
        #     action='set'
        # )

    def report_log_ingestion(self, tenant_id: str, gigabytes_ingested: float):
        """
        Runs hourly. Reports the volume of SIEM logs ingested into ClickHouse.
        """
        print(f"[Billing] Reporting {gigabytes_ingested}GB of log ingestion for Tenant {tenant_id}")
        # stripe.SubscriptionItem.create_usage_record(
        #     "si_data_item_id",
        #     quantity=int(gigabytes_ingested * 1000), # Charge per MB
        #     timestamp=int(time.time()),
        #     action='increment'
        # )

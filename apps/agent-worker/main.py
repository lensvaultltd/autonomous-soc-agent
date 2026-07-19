import asyncio
from temporalio.client import Client
from temporalio.worker import Worker
from workflows.triage import IncidentResponseWorkflow

# This is the daemon that runs the AI SOC Agents 24/7.
# It listens to the Temporal task queue and picks up incidents as they arrive from the API Gateway.

async def main():
    # Connect to the Temporal cluster
    try:
        client = await Client.connect("localhost:7233")
        print("Connected to Temporal Cluster.")
    except Exception as e:
        print("Temporal cluster not reachable. (Ensure docker-compose is running). Starting mock worker...")
        # For development purposes if temporal isn't running
        while True:
            await asyncio.sleep(10)
        return

    # Run the worker
    worker = Worker(
        client,
        task_queue="soc-incident-queue",
        workflows=[IncidentResponseWorkflow],
        # activities=[mcp_tool_calls] # Phase 5 integration
    )
    
    print("AI SOC Agent Worker is listening for incidents...")
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())

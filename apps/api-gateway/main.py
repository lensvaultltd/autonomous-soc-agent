from fastapi import FastAPI, Depends
from core.auth import get_current_user, require_role, UserContext
from routers import ingest

app = FastAPI(title="Lens Vault AI SOC Ingestion API")

# Register the high-throughput ingestion routes
app.include_router(ingest.router)

@app.get("/api/v1/incidents")
async def get_incidents(current_user: UserContext = Depends(get_current_user)):
    return {
        "message": f"Welcome {current_user.user_id}. You are viewing incidents for Tenant: {current_user.tenant_id}",
        "data": []
    }

@app.post("/api/v1/admin/configure")
async def admin_only_route(current_user: UserContext = Depends(require_role(["admin", "analyst"]))):
    return {"message": "Admin configuration updated successfully."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

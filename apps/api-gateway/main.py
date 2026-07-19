from fastapi import FastAPI, Depends
from core.auth import get_current_user, require_role, UserContext

app = FastAPI(title="Lens Vault AI SOC Ingestion API")

@app.get("/api/v1/incidents")
async def get_incidents(current_user: UserContext = Depends(get_current_user)):
    # ROW LEVEL SECURITY ENFORCEMENT:
    # A customer MUST only see incidents belonging to their tenant_id.
    
    # Example pseudo-code for DB query:
    # db.query(Incident).filter(Incident.tenant_id == current_user.tenant_id).all()
    
    return {
        "message": f"Welcome {current_user.user_id}. You are viewing incidents for Tenant: {current_user.tenant_id}",
        "data": []
    }

@app.post("/api/v1/admin/configure")
async def admin_only_route(current_user: UserContext = Depends(require_role(["admin", "analyst"]))):
    # This route is protected by RBAC. Only admins and internal SOC analysts can hit it.
    return {"message": "Admin configuration updated successfully."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

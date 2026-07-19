from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from pydantic import BaseModel

security = HTTPBearer()

# In a real app, this would be fetched from Keycloak's JWKS endpoint
KEYCLOAK_PUBLIC_KEY = "MOCK_PUBLIC_KEY_FOR_JWT_VALIDATION"

class UserContext(BaseModel):
    user_id: str
    tenant_id: str
    role: str

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> UserContext:
    token = credentials.credentials
    try:
        # 1. Decode JWT (Simulated validation)
        # payload = jwt.decode(token, KEYCLOAK_PUBLIC_KEY, algorithms=["RS256"])
        
        # MOCK IMPLEMENTATION FOR STRUCTURAL PURPOSES
        if token == "mock-admin-token":
            payload = {"sub": "USR-1", "tenant_id": "TEN-1", "role": "admin"}
        elif token == "mock-customer-token":
             payload = {"sub": "USR-2", "tenant_id": "TEN-1", "role": "customer"}
        else:
             raise Exception("Invalid Mock Token")
            
        # 2. Extract Multi-Tenant Context
        return UserContext(
            user_id=payload.get("sub"),
            tenant_id=payload.get("tenant_id"),
            role=payload.get("role")
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

def require_role(required_roles: list[str]):
    """
    Dependency generator for Role-Based Access Control (RBAC).
    Ensures the user holds a specific role before accessing the endpoint.
    """
    def role_checker(current_user: UserContext = Depends(get_current_user)):
        if current_user.role not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation not permitted for this role"
            )
        return current_user
    return role_checker

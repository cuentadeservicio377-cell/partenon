"""JWT authentication and workspace context for the Partenon API."""

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from partenon_api.config import DEFAULT_WORKSPACE_ID, get_secret

ALGORITHM = "HS256"
ACCESS_TOKEN_TTL_HOURS = 12
AUTH_COOKIE_NAME = "partenon_dashboard_session"

security = HTTPBearer(auto_error=False)


@dataclass
class WorkspaceContext:
    username: str
    workspace_id: str


def create_access_token(username: str, workspace_id: str = DEFAULT_WORKSPACE_ID) -> str:
    """Create a JWT access token for the dashboard/API."""
    now = datetime.now(timezone.utc)
    payload = {
        "sub": username,
        "workspace_id": workspace_id,
        "iat": now,
        "exp": now + timedelta(hours=ACCESS_TOKEN_TTL_HOURS),
        "type": "access",
    }
    return jwt.encode(payload, get_secret(), algorithm=ALGORITHM)


def decode_token(token: str) -> dict:
    """Decode and validate a JWT."""
    try:
        return jwt.decode(token, get_secret(), algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
    except jwt.InvalidTokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc


def _extract_token(request: Request, credentials: Optional[HTTPAuthorizationCredentials]) -> Optional[str]:
    """Extract JWT from Authorization header or cookie."""
    if credentials:
        return credentials.credentials
    return request.cookies.get(AUTH_COOKIE_NAME)


async def get_current_workspace(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
) -> WorkspaceContext:
    """FastAPI dependency that returns the current workspace context."""
    token = _extract_token(request, credentials)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    payload = decode_token(token)
    return WorkspaceContext(
        username=payload.get("sub", "unknown"),
        workspace_id=payload.get("workspace_id", DEFAULT_WORKSPACE_ID),
    )


def require_workspace() -> WorkspaceContext:
    """Synchronous helper for non-dependency contexts (tests, scripts)."""
    return WorkspaceContext(username="system", workspace_id=DEFAULT_WORKSPACE_ID)

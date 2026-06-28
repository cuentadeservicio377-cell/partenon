"""Authentication routes for the dashboard/API."""

import os

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from partenon_api.auth import WorkspaceContext, create_access_token, get_current_workspace

router = APIRouter(prefix="/auth", tags=["auth"])


class TokenRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class MeResponse(BaseModel):
    username: str
    workspace_id: str


def _get_expected_creds() -> tuple:
    username = os.environ.get("DASHBOARD_APP_USERNAME")
    password = os.environ.get("DASHBOARD_APP_PASSWORD")
    if not username or not password:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Dashboard credentials are not configured",
        )
    return username, password


@router.post("/token")
async def login(body: TokenRequest) -> TokenResponse:
    expected_user, expected_pass = _get_expected_creds()
    if body.username != expected_user or body.password != expected_pass:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token(body.username)
    return TokenResponse(access_token=token)


@router.get("/me")
async def me(ctx: WorkspaceContext = Depends(get_current_workspace)) -> MeResponse:
    return MeResponse(username=ctx.username, workspace_id=ctx.workspace_id)

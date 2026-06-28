"""Google Workspace client for Partenon MCP server.

Supports service-account JSON or OAuth 2.0 credentials. Falls back to dry-run
when no credentials are configured.
"""

import json
import os
from base64 import urlsafe_b64encode
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2.service_account import Credentials as ServiceAccountCredentials
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/gmail.compose",
]


def _load_credentials() -> Optional[Credentials]:
    service_account_path = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
    if service_account_path and Path(service_account_path).exists():
        return ServiceAccountCredentials.from_service_account_file(
            service_account_path, scopes=SCOPES
        )

    client_id = os.environ.get("GOOGLE_OAUTH_CLIENT_ID")
    client_secret = os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET")
    if client_id and client_secret:
        token_path = Path.home() / ".partenon" / "google_token.json"
        token_path.parent.mkdir(parents=True, exist_ok=True)
        creds = None
        if token_path.exists():
            creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                from google_auth_oauthlib.flow import InstalledAppFlow

                flow = InstalledAppFlow.from_client_config(
                    {
                        "installed": {
                            "client_id": client_id,
                            "client_secret": client_secret,
                            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                            "token_uri": "https://oauth2.googleapis.com/token",
                        }
                    },
                    SCOPES,
                )
                creds = flow.run_local_server(port=0)
            token_path.write_text(creds.to_json(), encoding="utf-8")
        return creds

    return None


def _get_service(api_name: str, version: str):
    creds = _load_credentials()
    if not creds:
        raise RuntimeError("Google Workspace credentials not configured")
    return build(api_name, version, credentials=creds, cache_discovery=False)


class GoogleWorkspaceClient:
    """Thin wrapper around Google Workspace APIs."""

    def create_spreadsheet(self, title: str) -> dict:
        service = _get_service("sheets", "v4")
        spreadsheet = {"properties": {"title": title}}
        result = service.spreadsheets().create(body=spreadsheet).execute()
        return {"spreadsheet_id": result["spreadsheetId"], "title": result["properties"]["title"]}

    def write_to_sheets(self, spreadsheet_id: str, range_name: str, values: list) -> dict:
        service = _get_service("sheets", "v4")
        body = {"values": values}
        result = (
            service.spreadsheets()
            .values()
            .update(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption="USER_ENTERED",
                body=body,
            )
            .execute()
        )
        return {"updated_cells": result.get("updatedCells", 0)}

    def read_sheet(self, spreadsheet_id: str, range_name: str) -> dict:
        service = _get_service("sheets", "v4")
        result = (
            service.spreadsheets()
            .values()
            .get(spreadsheetId=spreadsheet_id, range=range_name)
            .execute()
        )
        return {"values": result.get("values", [])}

    def create_document(self, title: str, content: Optional[str] = None) -> dict:
        service = _get_service("docs", "v1")
        doc = {"title": title}
        result = service.documents().create(body=doc).execute()
        doc_id = result["documentId"]
        if content:
            requests = [{"insertText": {"location": {"index": 1}, "text": content}}]
            service.documents().batchUpdate(documentId=doc_id, body={"requests": requests}).execute()
        return {"document_id": doc_id, "title": result["title"]}

    def create_presentation(self, title: str) -> dict:
        service = _get_service("slides", "v1")
        presentation = {"title": title}
        result = service.presentations().create(body=presentation).execute()
        return {"presentation_id": result["presentationId"], "title": result["title"]}

    def create_calendar_event(
        self,
        summary: str,
        start: str,
        end: str,
        attendees: Optional[list] = None,
        description: str = "",
    ) -> dict:
        service = _get_service("calendar", "v3")
        event_body = {
            "summary": summary,
            "description": description,
            "start": {"dateTime": start, "timeZone": "UTC"},
            "end": {"dateTime": end, "timeZone": "UTC"},
            "attendees": [{"email": e} for e in (attendees or [])],
        }
        result = service.events().insert(calendarId="primary", body=event_body).execute()
        return {"event_id": result["id"], "html_link": result.get("htmlLink", "")}

    def send_email(self, to: str, subject: str, body: str) -> dict:
        service = _get_service("gmail", "v1")
        message = f"To: {to}\r\nSubject: {subject}\r\n\r\n{body}"
        encoded = urlsafe_b64encode(message.encode("utf-8")).decode("ascii")
        result = service.users().messages().send(userId="me", body={"raw": encoded}).execute()
        return {"message_id": result["id"]}


def iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()

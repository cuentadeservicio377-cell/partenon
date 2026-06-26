"""
Partenon Tesorero - Google Sheets Integration
Tools for reading, writing and building financial dashboards in Sheets.
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, List, Optional

# Google API imports (optional - graceful degradation if not installed)
try:
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    GOOGLE_AVAILABLE = True
except ImportError:
    GOOGLE_AVAILABLE = False


class GoogleSheets:
    """Integration with Google Sheets API for finance dashboards."""

    SCOPES = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]

    def __init__(self, service_account_path: Optional[str] = None):
        self.service_account_path = service_account_path
        self.credentials = None
        self._service = None
        self._drive_service = None

    def _init_credentials(self) -> bool:
        """Initialize Google API credentials."""
        if not GOOGLE_AVAILABLE:
            return False

        if self.credentials:
            return True

        path = self._find_service_account()
        if not path:
            return False

        try:
            self.credentials = service_account.Credentials.from_service_account_file(
                str(path),
                scopes=self.SCOPES
            )
            return True
        except Exception as e:
            print(f"Failed to load Google credentials: {e}")
            return False

    def _find_service_account(self) -> Optional[Path]:
        """Find the service account JSON file."""
        if self.service_account_path:
            candidate = Path(self.service_account_path)
            if candidate.exists():
                return candidate

        env_path = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON", "")
        if env_path:
            candidate = Path(env_path)
            if candidate.exists():
                return candidate

        # Common locations
        filenames = ["google-service-account.json", "service-account.json"]
        locations = [
            Path.cwd(),
            Path.cwd() / "config",
            Path.home() / ".partenon",
            Path.home() / ".hermes",
        ]
        for filename in filenames:
            for location in locations:
                candidate = location / filename
                if candidate.exists():
                    return candidate

        return None

    def _get_service(self):
        """Get or create Google Sheets API service."""
        if self._service is None:
            if not self._init_credentials():
                return None
            try:
                self._service = build("sheets", "v4", credentials=self.credentials)
            except Exception as e:
                print(f"Failed to create Sheets service: {e}")
                return None
        return self._service

    def _get_drive_service(self):
        """Get or create Google Drive API service."""
        if self._drive_service is None:
            if not self._init_credentials():
                return None
            try:
                self._drive_service = build("drive", "v3", credentials=self.credentials)
            except Exception as e:
                print(f"Failed to create Drive service: {e}")
                return None
        return self._drive_service

    def read_sheet(self, spreadsheet_id: str, range_name: str) -> List[List[Any]]:
        """Read values from a spreadsheet range."""
        service = self._get_service()
        if not service:
            return []

        try:
            result = service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id,
                range=range_name
            ).execute()
            return result.get("values", [])
        except HttpError as e:
            print(f"Failed to read range {range_name}: {e}")
            return []

    def write_sheet(self, spreadsheet_id: str, range_name: str, values: List[List[Any]]) -> bool:
        """Write values to a spreadsheet range."""
        service = self._get_service()
        if not service:
            return False

        try:
            body = {"values": values}
            service.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption="USER_ENTERED",
                body=body
            ).execute()
            return True
        except HttpError as e:
            print(f"Failed to write range {range_name}: {e}")
            return False

    def append_row(self, spreadsheet_id: str, range_name: str, row: List[Any]) -> bool:
        """Append a single row to a spreadsheet."""
        service = self._get_service()
        if not service:
            return False

        try:
            body = {"values": [row]}
            service.spreadsheets().values().append(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption="USER_ENTERED",
                insertDataOption="INSERT_ROWS",
                body=body
            ).execute()
            return True
        except HttpError as e:
            print(f"Failed to append row to {range_name}: {e}")
            return False

    def create_spreadsheet(self, title: str) -> Optional[str]:
        """Create a new spreadsheet. Returns spreadsheet ID."""
        service = self._get_service()
        if not service:
            return None

        try:
            spreadsheet = {"properties": {"title": title}}
            result = service.spreadsheets().create(body=spreadsheet).execute()
            return result.get("spreadsheetId")
        except HttpError as e:
            print(f"Failed to create spreadsheet: {e}")
            return None

    def get_or_create_spreadsheet(self, title: str) -> Optional[str]:
        """Find spreadsheet by title or create it."""
        drive = self._get_drive_service()
        if drive:
            try:
                query = f"mimeType='application/vnd.google-apps.spreadsheet' and name='{title}' and trashed=false"
                results = drive.files().list(
                    q=query,
                    spaces="drive",
                    fields="files(id, name)"
                ).execute()
                files = results.get("files", [])
                if files:
                    return files[0].get("id")
            except HttpError as e:
                print(f"Failed to search spreadsheet: {e}")

        return self.create_spreadsheet(title)

    def create_dashboard(self, title: str = "Partenon Finanzas") -> Optional[str]:
        """Create master finance dashboard with base sheets."""
        spreadsheet_id = self.get_or_create_spreadsheet(title)
        if not spreadsheet_id:
            return None

        sheets_config = [
            {"title": "Resumen Mensual"},
            {"title": "Flujo de Caja"},
            {"title": "Costos Fijos"},
            {"title": "Costos Variables"},
            {"title": "Proveedores"},
            {"title": "Presupuestos vs Real"},
            {"title": "Alertas"},
        ]

        service = self._get_service()
        if not service:
            return spreadsheet_id

        try:
            spreadsheet = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
            existing_titles = {s["properties"]["title"] for s in spreadsheet.get("sheets", [])}

            requests = []
            for sheet in sheets_config:
                if sheet["title"] not in existing_titles:
                    requests.append({
                        "addSheet": {
                            "properties": {"title": sheet["title"]}
                        }
                    })

            if requests:
                service.spreadsheets().batchUpdate(
                    spreadsheetId=spreadsheet_id,
                    body={"requests": requests}
                ).execute()

            self._seed_headers(spreadsheet_id)
            return spreadsheet_id
        except HttpError as e:
            print(f"Failed to create dashboard: {e}")
            return spreadsheet_id

    def _seed_headers(self, spreadsheet_id: str):
        """Write default headers to dashboard sheets."""
        headers = {
            "Resumen Mensual": [
                ["Periodo", "Ingresos", "Gastos", "Balance", "Margen %", "Transacciones", "Actualizado"]
            ],
            "Flujo de Caja": [
                ["Mes", "Ingresos", "Gastos Fijos", "Gastos Variables", "Balance", "Acumulado"]
            ],
            "Costos Fijos": [
                ["Fecha", "Concepto", "Monto", "Categoria", "Proveedor", "Frecuencia", "Vencimiento"]
            ],
            "Costos Variables": [
                ["Fecha", "Concepto", "Monto", "Categoria", "Proveedor", "Proyecto", "Fijo/Variable"]
            ],
            "Proveedores": [
                ["ID", "Nombre", "Contacto", "Telefono", "Email", "Especialidad", "Monto Total", "Calificacion"]
            ],
            "Presupuestos vs Real": [
                ["Area", "Periodo", "Presupuestado", "Real", "Diferencia", "% Variacion", "Estado"]
            ],
            "Alertas": [
                ["Tipo", "Descripcion", "Categoria", "Monto", "Severidad", "Accion Sugerida", "Fecha"]
            ],
        }

        for sheet_name, values in headers.items():
            self.write_sheet(spreadsheet_id, f"{sheet_name}!A1", values)


# Singleton instance
_sheets_instance = None


def get_google_sheets(service_account_path: Optional[str] = None) -> GoogleSheets:
    """Get or create singleton Google Sheets instance."""
    global _sheets_instance
    if _sheets_instance is None:
        _sheets_instance = GoogleSheets(service_account_path=service_account_path)
    return _sheets_instance

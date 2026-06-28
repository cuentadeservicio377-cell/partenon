"""
Partenon Onboarding Engine.

Automates the full onboarding process: config, Google Workspace setup,
folder structure, templates, and first-project creation.
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

sys.path.insert(0, str(Path(__file__).parent))

try:
    from .config_loader import ConfigLoader, get_config
except ImportError:
    from config_loader import ConfigLoader, get_config


class OnboardingEngine:
    """
    Automates the complete onboarding workflow for a new Partenon installation.

    Steps:
    1. Validate or create company.yaml
    2. Create local data structure
    3. Create industry-specific catalog
    4. Generate sample data
    5. Set up Google Workspace (if configured)
    6. Generate welcome documents
    """

    def __init__(self, config_path: str = None):
        self.config = ConfigLoader(config_path) if config_path else get_config()
        current = Path(__file__).resolve()
        self.project_root = current.parent.parent.parent
        if not (self.project_root / "config").exists():
            cwd = Path.cwd()
            if (cwd / "config").exists():
                self.project_root = cwd
            elif (cwd.parent / "config").exists():
                self.project_root = cwd.parent
        self.data_dir = self.project_root / "data"
        self.data_dir.mkdir(exist_ok=True)
        self.results: Dict[str, Any] = {
            "success": True,
            "steps": [],
            "errors": [],
        }

    def run_full_onboarding(self) -> Dict[str, Any]:
        """Run the complete onboarding process."""
        self._log_step("Starting Partenon onboarding", "info")
        self._validate_config()
        self._create_local_data_structure()
        self._create_industry_catalog()
        self._create_sample_data()
        self._setup_google_workspace()
        self._generate_welcome_documents()
        self._log_step("Onboarding completed", "success")
        return self.results

    def _log_step(self, message: str, status: str = "info"):
        """Log a step result."""
        self.results["steps"].append({
            "message": message,
            "status": status,
            "timestamp": datetime.now().isoformat(),
        })
        print(f"  [{status}] {message}")

    def _validate_config(self):
        """Validate company configuration."""
        name = self.config.name
        if not name or name == "My Company":
            self._log_step(
                "Company configuration not completed. Run: python3 partenon-core/tools/onboarding_flow.py",
                "warning",
            )
            self.results["success"] = False
            return
        self._log_step(f"Company configured: {name}", "success")

    def _create_local_data_structure(self):
        """Create local JSON data files if they do not exist."""
        files = {
            "clients.json": {"clients": [], "next_id": 1},
            "projects.json": {"projects": [], "next_id": 1},
            "tasks.json": {"tasks": [], "next_id": 1},
            "quotes.json": {"quotes": [], "next_num": 1},
            "pipeline.json": {"entries": []},
            "checklists.json": {},
            "catalog.json": {},
            "events.json": {"events": []},
            "nudges.json": {"nudges": []},
            "goals.json": {"goals": []},
        }
        for filename, default_data in files.items():
            filepath = self.data_dir / filename
            if not filepath.exists():
                with open(filepath, "w", encoding="utf-8") as f:
                    json.dump(default_data, f, ensure_ascii=False, indent=2)
                self._log_step(f"Created: data/{filename}", "success")
            else:
                self._log_step(f"Exists: data/{filename}", "info")

    def _create_industry_catalog(self):
        """Create service catalog based on industry."""
        catalog_file = self.data_dir / "catalog.json"
        industry = self.config.industry
        currency = self.config.currency
        catalogs = {
            "events": {
                "services": [
                    {"code": "EVT-BAS", "name": "Basic Package", "description": "Basic event decoration", "base_price": 50000, "unit": "event"},
                    {"code": "EVT-INT", "name": "Intermediate Package", "description": "Intermediate decoration + furniture", "base_price": 100000, "unit": "event"},
                    {"code": "EVT-PRE", "name": "Premium Package", "description": "Premium decoration + furniture + lighting", "base_price": 180000, "unit": "event"},
                    {"code": "EVT-MES", "name": "Candy table", "description": "Custom candy table", "base_price": 8000, "unit": "table"},
                    {"code": "EVT-FLO", "name": "Floral arrangement", "description": "Centerpieces and floral decoration", "base_price": 5000, "unit": "arrangement"},
                ],
                "multipliers": {"high_season": 1.2, "low_season": 0.9, "urgency": 1.3}
            },
            "legal": {
                "services": [
                    {"code": "LEG-CON", "name": "Contract review", "description": "Review and legal opinion of a contract", "base_price": 15000, "unit": "contract"},
                    {"code": "LEG-DEM", "name": "Demand drafting", "description": "Civil or commercial demand", "base_price": 35000, "unit": "demand"},
                    {"code": "LEG-ASE", "name": "Monthly advisory", "description": "Monthly preventive legal advisory", "base_price": 12000, "unit": "month"},
                    {"code": "LEG-REP", "name": "Judicial representation", "description": "Representation in trial", "base_price": 50000, "unit": "trial"},
                    {"code": "LEG-CONS", "name": "Legal consultation", "description": "Point consultation", "base_price": 3000, "unit": "consultation"},
                ],
                "multipliers": {"high_complexity": 1.5, "medium_complexity": 1.2, "urgency": 1.3}
            },
            "consulting": {
                "services": [
                    {"code": "CON-DIA", "name": "Diagnosis", "description": "Initial business diagnosis", "base_price": 25000, "unit": "diagnosis"},
                    {"code": "CON-EST", "name": "Strategy", "description": "Strategic plan", "base_price": 50000, "unit": "plan"},
                    {"code": "CON-IMP", "name": "Implementation", "description": "Strategy implementation", "base_price": 40000, "unit": "month"},
                    {"code": "CON-CAP", "name": "Training", "description": "Workshop or training", "base_price": 15000, "unit": "session"},
                ],
                "multipliers": {"large_company": 1.5, "medium_company": 1.2, "urgency": 1.2}
            },
            "retail": {
                "services": [
                    {"code": "RTL-PRO", "name": "Product A", "description": "Product description", "base_price": 500, "unit": "piece"},
                    {"code": "RTL-PRB", "name": "Product B", "description": "Product description", "base_price": 800, "unit": "piece"},
                    {"code": "RTL-ENV", "name": "Shipping", "description": "Home delivery", "base_price": 150, "unit": "shipment"},
                ],
                "multipliers": {"wholesale": 0.85, "retail": 1.0}
            },
        }
        default_catalog = catalogs.get(industry, catalogs["consulting"])
        if not catalog_file.exists() or catalog_file.stat().st_size < 50:
            with open(catalog_file, "w", encoding="utf-8") as f:
                json.dump(default_catalog, f, ensure_ascii=False, indent=2)
            self._log_step(f"Service catalog created for industry: {industry}", "success")
        else:
            self._log_step("Service catalog already exists", "info")

    def _create_sample_data(self):
        """Create sample/demo data if database is empty."""
        clients_file = self.data_dir / "clients.json"
        projects_file = self.data_dir / "projects.json"
        with open(clients_file, "r", encoding="utf-8") as f:
            clients_data = json.load(f)
        if clients_data.get("clients"):
            self._log_step("Clients already exist, skipping sample data", "info")
            return
        sample_client = {
            "id": "CLI-001",
            "name": "Example Client",
            "email": "client@example.test",
            "phone": "+1 555 0100 0001",
            "project_type": "example project",
            "source": "onboarding",
            "status": "prospect",
            "notes": "Client created automatically during onboarding",
            "registration_date": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "projects": ["PROJ-001"],
        }
        sample_project = {
            "id": "PROJ-001",
            "name": "Welcome Project",
            "client_id": "CLI-001",
            "client_name": "Example Client",
            "description": "Example project to get familiar with Partenon",
            "type": self.config.industry,
            "status": "planned",
            "amount": 0,
            "created": datetime.now().isoformat(),
            "start_date": datetime.now().isoformat(),
            "delivery_date": datetime.now().isoformat(),
            "completed_date": None,
            "progress": 0,
            "tasks": [],
            "checklist": [],
            "notes": "",
            "history": [{"action": "Created during onboarding", "date": datetime.now().isoformat()}],
        }
        clients_data["clients"] = [sample_client]
        clients_data["next_id"] = 2
        with open(clients_file, "w", encoding="utf-8") as f:
            json.dump(clients_data, f, ensure_ascii=False, indent=2)
        with open(projects_file, "r", encoding="utf-8") as f:
            projects_data = json.load(f)
        projects_data["projects"] = [sample_project]
        projects_data["next_id"] = 2
        with open(projects_file, "w", encoding="utf-8") as f:
            json.dump(projects_data, f, ensure_ascii=False, indent=2)
        self._log_step("Sample data created (client + project)", "success")

    def _setup_google_workspace(self):
        """Set up Google Workspace if configured."""
        if not self.config.integration_active("google_workspace"):
            self._log_step("Google Workspace is not active, skipping", "info")
            return
        try:
            from google_workspace import get_google_workspace
            gw = get_google_workspace()
            if not gw._init_credentials():
                self._log_step("Could not load Google credentials", "warning")
                return
            company_name = self.config.name
            folder_name = f"Partenon — {company_name}"
            folder_id = gw.get_or_create_folder(folder_name)
            if folder_id:
                self._log_step(f"Drive folder created: {folder_name}", "success")
                subfolders = ["Clients", "Projects", "Templates"]
                for sub in subfolders:
                    sub_id = gw.get_or_create_folder(sub, folder_id)
                    if sub_id:
                        self._log_step(f"  └─ {sub}/", "success")
            spreadsheet_id = gw.create_spreadsheet("Project Index")
            if spreadsheet_id:
                self._log_step("Master spreadsheet created: Project Index", "success")
                gw.update_spreadsheet_values(
                    spreadsheet_id,
                    "Projects!A1:H1",
                    [["ID", "Name", "Client", "Type", "Status", "Date", "Amount", "Drive Link"]],
                )
                gw.update_spreadsheet_values(
                    spreadsheet_id,
                    "Clients!A1:G1",
                    [["ID", "Name", "Email", "Phone", "Source", "Status", "Registration Date"]],
                )
                gw.update_spreadsheet_values(
                    spreadsheet_id,
                    "Finance!A1:E1",
                    [["Project ID", "Income", "Expense", "Margin", "Payment Status"]],
                )
                self._log_step("  └─ Sheet headers created", "success")
        except Exception as e:
            self._log_step(f"Error configuring Google Workspace: {e}", "error")
            self.results["errors"].append(str(e))

    def _generate_welcome_documents(self):
        """Generate welcome/guide documents."""
        docs_dir = self.project_root / "docs"
        docs_dir.mkdir(exist_ok=True)
        welcome_file = docs_dir / "WELCOME.md"
        company = self.config.name
        industry = self.config.industry
        welcome_content = f"""# Welcome to Partenon

## {company}

Partenon is now configured for your company.

## What can you do now?

1. **Talk to Hermes via Telegram**
   - Send: "Register a new client"
   - Send: "Quote a service"
   - Send: "What do we have pending?"

2. **Use the Web Dashboard**
   ```bash
   cd dashboard
   npm install
   npm run dev
   ```
   Open http://localhost:3000

3. **Manage your business**
   - Clients and prospects
   - Quotes and pipeline
   - Projects and tasks
   - Automatic documents

## Useful first commands

| Command | Description |
|---------|-------------|
| `/company` | View configuration |
| `/clients` | List clients |
| `/projects` | List projects |
| `/status` | Business summary |

## Industry: {industry}

Partenon comes preconfigured with:
- Service catalog for {industry}
- Document templates
- Checklists per phase

---

*Document generated automatically by Partenon Onboarding*
"""
        with open(welcome_file, "w", encoding="utf-8") as f:
            f.write(welcome_content)
        self._log_step(f"Welcome guide created: docs/WELCOME.md", "success")

    def get_onboarding_status(self) -> Dict[str, Any]:
        """Get current onboarding status."""
        status = {
            "config_exists": self.config.config_path.exists(),
            "company_name": self.config.name,
            "industry": self.config.industry,
            "data_dir_exists": self.data_dir.exists(),
            "google_workspace_active": self.config.integration_active("google_workspace"),
            "profiles_active": [],
        }
        for profile in ["scribe", "herald", "collector", "guardian", "strategist", "diplomat", "brain"]:
            if self.config.department_active(profile):
                status["profiles_active"].append(profile)
        return status


_onboarding_instance = None


def get_onboarding_engine() -> OnboardingEngine:
    """Get or create singleton OnboardingEngine instance."""
    global _onboarding_instance
    if _onboarding_instance is None:
        _onboarding_instance = OnboardingEngine()
    return _onboarding_instance


if __name__ == "__main__":
    engine = OnboardingEngine()
    result = engine.run_full_onboarding()
    print("\n" + "=" * 50)
    if result["success"]:
        print("Onboarding completed successfully")
    else:
        print("Onboarding completed with warnings")
    if result["errors"]:
        print("\nErrors:")
        for err in result["errors"]:
            print(f"  - {err}")

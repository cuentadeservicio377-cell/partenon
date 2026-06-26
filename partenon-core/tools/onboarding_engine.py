"""
Hermes Business OS — Onboarding Engine
Automates the full onboarding process: config, Google Workspace setup,
folder structure, templates, and first-project creation.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

import sys
sys.path.insert(0, str(Path(__file__).parent))

from config_loader import get_config, ConfigLoader


class OnboardingEngine:
    """
    Automates the complete onboarding workflow for a new HBOS installation.
    
    Steps:
    1. Validate or create empresa.yaml
    2. Create Google Drive folder structure
    3. Create Google Sheets masters
    4. Generate industry-specific templates
    5. Create welcome project / sample data
    6. Verify everything with hbos doctor
    """
    
    def __init__(self, config_path: str = None):
        self.config = ConfigLoader(config_path) if config_path else get_config()
        # Find project root: go up from skills/hermes-business-core/tools/
        current = Path(__file__).resolve()
        self.project_root = current.parent.parent.parent.parent  # up to project root
        # Fallback: if we can't find the right root, try current working directory
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
        self._log_step("Iniciando onboarding de Hermes Business OS", "info")
        
        # Step 1: Validate config
        self._validate_config()
        
        # Step 2: Create local data structure
        self._create_local_data_structure()
        
        # Step 3: Create industry-specific catalog
        self._create_industry_catalog()
        
        # Step 4: Create sample data if empty
        self._create_sample_data()
        
        # Step 5: Setup Google Workspace (if configured)
        self._setup_google_workspace()
        
        # Step 6: Generate welcome documents
        self._generate_welcome_documents()
        
        self._log_step("Onboarding completado", "success")
        return self.results
    
    def _log_step(self, message: str, status: str = "info"):
        """Log a step result."""
        self.results["steps"].append({
            "message": message,
            "status": status,
            "timestamp": datetime.now().isoformat(),
        })
        
        emoji = {"info": "ℹ️", "success": "✅", "warning": "⚠️", "error": "❌"}.get(status, "•")
        print(f"  {emoji} {message}")
    
    def _validate_config(self):
        """Validate company configuration."""
        nombre = self.config.nombre
        if not nombre or nombre == "Mi Empresa":
            self._log_step("Configuración de empresa no completada. Ejecuta: hbos setup", "warning")
            self.results["success"] = False
            return
        
        self._log_step(f"Empresa configurada: {nombre}", "success")
    
    def _create_local_data_structure(self):
        """Create local JSON data files if they don't exist."""
        files = {
            "clients.json": {"clients": [], "next_id": 1},
            "projects.json": {"projects": [], "next_id": 1},
            "tasks.json": {"tasks": [], "next_id": 1},
            "quotes.json": {"quotes": [], "next_num": 1},
            "pipeline.json": {"entries": []},
            "checklists.json": {},
            "catalog.json": {},
        }
        
        for filename, default_data in files.items():
            filepath = self.data_dir / filename
            if not filepath.exists():
                with open(filepath, "w", encoding="utf-8") as f:
                    json.dump(default_data, f, ensure_ascii=False, indent=2)
                self._log_step(f"Creado: data/{filename}", "success")
            else:
                self._log_step(f"Existe: data/{filename}", "info")
    
    def _create_industry_catalog(self):
        """Create service catalog based on industry."""
        catalog_file = self.data_dir / "catalog.json"
        industry = self.config.industria
        moneda = self.config.moneda
        
        catalogs = {
            "eventos": {
                "servicios": [
                    {"codigo": "EVT-BAS", "nombre": "Paquete Básico", "descripcion": "Decoración básica para evento", "precio_base": 50000, "unidad": "evento"},
                    {"codigo": "EVT-INT", "nombre": "Paquete Intermedio", "descripcion": "Decoración intermedia + mobiliario", "precio_base": 100000, "unidad": "evento"},
                    {"codigo": "EVT-PRE", "nombre": "Paquete Premium", "descripcion": "Decoración premium + mobiliario + iluminación", "precio_base": 180000, "unidad": "evento"},
                    {"codigo": "EVT-MES", "nombre": "Mesas de dulces", "descripcion": "Mesa de dulces personalizada", "precio_base": 8000, "unidad": "mesa"},
                    {"codigo": "EVT-FLO", "nombre": "Arreglo floral", "descripcion": "Centros de mesa y decoración floral", "precio_base": 5000, "unidad": "arreglo"},
                ],
                "multiplicadores": {"temporada_alta": 1.2, "temporada_baja": 0.9, "urgencia": 1.3}
            },
            "legal": {
                "servicios": [
                    {"codigo": "LEG-CON", "nombre": "Revisión de contrato", "descripcion": "Revisión y opinión legal de contrato", "precio_base": 15000, "unidad": "contrato"},
                    {"codigo": "LEG-DEM", "nombre": "Elaboración de demanda", "descripcion": "Demanda civil o mercantil", "precio_base": 35000, "unidad": "demanda"},
                    {"codigo": "LEG-ASE", "nombre": "Asesoría mensual", "descripcion": "Asesoría legal mensual preventiva", "precio_base": 12000, "unidad": "mes"},
                    {"codigo": "LEG-REP", "nombre": "Representación judicial", "descripcion": "Representación en juicio", "precio_base": 50000, "unidad": "juicio"},
                    {"codigo": "LEG-CONS", "nombre": "Consulta legal", "descripcion": "Consulta puntual", "precio_base": 3000, "unidad": "consulta"},
                ],
                "multiplicadores": {"complejidad_alta": 1.5, "complejidad_media": 1.2, "urgencia": 1.3}
            },
            "consultoria": {
                "servicios": [
                    {"codigo": "CON-DIA", "nombre": "Diagnóstico", "descripcion": "Diagnóstico inicial de negocio", "precio_base": 25000, "unidad": "diagnóstico"},
                    {"codigo": "CON-EST", "nombre": "Estrategia", "descripcion": "Plan estratégico", "precio_base": 50000, "unidad": "plan"},
                    {"codigo": "CON-IMP", "nombre": "Implementación", "descripcion": "Implementación de estrategia", "precio_base": 40000, "unidad": "mes"},
                    {"codigo": "CON-CAP", "nombre": "Capacitación", "descripcion": "Taller o capacitación", "precio_base": 15000, "unidad": "sesión"},
                ],
                "multiplicadores": {"empresa_grande": 1.5, "empresa_mediana": 1.2, "urgencia": 1.2}
            },
            "retail": {
                "servicios": [
                    {"codigo": "RTL-PRO", "nombre": "Producto A", "descripcion": "Descripción del producto", "precio_base": 500, "unidad": "pieza"},
                    {"codigo": "RTL-PRB", "nombre": "Producto B", "descripcion": "Descripción del producto", "precio_base": 800, "unidad": "pieza"},
                    {"codigo": "RTL-ENV", "nombre": "Envío", "descripcion": "Envío a domicilio", "precio_base": 150, "unidad": "envío"},
                ],
                "multiplicadores": {"mayoreo": 0.85, "menudeo": 1.0}
            },
        }
        
        default_catalog = catalogs.get(industry, catalogs["consultoria"])
        
        if not catalog_file.exists() or catalog_file.stat().st_size < 50:
            with open(catalog_file, "w", encoding="utf-8") as f:
                json.dump(default_catalog, f, ensure_ascii=False, indent=2)
            self._log_step(f"Catálogo de servicios creado para industria: {industry}", "success")
        else:
            self._log_step("Catálogo de servicios ya existe", "info")
    
    def _create_sample_data(self):
        """Create sample/demo data if database is empty."""
        clients_file = self.data_dir / "clients.json"
        projects_file = self.data_dir / "projects.json"
        
        with open(clients_file, "r", encoding="utf-8") as f:
            clients_data = json.load(f)
        
        if clients_data.get("clients"):
            self._log_step("Ya existen clientes, omitiendo datos de ejemplo", "info")
            return
        
        # Create sample client
        sample_client = {
            "id": "CLI-001",
            "nombre": "Cliente de Ejemplo",
            "email": "ejemplo@email.com",
            "telefono": "+52 55 0000 0000",
            "tipo_proyecto": "proyecto de ejemplo",
            "fuente": "onboarding",
            "estado": "prospecto",
            "notas": "Cliente creado automáticamente durante el onboarding",
            "fecha_registro": datetime.now().isoformat(),
            "ultima_actualizacion": datetime.now().isoformat(),
            "proyectos": ["PROJ-001"],
        }
        
        # Create sample project
        sample_project = {
            "id": "PROJ-001",
            "nombre": "Proyecto de Bienvenida",
            "cliente_id": "CLI-001",
            "cliente_nombre": "Cliente de Ejemplo",
            "descripcion": "Proyecto de ejemplo para familiarizarte con Hermes",
            "tipo": self.config.industria,
            "estado": "planificado",
            "monto": 0,
            "fecha_creacion": datetime.now().isoformat(),
            "fecha_inicio": datetime.now().isoformat(),
            "fecha_entrega": datetime.now().isoformat(),
            "fecha_completado": None,
            "progreso": 0,
            "tareas": [],
            "checklist": [],
            "notas": "",
            "historial": [{"accion": "Creación durante onboarding", "fecha": datetime.now().isoformat()}],
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
        
        self._log_step("Datos de ejemplo creados (cliente + proyecto)", "success")
    
    def _setup_google_workspace(self):
        """Setup Google Workspace if configured."""
        if not self.config.integracion_activa("google_workspace"):
            self._log_step("Google Workspace no está activo, omitiendo", "info")
            return
        
        try:
            from google_workspace import get_google_workspace
            gw = get_google_workspace()
            
            if not gw._init_credentials():
                self._log_step("No se pudieron cargar credenciales de Google", "warning")
                return
            
            # Create main folder
            empresa_nombre = self.config.nombre
            folder_name = f"Hermes OS — {empresa_nombre}"
            
            folder_id = gw.get_or_create_folder(folder_name)
            if folder_id:
                self._log_step(f"Carpeta de Drive creada: {folder_name}", "success")
                
                # Create subfolders
                subfolders = ["Clientes", "Proyectos", "Templates"]
                for sub in subfolders:
                    sub_id = gw.get_or_create_folder(sub, folder_id)
                    if sub_id:
                        self._log_step(f"  └─ {sub}/", "success")
            
            # Create master spreadsheet
            spreadsheet_id = gw.create_spreadsheet("Indice de Proyectos")
            if spreadsheet_id:
                self._log_step("Spreadsheet maestro creado: Indice de Proyectos", "success")
                
                # Setup headers
                gw.update_spreadsheet_values(
                    spreadsheet_id,
                    "Proyectos!A1:H1",
                    [["ID", "Nombre", "Cliente", "Tipo", "Estado", "Fecha", "Monto", "Link Drive"]]
                )
                gw.update_spreadsheet_values(
                    spreadsheet_id,
                    "Clientes!A1:G1",
                    [["ID", "Nombre", "Email", "Teléfono", "Fuente", "Estado", "Fecha registro"]]
                )
                gw.update_spreadsheet_values(
                    spreadsheet_id,
                    "Finanzas!A1:E1",
                    [["ID Proyecto", "Ingreso", "Gasto", "Margen", "Estado pago"]]
                )
                
                self._log_step("  └─ Headers de pestañas creados", "success")
        
        except Exception as e:
            self._log_step(f"Error configurando Google Workspace: {e}", "error")
            self.results["errors"].append(str(e))
    
    def _generate_welcome_documents(self):
        """Generate welcome/guide documents."""
        docs_dir = self.project_root / "docs"
        welcome_file = docs_dir / "WELCOME.md"
        
        empresa = self.config.nombre
        industria = self.config.industria
        
        welcome_content = f"""# 🎉 Bienvenido a Hermes Business OS

## {empresa}

Hermes Business OS está ahora configurado para tu empresa.

### ¿Qué puedes hacer ahora?

1. **Habla con Hermes por Telegram**
   - Envía: "Registra un cliente nuevo"
   - Envía: "Cotiza un servicio"
   - Envía: "¿Qué tenemos pendiente?"

2. **Usa el Dashboard Web**
   ```bash
   cd dashboard
   npm install
   npm run dev
   ```
   Abre http://localhost:3000

3. **Gestiona tu negocio**
   - Clientes y prospectos
   - Cotizaciones y pipeline
   - Proyectos y tareas
   - Documentos automáticos

### Primeros comandos útiles

| Comando | Descripción |
|---------|-------------|
| `/empresa` | Ver configuración |
| `/clientes` | Listar clientes |
| `/proyectos` | Listar proyectos |
| `/estado` | Resumen del negocio |

### Industria: {industria}

Hermes viene preconfigurado con:
- Catálogo de servicios para {industria}
- Templates de documentos
- Checklists por fase

---

*Documento generado automáticamente por Hermes Business OS Onboarding*
"""
        
        with open(welcome_file, "w", encoding="utf-8") as f:
            f.write(welcome_content)
        
        self._log_step(f"Guía de bienvenida creada: docs/WELCOME.md", "success")
    
    def get_onboarding_status(self) -> Dict[str, Any]:
        """Get current onboarding status."""
        status = {
            "config_exists": self.config.config_path.exists(),
            "company_name": self.config.nombre,
            "industry": self.config.industria,
            "data_dir_exists": self.data_dir.exists(),
            "google_workspace_active": self.config.integracion_activa("google_workspace"),
            "departments_active": [],
        }
        
        for dept in ["ventas", "operaciones", "documentos", "finanzas", "rrhh"]:
            if self.config.departamento_activo(dept):
                status["departments_active"].append(dept)
        
        return status


# Singleton
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
        print("✅ Onboarding completado exitosamente")
    else:
        print("⚠️  Onboarding completado con advertencias")
    
    if result["errors"]:
        print("\nErrores:")
        for err in result["errors"]:
            print(f"  - {err}")

---
name: finance
description: Skill de finanzas para el perfil Tesorero de Partenon. Clasifica costos fijos y variables, construye dashboards, analiza gastos y detecta inconsistencias en Google Sheets.
version: 0.1.0
metadata:
  partenon:
    profile: partenon-tesorero
    tags: [finanzas, google-sheets, presupuestos, proveedores, costos, dashboards]
    related_skills: [business-core, marketing, operations]
    depends_on: [google_workspace]
    status: draft
---

# Skill: Finance — Partenon Tesorero v0.1

## Rol

Soy la skill de finanzas del Tesorero. Mantengo los numeros de Hermes ordenados, visibles y auditables en Google Sheets.

## Activacion

Me activo cuando:
- Se recibe un gasto o ingreso para registrar.
- Se necesita clasificar un costo como fijo o variable.
- Se pide un presupuesto de proyecto o campana.
- Hay que construir o actualizar un dashboard.
- Se detecta una inconsistencia o duplicidad.
- Se acerca una fecha de vencimiento.

## Herramientas Python

### `tools/google_sheets.py`
- `GoogleSheets.read_sheet(spreadsheet_id, range_name)` — Lee un rango de Sheets.
- `GoogleSheets.write_sheet(spreadsheet_id, range_name, values)` — Escribe un rango en Sheets.
- `GoogleSheets.append_row(spreadsheet_id, range_name, row)` — Agrega una fila al final.
- `GoogleSheets.create_dashboard(title, sheets)` — Crea spreadsheet maestro con hojas base.
- `GoogleSheets.get_or_create_spreadsheet(title)` — Busca o crea spreadsheet por titulo.

### `tools/parsers.py`
- `ExpenseParser.parse_excel(filepath)` — Extrae gastos de un archivo Excel o CSV.
- `ExpenseParser.parse_csv(filepath)` — Extrae gastos de CSV.
- `ExpenseParser.normalize_amount(value)` — Normaliza montos a numero.
- `ExpenseParser.infer_category(description)` — Sugiere categoria a partir de descripcion.

### `tools/templates.py`
- `Templates.crear_presupuesto(filepath, periodo, rubros)` — Genera plantilla de presupuesto.
- `Templates.crear_proveedores(filepath)` — Genera directorio de proveedores.
- `Templates.crear_flujo_caja(filepath, meses)` — Genera plantilla de flujo de caja.

## Funciones principales

### 1. Clasificar costos fijos y variables

Cada gasto se etiqueta en el momento del registro:
- Fijo: renta, salarios base, servicios recurrentes.
- Variable: materiales, publicidad, flete, comisiones.
- Ambiguo: se deja en revision y se pregunta al usuario.

### 2. Construir dashboard

El dashboard maestro incluye estas hojas:
- Resumen Mensual
- Flujo de Caja
- Costos Fijos
- Costos Variables
- Proveedores
- Presupuestos vs Real
- Alertas

### 3. Analizar gastos

- Comparar gastos reales contra presupuesto.
- Calcular variacion porcentual.
- Identificar top proveedores por monto.
- Agrupar gastos por categoria y periodo.

### 4. Detectar inconsistencias

- Duplicidades de transacciones.
- Montos negativos o nulos.
- Categorias vacias o desconocidas.
- Vencimientos proximos sin pago registrado.
- Variaciones de precio mayores al umbral configurado.

## Flujo: Registrar un gasto

1. Recibir descripcion, monto, fecha y metodo.
2. Normalizar monto y fecha.
3. Inferir categoria.
4. Clasificar como fijo o variable.
5. Si es ambiguo, preguntar al usuario.
6. Escribir fila en la hoja correspondiente de Sheets.
7. Actualizar dashboard si aplica.

## Flujo: Presupuesto de campana

1. Recibir parametros de la campana del Mensajero.
2. Calcular costos variables esperados.
3. Verificar disponibilidad contra presupuesto de marketing.
4. Crear o actualizar presupuesto en Sheets.
5. Compartir enlace con el Mensajero.

## Reglas

- Siempre escribir en Google Sheets.
- Preguntar antes de categorizar ambiguo.
- No modificar transacciones pasadas; crear reversos.
- Mantener moneda y redondeo consistentes.
- Alertar vencimientos 3 dias antes.
- Conectar con Mensajero para presupuestos de campanas.

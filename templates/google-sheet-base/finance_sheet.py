"""
Generates a Partenon finance master spreadsheet template.
Can be used locally with openpyxl or uploaded to Google Sheets.
"""

from datetime import datetime
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter


ACCENT = "00D4FF"
BG = "050505"
TEXT = "E8E8ED"
MUTED = "6B6B78"


def style_header(cell):
    cell.font = Font(name="Space Grotesk", size=11, bold=True, color=BG)
    cell.fill = PatternFill(start_color=ACCENT, end_color=ACCENT, fill_type="solid")
    cell.alignment = Alignment(horizontal="left", vertical="center")


def style_cell(cell, bold=False):
    cell.font = Font(name="Geist", size=10, color=TEXT, bold=bold)
    cell.alignment = Alignment(horizontal="left", vertical="center")


def auto_width(ws):
    for col in ws.columns:
        max_length = 0
        col_letter = get_column_letter(col[0].column)
        for cell in col:
            try:
                if cell.value:
                    max_length = max(max_length, len(str(cell.value)))
            except Exception:
                pass
        ws.column_dimensions[col_letter].width = min(max_length + 4, 50)


def create_finance_sheet(output_path: Path):
    wb = Workbook()

    # Dashboard
    ws = wb.active
    ws.title = "Dashboard"
    headers = ["Indicator", "Value", "Note"]
    ws.append(headers)
    for cell in ws[1]:
        style_header(cell)

    rows = [
        ["Current month income", "=SUM(Income!C:C)", "Sum of Income sheet"],
        ["Monthly fixed expenses", "=SUM('Fixed Expenses'!C:C)", "Recurring costs"],
        ["Monthly variable expenses", "=SUM('Variable Expenses'!C:C)", "Proportional costs"],
        ["Estimated margin", "=B2-B3-B4", "Income - expenses"],
        ["Active suppliers", "=COUNTA(Suppliers!A:A)-1", ""],
    ]
    for row in rows:
        ws.append(row)
        for cell in ws[ws.max_row]:
            style_cell(cell)

    # Income
    ws = wb.create_sheet("Income")
    ws.append(["Date", "Concept", "Amount", "Client", "Channel"])
    for cell in ws[1]:
        style_header(cell)

    # Fixed Expenses
    ws = wb.create_sheet("Fixed Expenses")
    ws.append(["Date", "Concept", "Amount", "Frequency", "Supplier"])
    for cell in ws[1]:
        style_header(cell)

    # Variable Expenses
    ws = wb.create_sheet("Variable Expenses")
    ws.append(["Date", "Concept", "Amount", "Category", "Supplier"])
    for cell in ws[1]:
        style_header(cell)

    # Suppliers
    ws = wb.create_sheet("Suppliers")
    ws.append(["Name", "Service", "Contact", "Usual payment", "Rating"])
    for cell in ws[1]:
        style_header(cell)

    for sheet in wb.worksheets:
        auto_width(sheet)

    wb.save(output_path)
    return output_path


if __name__ == "__main__":
    output = Path(__file__).resolve().parents[2] / "data" / "partenon-finance-template.xlsx"
    output.parent.mkdir(parents=True, exist_ok=True)
    create_finance_sheet(output)
    print(f"Created {output}")

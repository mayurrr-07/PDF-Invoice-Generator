# 🧾 PDF Invoice Generator v2 (Python + ReportLab)

A command-line PDF Invoice Generator built with Python and the ReportLab library. Easily create professional invoices with itemized billing, tax calculations, and export to PDF format — all from your terminal.

---

## 📦 Features

- Interactive CLI to input:
  - Company details
  - Customer information
  - Line items (products/services)
- Support for item-wise tax rate (default: 18%)
- Automatic calculation of:
  - Subtotal
  - Tax (multiple rates supported)
  - Grand Total
- Generates a clean and styled **PDF invoice**
- Auto-generates invoice numbers with date (`INV-YYYYMMDD-001` format)
- Organized output directory (`./invoices/`)

---

## 🛠 Requirements

- Python 3.6+
- ReportLab

### Install Dependencies

```bash
pip install reportlab

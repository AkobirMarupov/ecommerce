# app/utils/pdf.py

from fpdf import FPDF
from pathlib import Path
from datetime import datetime

class InvoicePDF(FPDF):
    def header(self):
        # Logotip (bor bo‘lsa)
        # self.image("static/logo.png", 10, 8, 33)  # optional

        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "INVOICE", ln=True, align="C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 10)
        self.cell(0, 10, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", align="C")


def generate_invoice_pdf(order_id: int, user_email: str, items: list[dict], total_amount: float) -> str:
    pdf = InvoicePDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Mijoz va sana ma’lumotlari
    pdf.cell(100, 10, f"Order ID: {order_id}", ln=True)
    pdf.cell(100, 10, f"Customer Email: {user_email}", ln=True)
    pdf.cell(100, 10, f"Date: {datetime.now().strftime('%d-%m-%Y')}", ln=True)
    pdf.ln(5)

    # Jadval sarlavhalari
    pdf.set_fill_color(220, 220, 220)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(60, 10, "Product", border=1, fill=True)
    pdf.cell(30, 10, "Quantity", border=1, fill=True)
    pdf.cell(40, 10, "Price", border=1, fill=True)
    pdf.cell(40, 10, "Subtotal", border=1, fill=True)
    pdf.ln()

    # Mahsulotlar ro'yxati
    pdf.set_font("Arial", size=11)
    for item in items:
        subtotal = item["quantity"] * item["price"]
        pdf.cell(60, 10, item["name"], border=1)
        pdf.cell(30, 10, str(item["quantity"]), border=1)
        pdf.cell(40, 10, f"${item['price']:.2f}", border=1)
        pdf.cell(40, 10, f"${subtotal:.2f}", border=1)
        pdf.ln()

    pdf.set_font("Arial", "B", 12)
    pdf.cell(130, 10, "Total", border=0)
    pdf.cell(40, 10, f"${total_amount:.2f}", border=1)
    pdf.ln(10)

    # Saqlash
    file_path = Path(f"static/invoices/invoice_{order_id}.pdf")
    file_path.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(file_path))

    return str(file_path)

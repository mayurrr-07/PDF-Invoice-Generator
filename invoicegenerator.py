from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from datetime import datetime
import os
import json

class InvoiceGeneratorV2:
    def __init__(self, company_info):
        self.company_info = company_info
        self.items = []
        self.styles = getSampleStyleSheet()
        
    def add_item(self, description, quantity, price, tax_rate=0.18):
        """Add an item to the invoice."""
        self.items.append({
            'description': description,
            'quantity': quantity,
            'price': price,
            'tax_rate': tax_rate,
            'total': quantity * price * (1 + tax_rate)
        })
        return self
    
    def calculate_totals(self):
        """Calculate invoice totals."""
        subtotal = sum(item['quantity'] * item['price'] for item in self.items)
        tax_details = {}
        
        for item in self.items:
            rate = item['tax_rate']
            if rate not in tax_details:
                tax_details[rate] = 0
            tax_details[rate] += item['quantity'] * item['price'] * rate
            
        total_tax = sum(tax_details.values())
        grand_total = subtotal + total_tax
        
        return {
            'subtotal': subtotal,
            'tax_details': tax_details,
            'total_tax': total_tax,
            'grand_total': grand_total
        }
    
    def generate_invoice(self, customer_info, invoice_number, output_dir='.'):
        """Generate the invoice PDF."""
        # Calculate totals
        totals = self.calculate_totals()
        
        # Create PDF
        filename = os.path.join(output_dir, f'invoice_{invoice_number}.pdf')
        doc = SimpleDocTemplate(filename, pagesize=letter)
        
        # Create custom styles
        styles = self.styles
        styles.add(ParagraphStyle(
            name='InvoiceTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=20,
            alignment=1  # Center
        ))
        
        # Build story
        story = []
        
        # Add company info
        story.append(Paragraph(self.company_info['name'], styles['InvoiceTitle']))
        story.append(Paragraph(self.company_info['address'], styles['Normal']))
        story.append(Paragraph(f"Phone: {self.company_info['phone']}", styles['Normal']))
        story.append(Paragraph(f"Email: {self.company_info['email']}", styles['Normal']))
        story.append(Spacer(1, 30))
        
        # Add invoice info
        story.append(Paragraph("INVOICE", styles['Heading1']))
        story.append(Paragraph(f"<b>Invoice #:</b> {invoice_number}", styles['Normal']))
        story.append(Paragraph(f"<b>Date:</b> {datetime.now().strftime('%Y-%m-%d')}", styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Add customer info
        story.append(Paragraph("<b>Bill To:</b>", styles['Heading3']))
        story.append(Paragraph(customer_info['name'], styles['Normal']))
        story.append(Paragraph(customer_info['address'], styles['Normal']))
        story.append(Spacer(1, 30))
        
        # Create items table
        data = [["Description", "Qty", "Price", "Tax %", "Total"]]
        for item in self.items:
            data.append([
                item['description'],
                str(item['quantity']),
                f"₹{item['price']:.2f}",
                f"{int(item['tax_rate']*100)}%",
                f"₹{item['total']:.2f}"
            ])
        
        # Add totals row
        data.append(["", "", "", "Subtotal:", f"₹{totals['subtotal']:.2f}"])
        
        # Add tax rows
        for rate, tax in totals['tax_details'].items():
            data.append(["", "", "", f"Tax ({int(rate*100)}%):", f"₹{tax:.2f}"])
            
        # Add grand total
        data.append(["", "", "", "<b>Total:</b>", f"<b>₹{totals['grand_total']:.2f}</b>"])
        
        # Create and style table
        table = Table(data, colWidths=[250, 50, 80, 70, 80])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#40466e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f5f5f5')),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('PADDING', (0, 0), (-1, -1), 6),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),  # Left align description
            ('ALIGN', (-2, -len(totals['tax_details'])-2), (-1, -1), 'RIGHT'),  # Right align totals
            ('FONTNAME', (-2, -1), (-1, -1), 'Helvetica-Bold'),  # Bold grand total
        ]))
        
        story.append(table)
        story.append(Spacer(1, 40))
        
        # Add thank you note
        story.append(Paragraph("Thank you for your business!", styles['Italic']))
        
        # Build PDF
        doc.build(story)
        return filename

def get_company_info():
    """Get company information from user input."""
    print("\n=== Company Information ===")
    return {
        'name': input("Company Name: "),
        'address': input("Address: "),
        'phone': input("Phone: "),
        'email': input("Email: ")
    }

def get_customer_info():
    """Get customer information from user input."""
    print("\n=== Customer Information ===")
    return {
        'name': input("Customer Name: "),
        'address': input("Address: ")
    }

def add_items_to_invoice(invoice):
    """Add items to the invoice interactively."""
    print("\n=== Add Items (enter 'done' when finished) ===")
    
    while True:
        description = input("\nItem description (or 'done'): ").strip()
        if description.lower() == 'done':
            if not invoice.items:
                print("Please add at least one item.")
                continue
            break
            
        while True:
            try:
                quantity = float(input("Quantity: "))
                if quantity <= 0:
                    print("Quantity must be greater than 0")
                    continue
                break
            except ValueError:
                print("Please enter a valid number")
                
        while True:
            try:
                price = float(input("Price per unit (₹): "))
                if price < 0:
                    print("Price cannot be negative")
                    continue
                break
            except ValueError:
                print("Please enter a valid number")
                
        while True:
            try:
                tax_rate = input("Tax rate (% - press Enter for 18%): ") or "18"
                tax_rate = float(tax_rate) / 100
                if tax_rate < 0 or tax_rate > 1:
                    print("Tax rate must be between 0% and 100%")
                    continue
                break
            except ValueError:
                print("Please enter a valid number")
        
        invoice.add_item(description, quantity, price, tax_rate)
        print(f"✓ Added: {quantity} x {description} @ ₹{price:.2f} ({int(tax_rate*100)}% tax)")

if __name__ == "__main__":
    print("=== Invoice Generator v2 ===")
    
    # Create output directory if it doesn't exist
    output_dir = "invoices"
    os.makedirs(output_dir, exist_ok=True)
    
    # Get company info
    company = get_company_info()
    
    # Create invoice generator
    invoice = InvoiceGeneratorV2(company)
    
    # Add items
    add_items_to_invoice(invoice)
    
    # Get customer info
    customer = get_customer_info()
    
    # Generate invoice number (YYYYMMDD-XXX format)
    invoice_number = f"INV-{datetime.now().strftime('%Y%m%d')}-001"
    
    # Generate the invoice
    print("\nGenerating invoice...")
    try:
        filename = invoice.generate_invoice(customer, invoice_number, output_dir)
        print(f"\n✅ Invoice generated successfully: {os.path.abspath(filename)}")
    except Exception as e:
        print(f"\n❌ Error generating invoice: {str(e)}")

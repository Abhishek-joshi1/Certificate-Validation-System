from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from datetime import datetime  # ✅ Import datetime
import pdfplumber
import hashlib

def generate_certificate(output_path, uid, candidate_name, course_name, org_name, institute_logo_path):
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    elements = []

    # ✅ Function to draw border
    def draw_border(canvas, doc):
        canvas.setStrokeColor(colors.black)
        canvas.setLineWidth(3)
        margin = 20
        canvas.rect(margin, margin, letter[0] - 2 * margin, letter[1] - 2 * margin)

    # ✅ Get today's date in a readable format
    today_date = datetime.today().strftime("%B %d, %Y")

    # Add institute logo
    if institute_logo_path:
        logo = Image(institute_logo_path, width=100, height=100)
        elements.append(logo)

    # Add institute name
    institute_style = ParagraphStyle(
        "InstituteStyle",
        parent=getSampleStyleSheet()["Title"],
        fontName="Helvetica-Bold",
        fontSize=20,
        spaceAfter=30,
        alignment=1
    )
    institute = Paragraph(org_name, institute_style)
    elements.append(institute)

    # Add title
    title_style = ParagraphStyle(
        "TitleStyle",
        parent=getSampleStyleSheet()["Title"],
        fontName="Helvetica-Bold",
        fontSize=28,
        textColor=colors.darkblue,
        spaceAfter=20,
        alignment=1
    )
    title = Paragraph("Certificate of Completion", title_style)
    elements.append(title)

    # Add recipient details
    recipient_style = ParagraphStyle(
        "RecipientStyle",
        parent=getSampleStyleSheet()["BodyText"],
        fontSize=16,
        leading=22,
        alignment=1
    )

    recipient_text = f"""<br/><br/>
    This is to certify that <br/>
    <font color='red' size=16><b>{candidate_name}</b></font> <br/><br/>
    with UID <br/>
    <font color='red' size=14><b>{uid}</b></font> <br/><br/>
    has successfully completed the course:<br/>
    <font color='blue' size=16><b>{course_name}</b></font>
    """
    recipient = Paragraph(recipient_text, recipient_style)
    elements.append(recipient)

    elements.append(Spacer(1, 20))

    # ✅ Add today's date
    date_style = ParagraphStyle(
        "DateStyle",
        parent=getSampleStyleSheet()["BodyText"],
        fontSize=14,
        spaceAfter=20,
        alignment=1
    )
    date_paragraph = Paragraph(f"Date of Issue: <b>{today_date}</b>", date_style)
    elements.append(date_paragraph)

    # Add signature & date placeholders
    signature_table = Table(
        [["__________________", "", "__________________"],
         ["Authorized Signatory", "", "Date"]],
        colWidths=[3 * inch, 1 * inch, 3 * inch]
    )
    signature_table.setStyle(
        TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12)
        ])
    )
    elements.append(signature_table)

    # Build PDF with border
    doc.build(elements, onFirstPage=draw_border)

    print(f"Certificate generated and saved at: {output_path}")


def extract_certificate(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n"

    # Debugging: Print extracted text
    print("Extracted Certificate Text:\n", text)

    # Extract details assuming text order (adjust if needed)
    lines = text.splitlines()
    
    try:
        org_name = lines[0].strip()
        candidate_name = lines[3].strip()
        uid = lines[5].strip()
        course_name = lines[-1].strip()
        
        print("Extracted Data:")
        print(f"UID: {uid}, Candidate: {candidate_name}, Course: {course_name}, Org: {org_name}")


        return (uid, candidate_name, course_name, org_name)

    except IndexError:
        print("Error: Could not extract certificate details properly.")
        return None
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from datetime import datetime
import json

def export_chat_to_pdf(conversation_history, filename=None):
    """Export conversation to PDF"""
    
    if not filename:
        filename = f"chat_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    
    # Create PDF document
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#667eea'),
        alignment=1  # Center alignment
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#764ba2')
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        leading=14
    )
    
    # Build PDF content
    story = []
    
    # Title
    story.append(Paragraph("College Chatbot Conversation Report", title_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Metadata
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}", normal_style))
    story.append(Paragraph(f"Total Messages: {len(conversation_history)}", normal_style))
    story.append(Spacer(1, 0.3*inch))
    
    # Conversation
    story.append(Paragraph("Conversation Log", heading_style))
    story.append(Spacer(1, 0.1*inch))
    
    for i, (user_msg, bot_msg) in enumerate(conversation_history, 1):
        story.append(Paragraph(f"<b>{i}. User:</b> {user_msg}", normal_style))
        story.append(Spacer(1, 0.05*inch))
        story.append(Paragraph(f"<b>Bot:</b> {bot_msg}", normal_style))
        story.append(Spacer(1, 0.1*inch))
    
    # Build PDF
    doc.build(story)
    return filename

# Example usage
if __name__ == "__main__":
    # Sample conversation
    sample_chat = [
        ("What courses are offered?", "We offer B.Tech, MBA, BCA, MCA, BSc, and PhD programs."),
        ("How much are the fees?", "Engineering: Rs 1.5L/year, MBA: Rs 2L/year"),
        ("Tell me about placements", "95% placement rate. Average package: Rs 8.5 LPA")
    ]
    
    filename = export_chat_to_pdf(sample_chat)
    print(f"✅ PDF exported: {filename}")
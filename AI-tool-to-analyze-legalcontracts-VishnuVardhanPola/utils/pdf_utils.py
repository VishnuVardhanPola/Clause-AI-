from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


def generate_pdf(report_text, output_path):
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(output_path)

    elements = []

    for line in report_text.split("\n"):
        elements.append(Paragraph(line, styles["Normal"]))
        elements.append(Spacer(1, 12))

    doc.build(elements)
    return output_path

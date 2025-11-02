
from weasyprint import HTML
from flask import current_app
import tempfile, os

def render_pdf(html_content: str) -> bytes:
    with tempfile.TemporaryDirectory() as td:
        pdf = HTML(string=html_content, base_url=os.getcwd()).write_pdf()
        return pdf

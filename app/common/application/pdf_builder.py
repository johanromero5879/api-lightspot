from io import BytesIO
from functools import partial

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Table, BaseDocTemplate, Paragraph, Spacer, Frame, PageTemplate
from reportlab.lib.units import cm

styles = getSampleStyleSheet()


class Colors:
    PRIMARY_ALT = colors.HexColor(0x1559cf)
    LIGHT = colors.HexColor(0xffffff)
    LIGHT_ALT = colors.HexColor(0xf6f6f6)
    GREY = colors.HexColor(0x8297b5)


class PDFBuilder:
    def __init__(self):
        self.header = None
        self.footer = None
        self.elements = []

    def set_header(self, header_text: str):
        self.header = Paragraph(header_text, styles["Normal"])
        return self

    def set_footer(self, footer_text: str):
        self.footer = Paragraph(footer_text, styles["Normal"])
        return self

    def set_title(self, title: str):

        report_title = Paragraph(title, styles["Title"])
        report_title.alignment = "CENTER"

        self.elements.insert(0, report_title)
        self.elements.insert(1, self.add_space())
        return self

    def add_content(self, content: str):
        report_content = Paragraph(content)
        self.elements.extend([report_content, self.add_space(0.5)])
        return self

    def add_content_by_columns(self, content: list, col_width: int):
        table_data = []
        for item in content:
            row = [Paragraph(column, styles["Normal"]) for column in item if column is not None]
            table_data.append(row)

        report_content = Table(table_data, colWidths=col_width)

        self.elements.extend([report_content, self.add_space(0.5)])

        return self

    def add_table(self, data):
        table_style = [
            ('BACKGROUND', (0, 0), (-1, 0), Colors.PRIMARY_ALT),
            ('TEXTCOLOR', (0, 0), (-1, 0), Colors.LIGHT),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), Colors.LIGHT_ALT),
            ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
            ('FONTSIZE', (0, 1), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, Colors.GREY)
        ]

        self.elements.extend([Table(data, style=table_style), self.add_space()])
        return self

    def add_space(self, factor: float = 0.25):
        return Spacer(1, factor * cm)

    def build(self):
        if len(self.elements) == 0:
            raise NoContentReportError()

        buffer = BytesIO()
        doc = BaseDocTemplate(
            buffer,
            pagesize=letter
        )

        # Build the PDF
        self.__build_templates(doc)
        doc.build(self.elements)

        # Get the PDF data from the buffers
        pdf_data = buffer.getvalue()

        # Return the PDF data as bytes
        return pdf_data

    def __build_templates(self, doc):
        def header(canvas, doc, content):
            if content:
                canvas.saveState()
                w, h = content.wrap(doc.width, doc.topMargin)
                content.drawOn(canvas, 375, 750)

                canvas.drawImage("assets/images/long_logo.jpg", cm, 737, 6*cm, 1.25 * cm)
                canvas.restoreState()

        def footer(canvas, doc, content):
            canvas.saveState()
            if content:
                w, h = content.wrap(doc.width, doc.bottomMargin)
                content.drawOn(canvas, doc.width / 2, cm * 0.5)

            # Add page number
            page_num = canvas.getPageNumber()
            page_text = Paragraph(f"Pág. {page_num}", styles["Normal"])
            page_text.wrap(doc.width, doc.bottomMargin)
            page_text.drawOn(canvas, 550, cm * 0.5)

            canvas.restoreState()

        def header_and_footer(canvas, doc, header_content, footer_content):
            header(canvas, doc, header_content)
            footer(canvas, doc, footer_content)

        frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height)

        template = PageTemplate(
            frames=[frame],
            onPage=partial(header_and_footer, header_content=self.header, footer_content=self.footer))

        doc.addPageTemplates([template])


class NoContentReportError(Exception):
    def __init__(self):
        message = "No content in the report"
        super().__init__(message)

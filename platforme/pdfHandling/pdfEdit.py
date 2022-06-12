from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def printOnPDF(name, CIN, bidthDay, placeOfBirth, formationPlace, start, end, faitLe, faitLoDate, sertNum, pdfName, dirName, fourmateur):
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFont('Helvetica', 16)
    can.drawString(119.5, 332.9, name)
    can.drawString(430.2, 332.9, bidthDay)
    can.drawString(540, 332.9, placeOfBirth)
    can.drawString(680, 332.9, CIN)
    can.drawString(248, 254.9, formationPlace)
    can.drawString(429, 254.9, start)
    can.drawString(560, 254.9, end)
    can.drawString(325.2, 210.5, faitLe)
    can.drawString(555, 210.5, faitLoDate)
    can.drawString(269.5, 75.7, sertNum)
    can.save()

    #move to the beginning of the StringIO buffer
    packet.seek(0)

    # create a new PDF with Reportlab
    new_pdf = PdfFileReader(packet)
    # read your existing PDF
    existing_pdf = PdfFileReader(open("platforme/pdfHandling/attestation.pdf", "rb"))
    output = PdfFileWriter()
    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)
    # finally, write "output" to a real file
    outputStream = open(f"./media/{dirName}/{pdfName}.pdf", "wb")
    output.write(outputStream)
    outputStream.close()

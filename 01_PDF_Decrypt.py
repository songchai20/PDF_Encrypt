from pypdf import PdfReader, PdfWriter

reader = PdfReader("Cx_ScanReport_BDMS_CPROM_Lung-Questionnaire.pdf")

if reader.is_encrypted:
    reader.decrypt("Cx_ScanReport_BDMS_CPROM_Lung-Questionnaire_2.pdf")

writer = PdfWriter(clone_from=reader)

# Save the new PDF to a file
with open("decrypted-pdf.pdf", "wb") as f:
    writer.write(f)
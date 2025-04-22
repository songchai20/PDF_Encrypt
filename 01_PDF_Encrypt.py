from pypdf import PdfReader, PdfWriter

reader = PdfReader("D:/Python/PDF_Encrypt/test.pdf")
writer = PdfWriter(clone_from=reader)

# Add a password to the new PDF
writer.encrypt("bdMs@P3ntEsT@2025", algorithm="AES-256")

# Save the new PDF to a file
with open("test_Encrypt.pdf", "wb") as f:
    writer.write(f)
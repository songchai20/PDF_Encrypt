from pypdf import PdfReader, PdfWriter
from getpass import getpass

pdf_path = input("Enter the path of the PDF file: ")
output_path = input("Enter the output filename: ")
password = input("Enter the password to encrypt the PDF: ")

#Hide type password
#password = getpass("Enter the password to encrypt the PDF: ")

reader = PdfReader(pdf_path)
writer = PdfWriter(clone_from=reader)

writer.encrypt(password, algorithm="AES-256")

with open(output_path, "wb") as f:
    writer.write(f)

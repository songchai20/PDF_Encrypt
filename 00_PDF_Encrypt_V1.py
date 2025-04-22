from pypdf import PdfReader, PdfWriter

def encrypt_pdf(input_pdf, output_pdf, password):
    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    # คัดลอกทุกหน้าไปยัง PDF ใหม่
    for page in reader.pages:
        writer.add_page(page)

    # ตั้งรหัสผ่าน
    writer.encrypt(password)

    # บันทึกไฟล์ที่เข้ารหัส
    with open(output_pdf, "wb") as f:
        writer.write(f)

    print(f"ไฟล์ {output_pdf} ถูกเข้ารหัสเรียบร้อยแล้ว!")

# ตัวอย่างการใช้งาน
input_pdf = "document.pdf"    # ไฟล์ PDF ต้นฉบับ
output_pdf = "document_encrypted.pdf"  # ไฟล์ PDF ที่เข้ารหัส
password = "your_secure_password"  # ตั้งรหัสผ่าน

encrypt_pdf(input_pdf, output_pdf, password)

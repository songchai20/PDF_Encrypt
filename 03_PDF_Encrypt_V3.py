from pypdf import PdfReader, PdfWriter
from dotenv import load_dotenv
import os

# โหลดตัวแปรจาก .env
load_dotenv()

pdf_path = os.getenv("PDF_PATH")
output_file = os.getenv("OUTPUT_FILE")
password = os.getenv("PDF_PASSWORD")

# ตรวจสอบว่าโหลดค่ามาครบหรือไม่
if not all([pdf_path, output_file, password]):
    raise ValueError("Missing one or more required environment variables.")

reader = PdfReader(pdf_path)
writer = PdfWriter(clone_from=reader)

writer.encrypt(password, algorithm="AES-256")

with open(output_file, "wb") as f:
    writer.write(f)

print(f"✅ PDF ถูกเข้ารหัสและบันทึกไว้ที่: {output_file}")

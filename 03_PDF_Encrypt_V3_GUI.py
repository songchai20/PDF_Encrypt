import os
import logging
from tkinter import Tk, Label, Entry, Button, filedialog, StringVar
from tkinter.messagebox import showinfo
from getpass import getuser
from dotenv import load_dotenv
from pypdf import PdfReader, PdfWriter

# โหลด environment variables
load_dotenv()

# ตั้งค่า logging
logging.basicConfig(
    filename="audit.log",
    level=logging.INFO,
    format="%(asctime)s - USER:%(user)s - ACTION:%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

class UserFilter(logging.Filter):
    def filter(self, record):
        record.user = getuser()
        return True

logging.getLogger().addFilter(UserFilter())

# ฟังก์ชันเข้ารหัส PDF
def encrypt_pdf():
    input_path = pdf_path.get()
    output_path = output_filename.get()
    pwd = password.get()

    if not all([input_path, output_path, pwd]):
        showinfo("Error", "Please fill in all fields.")
        return

    try:
        reader = PdfReader(input_path)
        writer = PdfWriter(clone_from=reader)
        writer.encrypt(pwd, algorithm="AES-256")
        with open(output_path, "wb") as f:
            writer.write(f)

        logging.info(f"Encrypted '{input_path}' to '{output_path}'")
        showinfo("Success", f"PDF encrypted and saved as:\n{output_path}")
    except Exception as e:
        showinfo("Error", f"Failed to encrypt PDF: {e}")
        logging.error(f"Failed to encrypt: {e}")

# GUI เริ่มที่นี่
app = Tk()
app.title("PDF Encryptor")
app.geometry("400x250")

# โหลดค่าจาก .env
pdf_path = StringVar(value=os.getenv("PDF_PATH", ""))
output_filename = StringVar(value=os.getenv("OUTPUT_FILE", "test_Encrypt.pdf"))
password = StringVar(value=os.getenv("PDF_PASSWORD", ""))

def browse_pdf():
    filename = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if filename:
        pdf_path.set(filename)

# GUI Layout
Label(app, text="Select PDF File:").pack(pady=5)
Entry(app, textvariable=pdf_path, width=50).pack()
Button(app, text="Browse", command=browse_pdf).pack()

Label(app, text="Output Filename:").pack(pady=5)
Entry(app, textvariable=output_filename, width=50).pack()

Label(app, text="Password:").pack(pady=5)
Entry(app, textvariable=password, show="*", width=50).pack()

Button(app, text="Encrypt PDF", command=encrypt_pdf).pack(pady=20)

app.mainloop()

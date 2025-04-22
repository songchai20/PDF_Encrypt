import os
import csv
import json
import logging
from tkinter import Tk, Label, Entry, Button, filedialog, StringVar
from tkinter.messagebox import showinfo
from tkinterdnd2 import DND_FILES, TkinterDnD
from datetime import datetime
from dotenv import load_dotenv
from pypdf import PdfReader, PdfWriter
from getpass import getuser

# --- โหลด .env ---
load_dotenv()

# --- Logging CSV/JSON ---
LOG_CSV = "audit_log.csv"
LOG_JSON = "audit_log.json"

def log_action(file_in, file_out, status, error=""):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "user": getuser(),
        "input_file": file_in,
        "output_file": file_out,
        "status": status,
        "error": error,
    }

    # Append to JSON
    if os.path.exists(LOG_JSON):
        with open(LOG_JSON, "r+", encoding="utf-8") as jf:
            try:
                data = json.load(jf)
            except json.JSONDecodeError:
                data = []
            data.append(log_entry)
            jf.seek(0)
            json.dump(data, jf, indent=4)
    else:
        with open(LOG_JSON, "w", encoding="utf-8") as jf:
            json.dump([log_entry], jf, indent=4)

    # Append to CSV
    write_header = not os.path.exists(LOG_CSV)
    with open(LOG_CSV, "a", newline='', encoding="utf-8") as cf:
        writer = csv.DictWriter(cf, fieldnames=log_entry.keys())
        if write_header:
            writer.writeheader()
        writer.writerow(log_entry)

# --- ฟังก์ชันเข้ารหัส PDF ---
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

        log_action(input_path, output_path, "Success")
        showinfo("Success", f"✅ PDF saved:\n{output_path}")
    except Exception as e:
        log_action(input_path, output_path, "Failed", str(e))
        showinfo("Error", f"❌ Failed to encrypt:\n{e}")

# --- ฟังก์ชันลากไฟล์ ---
def drop_file(event):
    path = event.data.strip("{}")  # remove brackets from drag-drop
    pdf_path.set(path)

def browse_pdf():
    filename = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if filename:
        pdf_path.set(filename)

# --- GUI เริ่มที่นี่ ---
app = TkinterDnD.Tk()
app.title("🔐 PDF Encryptor - Drag & Drop")
app.geometry("450x300")
app.configure(bg="#f4f4f4")

# โหลด default จาก .env
pdf_path = StringVar(value=os.getenv("PDF_PATH", ""))
output_filename = StringVar(value=os.getenv("OUTPUT_FILE", "test_Encrypt.pdf"))
password = StringVar(value=os.getenv("PDF_PASSWORD", ""))

Label(app, text="Drag & Drop PDF หรือกด Browse", bg="#f4f4f4").pack(pady=10)

entry_pdf = Entry(app, textvariable=pdf_path, width=60)
entry_pdf.pack()
entry_pdf.drop_target_register(DND_FILES)
entry_pdf.dnd_bind('<<Drop>>', drop_file)

Button(app, text="Browse PDF", command=browse_pdf).pack(pady=5)

Label(app, text="Output Filename:", bg="#f4f4f4").pack(pady=5)
Entry(app, textvariable=output_filename, width=60).pack()

Label(app, text="Password:", bg="#f4f4f4").pack(pady=5)
Entry(app, textvariable=password, show="*", width=60).pack()

Button(app, text="🔐 Encrypt PDF", command=encrypt_pdf).pack(pady=20)

app.mainloop()

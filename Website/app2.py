import os
import csv
import json
from flask import Flask, render_template, request, send_from_directory, redirect, url_for, flash
from dotenv import load_dotenv
from pypdf import PdfReader, PdfWriter
from datetime import datetime
from getpass import getuser

load_dotenv()

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "encrypted"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app = Flask(__name__)
app.secret_key = "secret"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

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

    # Log to JSON
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

    # Log to CSV
    write_header = not os.path.exists(LOG_CSV)
    with open(LOG_CSV, "a", newline='', encoding="utf-8") as cf:
        writer = csv.DictWriter(cf, fieldnames=log_entry.keys())
        if write_header:
            writer.writeheader()
        writer.writerow(log_entry)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        uploaded_file = request.files.get("pdf_file")
        password = request.form.get("password")

        if not uploaded_file or not password:
            flash("กรุณาเลือกไฟล์ PDF และกรอกรหรัสผ่าน", "error")
            return redirect(url_for("index"))

        filename = uploaded_file.filename
        save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        uploaded_file.save(save_path)

        output_file = f"encrypted_{filename}"
        output_path = os.path.join(OUTPUT_FOLDER, output_file)

        try:
            reader = PdfReader(save_path)
            writer = PdfWriter(clone_from=reader)
            writer.encrypt(password, algorithm="AES-256")

            with open(output_path, "wb") as f:
                writer.write(f)

            log_action(save_path, output_path, "Success")
            return redirect(url_for("download_file", filename=output_file))

        except Exception as e:
            log_action(save_path, output_path, "Failed", str(e))
            flash(f"การเข้ารหัสล้มเหลว: {str(e)}", "error")
            return redirect(url_for("index"))

    return render_template("index.html")

@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(OUTPUT_FOLDER, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)

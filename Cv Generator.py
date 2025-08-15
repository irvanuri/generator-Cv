import streamlit as st
from docx import Document
from docx.shared import Inches
from docx2pdf import convert
import os

# Fungsi ekstrak kata kunci dari Job Description sederhana (split manual)
def extract_keywords_simple(text):
    words = text.split()
    unique_words = list(set([w.strip(",.!?").lower() for w in words if len(w) > 3]))
    return unique_words[:10]

# Fungsi membuat CV
def generate_cv(data, photo_path, output_format="docx"):
    doc = Document()

    # Header dengan foto
    table = doc.add_table(rows=1, cols=2)
    row = table.rows[0]
    cell1 = row.cells[0]
    cell2 = row.cells[1]

    if photo_path:
        cell1.paragraphs[0].add_run().add_picture(photo_path, width=Inches(1.5))
    else:
        cell1.text = ""

    cell2.add_paragraph(data['name']).bold = True
    cell2.add_paragraph(f"{data['phone']} | {data['email']}")
    cell2.add_paragraph(f"{data['location']}")
    if data['linkedin']:
        cell2.add_paragraph(f"LinkedIn: {data['linkedin']}")
    if data['portfolio']:
        cell2.add_paragraph(f"Portfolio: {data['portfolio']}")

    doc.add_paragraph()

    # Ringkasan
    doc.add_heading("Ringkasan Profil", level=1)
    doc.add_paragraph(data['summary'])

    # Pengalaman Kerja
    doc.add_heading("Pengalaman Kerja", level=1)
    for exp in data['experience']:
        doc.add_heading(f"{exp['job_title']} – {exp['company']}", level=2)
        doc.add_paragraph(f"{exp['location']} | {exp['start_date']} – {exp['end_date']}")
        for task in exp['tasks']:
            doc.add_paragraph(f"• {task}", style='List Bullet')

    # Pendidikan
    doc.add_heading("Pendidikan", level=1)
    for edu in data['education']:
        doc.add_paragraph(f"{edu['degree']} – {edu['school']} ({edu['year']})")

    # Sertifikasi
    doc.add_heading("Sertifikasi", level=1)
    for cert in data['certifications']:
        doc.add_paragraph(f"{cert['name']} – {cert['issuer']} ({cert['year']})")

    # Keahlian
    doc.add_heading("Keahlian", level=1)
    doc.add_paragraph(f"Hard Skills: {', '.join(data['hard_skills'])}")
    doc.add_paragraph(f"Soft Skills: {', '.join(data['soft_skills'])}")
    doc.add_paragraph(f"Tools & Software: {', '.join(data['tools'])}")

    # Simpan Word
    filename_docx = f"CV_ATS_{data['name'].replace(' ', '_')}.docx"
    doc.save(filename_docx)

    # Konversi PDF jika dipilih
    if output_format == "pdf":
        filename_pdf = filename_docx.replace(".docx", ".pdf")
        convert(filename_docx, filename_pdf)
        return filename_pdf
    return filename_docx

# ===== STREAMLIT APP =====
st.set_page_config(page_title="ATS CV Builder (No NLP)", layout="wide")
st.title("📄 ATS-Friendly CV Builder + Foto (Tanpa NLP)")

# Sidebar Job Description (Opsional)
st.sidebar.header("Job Description (Opsional)")
jd_text = st.sidebar.text_area("Tempel Job Description di sini")
jd_file = st.sidebar.file_uploader("atau Upload File .txt", type=["txt"])
if jd_file:
    jd_text = jd_file.read().decode("utf-8")

jd_keywords = extract_keywords_simple(jd_text) if jd_text else []

# Informasi Pribadi
st.header("Informasi Pribadi")
name = st.text_input("Nama Lengkap")
phone = st.text_input("Nomor Telepon")
email = st.text_input("Email Profesional")
location = st.text_input("Lokasi Domisili")
linkedin = st.text_input("LinkedIn URL", "")
portfolio = st.text_input("Portfolio / GitHub", "")

# Upload Foto
photo_file = st.file_uploader("Upload Foto (Opsional)", type=["jpg", "jpeg", "png"])
photo_path = None
if photo_file:
    photo_path = os.path.join("temp_photo." + photo_file.name.split(".")[-1])
    with open(photo_path, "wb") as f:
        f.write(photo_file.read())

# Ringkasan Profil
st.header("Ringkasan Profil")
summary = st.text_area("Deskripsikan profil singkat Anda (2-3 kalimat)")

# Pengalaman Kerja
st.header("Pengalaman Kerja")
experience = []
exp_count = st.number_input("Jumlah pengalaman kerja", min_value=0, max_value=10, step=1)
for i in range(exp_count):
    st.subheader(f"Pengalaman #{i+1}")
    company = st.text_input(f"Perusahaan #{i+1}")
    job_title = st.text_input(f"Jabatan #{i+1}")
    location_exp = st.text_input(f"Lokasi #{i+1}")
    start_date = st.text_input(f"Tanggal Mulai #{i+1}")
    end_date = st.text_input(f"Tanggal Selesai #{i+1}")
    tasks_raw = st.text_area(f"Tugas & Pencapaian (pisahkan dengan koma) #{i+1}").split(",")
    tasks_clean = [t.strip() for t in tasks_raw if t.strip()]

    # Tambahkan kata kunci JD (opsional)
    for kw in jd_keywords:
        if kw.lower() not in " ".join(tasks_clean).lower():
            tasks_clean.append(f"Pengalaman terkait {kw}")

    experience.append({
        "company": company,
        "job_title": job_title,
        "location": location_exp,
        "start_date": start_date,
        "end_date": end_date,
        "tasks": tasks_clean
    })

# Pendidikan
st.header("Pendidikan")
education = []
edu_count = st.number_input("Jumlah pendidikan", min_value=0, max_value=5, step=1)
for i in range(edu_count):
    school = st.text_input(f"Sekolah/Kampus #{i+1}")
    degree = st.text_input(f"Gelar/Jurusan #{i+1}")
    year = st.text_input(f"Tahun Lulus #{i+1}")
    education.append({"school": school, "degree": degree, "year": year})

# Sertifikasi
st.header("Sertifikasi")
certifications = []
cert_count = st.number_input("Jumlah sertifikasi", min_value=0, max_value=10, step=1)
for i in range(cert_count):
    cert_name = st.text_input(f"Nama Sertifikat #{i+1}")
    issuer = st.text_input(f"Penerbit #{i+1}")
    cert_year = st.text_input(f"Tahun #{i+1}")
    certifications.append({"name": cert_name, "issuer": issuer, "year": cert_year})

# Keahlian
st.header("Keahlian")
hard_skills = st.text_area("Hard Skills (pisahkan dengan koma)").split(",")
soft_skills = st.text_area("Soft Skills (pisahkan dengan koma)").split(",")
tools = st.text_area("Tools & Software (pisahkan dengan koma)").split(",")

# Pilihan Output
output_format = st.selectbox("Pilih format output CV", ["docx", "pdf"])

# Generate CV
if st.button("🚀 Generate CV"):
    data = {
        "name": name,
        "phone": phone,
        "email": email,
        "location": location,
        "linkedin": linkedin,
        "portfolio": portfolio,
        "summary": summary,
        "experience": experience,
        "education": education,
        "certifications": certifications,
        "hard_skills": [x.strip() for x in hard_skills if x.strip()],
        "soft_skills": [x.strip() for x in soft_skills if x.strip()],
        "tools": [x.strip() for x in tools if x.strip()]
    }
    filename = generate_cv(data, photo_path, output_format)
    st.success(f"✅ CV berhasil dibuat: {filename}")
    with open(filename, "rb") as f:
        st.download_button(f"📥 Download CV ({output_format.upper()})", f, file_name=filename)

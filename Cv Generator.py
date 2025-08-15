import streamlit as st
from docx import Document
from docx.shared import Inches
from docx2pdf import convert
import os

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
    cell2.add_paragraph(f"{data['address']}")

    doc.add_paragraph()

    # Profil
    doc.add_heading("Profil Profesional", level=1)
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
        doc.add_paragraph(f"{edu['degree']} – {edu['school']} ({edu['year']}) | IPK: {edu['gpa']}")

    # Pengalaman Organisasi
    doc.add_heading("Pengalaman Organisasi", level=1)
    for org in data['organizations']:
        doc.add_heading(f"{org['role']} – {org['name']}", level=2)
        doc.add_paragraph(f"{org['location']} | {org['start_date']} – {org['end_date']}")
        for desc in org['description']:
            doc.add_paragraph(f"• {desc}", style='List Bullet')

    # Keahlian
    doc.add_heading("Kemampuan", level=1)
    doc.add_paragraph(f"Hard Skills: {', '.join(data['hard_skills'])}")
    doc.add_paragraph(f"Soft Skills: {', '.join(data['soft_skills'])}")

    # Pencapaian
    doc.add_heading("Pencapaian Lainnya", level=1)
    for ach in data['achievements']:
        doc.add_paragraph(f"• {ach}", style='List Bullet')

    # Simpan file
    filename_docx = f"CV_{data['name'].replace(' ', '_')}.docx"
    doc.save(filename_docx)

    if output_format == "pdf":
        filename_pdf = filename_docx.replace(".docx", ".pdf")
        convert(filename_docx, filename_pdf)
        return filename_pdf
    return filename_docx


# ===== STREAMLIT UI =====
st.set_page_config(page_title="CV Builder", layout="wide")
st.title("📄 CV Builder Heppy Nugraha")

# Informasi Pribadi
st.header("Informasi Pribadi")
name = st.text_input("Nama Lengkap", "HEPPY NUGRAHA, S.P")
phone = st.text_input("Nomor Telepon", "+6285250101045")
email = st.text_input("Email", "hepiebleeding@gmail.com")
address = st.text_area("Alamat", "Jl. Tari Dewa-Dewa 1 No. 17 RT. 14, Kelurahan Guntung, Kecamatan Bontang Utara, Kota Bontang, Kalimantan Timur")

# Upload Foto
photo_file = st.file_uploader("Upload Foto (Opsional)", type=["jpg", "jpeg", "png"])
photo_path = None
if photo_file:
    photo_path = os.path.join("temp_photo." + photo_file.name.split(".")[-1])
    with open(photo_path, "wb") as f:
        f.write(photo_file.read())

# Profil
st.header("Profil Profesional")
summary = st.text_area("Ringkasan Profil", "Saya Lulusan baru di bidang Agroteknologi dengan kemampuan riset dan kerja tim yang baik...")

# Pengalaman Kerja
st.header("Pengalaman Kerja")
experience = []
exp_count = st.number_input("Jumlah pengalaman kerja", min_value=0, max_value=10, value=2)
for i in range(exp_count):
    st.subheader(f"Pengalaman #{i+1}")
    company = st.text_input(f"Perusahaan #{i+1}")
    job_title = st.text_input(f"Jabatan #{i+1}")
    location_exp = st.text_input(f"Lokasi #{i+1}")
    start_date = st.text_input(f"Tanggal Mulai #{i+1}")
    end_date = st.text_input(f"Tanggal Selesai #{i+1}")
    tasks = st.text_area(f"Tugas/Pencapaian #{i+1} (pisahkan dengan koma)").split(",")
    experience.append({
        "company": company,
        "job_title": job_title,
        "location": location_exp,
        "start_date": start_date,
        "end_date": end_date,
        "tasks": [t.strip() for t in tasks if t.strip()]
    })

# Pendidikan
st.header("Pendidikan")
education = []
edu_count = st.number_input("Jumlah pendidikan", min_value=0, max_value=5, value=1)
for i in range(edu_count):
    school = st.text_input(f"Sekolah/Kampus #{i+1}", "Universitas Mercu Buana Yogyakarta")
    degree = st.text_input(f"Gelar/Jurusan #{i+1}", "Sarjana Agroteknologi")
    year = st.text_input(f"Tahun Lulus #{i+1}", "2024")
    gpa = st.text_input(f"IPK #{i+1}", "3.29/4.00")
    education.append({"school": school, "degree": degree, "year": year, "gpa": gpa})

# Organisasi
st.header("Pengalaman Organisasi")
organizations = []
org_count = st.number_input("Jumlah organisasi", min_value=0, max_value=10, value=3)
for i in range(org_count):
    name_org = st.text_input(f"Nama Organisasi #{i+1}")
    role_org = st.text_input(f"Peran #{i+1}")
    location_org = st.text_input(f"Lokasi #{i+1}")
    start_org = st.text_input(f"Tanggal Mulai #{i+1}")
    end_org = st.text_input(f"Tanggal Selesai #{i+1}")
    desc_org = st.text_area(f"Deskripsi #{i+1} (pisahkan dengan koma)").split(",")
    organizations.append({
        "name": name_org,
        "role": role_org,
        "location": location_org,
        "start_date": start_org,
        "end_date": end_org,
        "description": [d.strip() for d in desc_org if d.strip()]
    })

# Keahlian
st.header("Kemampuan")
hard_skills = st.text_area("Hard Skills (pisahkan dengan koma)").split(",")
soft_skills = st.text_area("Soft Skills (pisahkan dengan koma)").split(",")

# Pencapaian
st.header("Pencapaian Lainnya")
achievements = st.text_area("Pencapaian (pisahkan dengan koma)").split(",")

# Pilihan Output
output_format = st.selectbox("Pilih format output CV", ["docx", "pdf"])

# Generate
if st.button("🚀 Generate CV"):
    data = {
        "name": name,
        "phone": phone,
        "email": email,
        "address": address,
        "summary": summary,
        "experience": experience,
        "education": education,
        "organizations": organizations,
        "hard_skills": [x.strip() for x in hard_skills if x.strip()],
        "soft_skills": [x.strip() for x in soft_skills if x.strip()],
        "achievements": [x.strip() for x in achievements if x.strip()]
    }
    filename = generate_cv(data, photo_path, output_format)
    st.success(f"✅ CV berhasil dibuat: {filename}")
    with open(filename, "rb") as f:
        st.download_button(f"📥 Download CV ({output_format.upper()})", f, file_name=filename)

import streamlit as st
import pdfplumber
import os
import json
import pandas as pd
from datetime import datetime
import uuid
from collections import Counter

# -------------------- CONFIG --------------------
st.set_page_config(page_title="Resume IQ - Smart Ats Resume Analyzer", layout="wide")

# -------------------- NEON UI (FIXED) --------------------
st.markdown("""
<style>

/* BACKGROUND */
.stApp {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
}

/* GLOBAL TEXT */
html, body, [class*="css"] {
    color: #ffffff !important;
}

/* HEADINGS */
h1, h2, h3 {
    color: #e0aaff !important;
    text-align: center;
    text-shadow: 0 0 10px #9d4edd;
}

/* LABELS */
label {
    color: #ffffff !important;
    font-weight: bold;
}

/* INPUTS */
input, textarea {
    background-color: #1a1a2e !important;
    color: white !important;
    border-radius: 8px;
}

/* SELECT BOX */
div[data-baseweb="select"] > div {
    background-color: #1a1a2e !important;
    color: white !important;
}

/* BUTTONS */
.stButton>button {
    background: linear-gradient(45deg, #7209b7, #560bad);
    color: white;
    border-radius: 12px;
    height: 3em;
    font-weight: bold;
    border: none;
    box-shadow: 0 0 10px #9d4edd;
}
.stButton>button:hover {
    box-shadow: 0 0 20px #c77dff;
}

/* TABS */
[data-baseweb="tab"] {
    background-color: #1a1a2e;
    color: #c77dff;
}
[data-baseweb="tab"][aria-selected="true"] {
    background: #7209b7;
    color: white;
}

/* METRIC FIX */
[data-testid="stMetric"] {
    background: #1a1a2e;
    border-radius: 10px;
    padding: 15px;
    box-shadow: 0 0 15px #9d4edd;
}
[data-testid="stMetricValue"] {
    color: #ffffff !important;
    font-size: 28px;
    font-weight: bold;
}
[data-testid="stMetricLabel"] {
    color: #c77dff !important;
    font-weight: 600;
}

/* DATAFRAME */
[data-testid="stDataFrame"] {
    background-color: #1a1a2e !important;
    color: white !important;
}

/* ALERTS */
.stSuccess {border-left: 5px solid #00ffcc;}
.stError {border-left: 5px solid #ff4d6d;}
.stInfo {border-left: 5px solid #9d4edd;}

</style>
""", unsafe_allow_html=True)

# -------------------- PATHS --------------------
DB_FOLDER = "resumes_db"
PDF_FOLDER = os.path.join(DB_FOLDER, "pdfs")
os.makedirs(DB_FOLDER, exist_ok=True)
os.makedirs(PDF_FOLDER, exist_ok=True)

# -------------------- ROLES --------------------
ROLE_SKILLS = {
    "Frontend Developer": ["HTML","CSS","JavaScript","React","Angular","Vue","Bootstrap","Tailwind","Responsive Design","Git"],
    "Backend Developer": ["Python","Java","Node.js","Django","Flask","Spring Boot","REST API","SQL","MongoDB"],
    "Full Stack Developer": ["HTML","CSS","JavaScript","React","Node.js","Python","SQL","MongoDB"],
    "Software Tester": ["Manual Testing","Automation","Selenium","Test Cases","Bug Tracking","JIRA"],
    "Data Analyst": ["Python","SQL","Excel","Power BI","Tableau","Statistics"],
    "Data Scientist": ["Python","Machine Learning","Deep Learning","Pandas","NumPy","TensorFlow"],
    "DevOps Engineer": ["AWS","Docker","Kubernetes","CI/CD","Linux","Jenkins"],
    "Mobile App Developer": ["Android","iOS","Flutter","React Native","Kotlin","Swift"]
}
ROLES = list(ROLE_SKILLS.keys())

# -------------------- FUNCTIONS --------------------
def extract_text_from_pdf(path):
    text = ""
    try:
        with pdfplumber.open(path) as pdf:
            for p in pdf.pages:
                text += p.extract_text() or ""
    except:
        st.error("Error reading PDF")
    return text.lower()

def calculate_ats(text, skills):
    matched = [s for s in skills if s.lower() in text]
    missing = [s for s in skills if s.lower() not in text]
    score = int((len(matched)/len(skills))*100) if skills else 0
    status = "Selected" if score >= 60 else "Rejected"
    return score, status, matched, missing

def generate_ai_feedback(score, matched, missing):
    if score >= 80:
        return f"Excellent: {', '.join(matched[:5])}"
    elif score >= 60:
        return f"Good. Improve: {', '.join(missing[:3])}"
    return f"Missing: {', '.join(missing[:5])}"

def save_resume(data):
    with open(os.path.join(DB_FOLDER, f"{data['id']}.json"), "w") as f:
        json.dump(data, f, indent=4)

def load_resumes():
    data = []
    for f in os.listdir(DB_FOLDER):
        if f.endswith(".json"):
            try:
                d = json.load(open(os.path.join(DB_FOLDER, f)))
                d["json_file"] = f
                data.append(d)
            except:
                pass
    return pd.DataFrame(data) if data else pd.DataFrame()

def delete_resume_by_id(rid):
    df = load_resumes()
    row = df[df["id"] == rid]
    if row.empty:
        return False, "Invalid ID"
    row = row.iloc[0]
    if row["status"] != "Rejected":
        return False, "Only rejected resumes can be deleted"
    os.remove(os.path.join(DB_FOLDER, row["json_file"]))
    if os.path.exists(row["pdf_path"]):
        os.remove(row["pdf_path"])
    return True, "Deleted successfully"

def display_skills(skills, color):
    for s in skills:
        st.markdown(
            f"<span style='background:{color};padding:6px;border-radius:10px;margin:3px;color:black;font-weight:bold'>{s}</span>",
            unsafe_allow_html=True
        )

# -------------------- UI --------------------
st.title("🚀 Resume IQ - Smart Ats Resume Analyzer")

tab1, tab2, tab3, tab4 = st.tabs([
    "📤 Resume Scan",
    "🛠 Admin Dashboard",
    "🗑 Delete Resume",
    "📊 Reports"
])

# -------------------- SCAN --------------------
with tab1:
    role = st.selectbox("Select Job Role", ["Select Role"] + ROLES)
    pdfs = st.file_uploader("Upload up to 5 resumes", type=["pdf"], accept_multiple_files=True)

    if st.button("🔍 Scan Resume"):
        if role == "Select Role":
            st.error("Please select a job role")
        elif not pdfs:
            st.error("Upload resumes")
        elif len(pdfs) > 5:
            st.error("Maximum 5 resumes allowed")
        else:
            for pdf in pdfs:
                name = pdf.name.replace(".pdf", "")
                email = f"{name.lower().replace(' ','')}@mail.com"
                path = os.path.join(PDF_FOLDER, pdf.name)

                with open(path, "wb") as f:
                    f.write(pdf.read())

                text = extract_text_from_pdf(path)
                score, status, matched, missing = calculate_ats(text, ROLE_SKILLS[role])
                feedback = generate_ai_feedback(score, matched, missing)
                uid = str(uuid.uuid4())[:8]

                save_resume({
                    "id": uid,
                    "name": name,
                    "email": email,
                    "role": role,
                    "ats_score": score,
                    "status": status,
                    "matched_skills": matched,
                    "missing_skills": missing,
                    "feedback": feedback,
                    "pdf_path": path
                })

                st.markdown("---")
                st.subheader(pdf.name)

                c1, c2 = st.columns(2)
                with c1:
                    if status == "Selected":
                        st.success(status)
                    else:
                        st.error(status)
                    st.metric("Score", f"{score}%")
                    st.progress(score)
                    st.write("ID:", uid)
                with c2:
                    st.info(feedback)

                c3, c4 = st.columns(2)
                with c3:
                    st.write("Matched Skills")
                    display_skills(matched, "#00ffcc")
                with c4:
                    st.write("Missing Skills")
                    display_skills(missing, "#ff4d6d")

# -------------------- ADMIN --------------------
with tab2:
    df = load_resumes()
    if df.empty:
        st.info("No resumes available")
    else:
        role_filter = st.selectbox("Filter by Role", ["All"] + ROLES)
        if role_filter != "All":
            df = df[df["role"] == role_filter]

        st.markdown("### ✅ Selected Candidates")
        st.dataframe(df[df["status"]=="Selected"][["id","name","role","ats_score"]])

        st.markdown("### ❌ Rejected Candidates")
        st.dataframe(df[df["status"]=="Rejected"][["id","name","role","ats_score"]])

# -------------------- DELETE --------------------
with tab3:
    df = load_resumes()
    if not df.empty:
        rej = df[df["status"]=="Rejected"]
        st.dataframe(rej[["id","name","role"]])

        rid = st.text_input("Enter Resume ID")
        if st.button("Delete Resume"):
            ok, msg = delete_resume_by_id(rid)
            if ok:
                st.success(msg)
            else:
                st.error(msg)

# -------------------- REPORT --------------------
with tab4:
    df = load_resumes()
    if not df.empty:
        total = len(df)
        sel = len(df[df["status"]=="Selected"])
        rej = len(df[df["status"]=="Rejected"])

        c1, c2, c3 = st.columns(3)
        c1.metric("Total", total)
        c2.metric("Selected", sel)
        c3.metric("Rejected", rej)

        st.markdown("### 🏆 Top Candidates")
        st.dataframe(df.sort_values("ats_score", ascending=False).head())

        missing = []
    
        for m in df["missing_skills"]:
            missing += m

        cnt = Counter(missing)
        st.markdown("### 📉 Skill Gap")
        st.dataframe(pd.DataFrame(cnt.items(), columns=["Skill","Count"]).sort_values("Count", ascending=False))

        st.markdown("### 🎯 Ranking by Role")
        r = st.selectbox("Select Role", ["All"] + ROLES)

        if r != "All":
            df = df[df["role"] == r]

        ranked = df.sort_values("ats_score", ascending=False).reset_index(drop=True)
        ranked["Rank"] = ranked.index + 1

        st.dataframe(ranked[["Rank","name","role","ats_score","status"]])
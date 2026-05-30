import streamlit as st
from parser import extract_text_from_pdf
from scorer import evaluate_candidate, generate_email
from utils import save_to_csv
import json

st.set_page_config(page_title="Hiring Dashboard", layout="centered")

# ===== STYLE =====
st.markdown("""
<style>

/* Background */
body {
    background-color: #f5f7fb;
}

/* Container */
.block-container {
    padding-top: 2rem;
}

/* Card */
.card {
    background: #ffffff;
    padding: 18px;
    border-radius: 10px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    margin-bottom: 18px;
    border: 1px solid #e2e8f0;
}

/* Headings */
h1 {
    color: #1e293b;
    font-weight: 600;
}

h2, h3 {
    color: #334155;
}

/* Accent line */
h3 {
    border-bottom: 2px solid #3b82f6;
    padding-bottom: 4px;
    display: inline-block;
}

/* Button */
div.stButton > button {
    background: #3b82f6;
    color: white;
    border-radius: 8px;
    padding: 8px;
    border: none;
    font-weight: 500;
}

div.stButton > button:hover {
    background: #2563eb;
}

/* Metrics */
[data-testid="stMetric"] {
    background: #f1f5f9;
    padding: 10px;
    border-radius: 8px;
    border-left: 3px solid #3b82f6;
}

/* Alerts */
.stAlert {
    border-radius: 8px;
}

</style>
""", unsafe_allow_html=True)

# ===== HEADER =====
st.markdown("<h1>Hiring Evaluation Dashboard</h1>", unsafe_allow_html=True)
st.caption("Resume Screening System")

st.divider()

# ===== INPUT =====
st.markdown("<div class='card'>", unsafe_allow_html=True)

st.subheader("Candidate Information")

col1, col2 = st.columns(2)

with col1:
    name = st.text_input("Full Name")
    email = st.text_input("Email")

with col2:
    phone = st.text_input("Phone Number")
    role = st.selectbox(
        "Position",
        ["Python Developer", "Frontend Developer", "AI/ML Engineer"]
    )

resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
submit = st.button("Evaluate")

st.markdown("</div>", unsafe_allow_html=True)

# ===== MAIN =====
if submit:
    if not resume_file:
        st.error("Upload resume")
    elif not name or not email or not phone:
        st.error("Fill all details")
    else:
        resume_text = extract_text_from_pdf(resume_file)

        if not resume_text.strip():
            st.error("Unable to extract text")
        else:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.subheader("Resume Preview")
            st.code(resume_text[:400])
            st.markdown("</div>", unsafe_allow_html=True)

            ai_response = evaluate_candidate(resume_text, role)

            try:
                data = json.loads(ai_response)

                st.markdown("<div class='card'>", unsafe_allow_html=True)

                st.subheader("Evaluation Summary")

                col1, col2 = st.columns(2)

                with col1:
                    st.metric("Score", data["score"])

                with col2:
                    st.write("Status")
                    st.write(data["decision"].capitalize())

                st.write("Summary")
                st.write(data["summary"])

                col1, col2 = st.columns(2)

                with col1:
                    st.metric("Skills Match", data["skills_match"])

                with col2:
                    st.metric("Experience Match", data["experience_match"])

                st.markdown("</div>", unsafe_allow_html=True)

                # ===== COMMUNICATION =====
                st.markdown("<div class='card'>", unsafe_allow_html=True)

                st.subheader("Communication Draft")

                email_text = generate_email(name, data["decision"])
                st.text_area("Email", email_text, height=150)

                st.markdown("Send Message")

                col1, col2 = st.columns(2)

                # Encode text for URL
                encoded_text = email_text.replace(" ", "%20").replace("\n", "%0A")

                # Gmail
                gmail_link = f"https://mail.google.com/mail/?view=cm&fs=1&to={email}&su=Application%20Update&body={encoded_text}"

                # WhatsApp (ensure number format: 91XXXXXXXXXX)
                whatsapp_link = f"https://wa.me/{phone}?text={encoded_text}"

                with col1:
                    st.link_button("Send via Gmail", gmail_link)

                with col2:
                    st.link_button("Send via WhatsApp", whatsapp_link)

                st.markdown("</div>", unsafe_allow_html=True)

                # ===== SAVE =====
                save_to_csv({
                    "name": name,
                    "email": email,
                    "phone": phone,
                    "role": role,
                    "score": data["score"],
                    "decision": data["decision"]
                })

                st.success("Record saved")

            except:
                st.error("Evaluation failed")
                st.code(ai_response)

# ===== FOOTER =====
st.markdown("<div class='card'>", unsafe_allow_html=True)

st.subheader("Notes")

st.write("""
- OCR used for scanned resumes  
- AI-based evaluation  
- Communication is integrated via Gmail and WhatsApp links  
""")

st.markdown("</div>", unsafe_allow_html=True)
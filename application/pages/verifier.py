import hashlib
import os
import streamlit as st
import pdfplumber
from utils.streamlit_utils import view_certificate, displayPDF, hide_icons, hide_sidebar, remove_whitespaces
from connection import contract

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
hide_icons()
hide_sidebar()
remove_whitespaces()

def extract_certificate(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())

    lines = text.splitlines()
    print("Extracted Certificate Text:\n", text)

    try:
        org_name = lines[0].strip()
        candidate_name = lines[3].strip()
        uid = lines[5].strip()

        # ✅ Extract the course name correctly
        date_index = next(i for i, line in enumerate(lines) if "Date of Issue" in line)
        course_name = lines[date_index - 1].strip()  # The line before "Date of Issue"

        print(f"Extracted Data: UID: {uid}, Candidate: {candidate_name}, Course: {course_name}, Org: {org_name}")
        return uid, candidate_name, course_name, org_name
    except IndexError:
        raise ValueError("Error extracting certificate details. Check PDF format.")


options = ("Verify Certificate using PDF", "View/Verify Certificate using Certificate ID")
selected = st.selectbox("", options, label_visibility="hidden")

if selected == options[0]:
    uploaded_file = st.file_uploader("Upload the PDF version of the certificate")
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        with open("certificate.pdf", "wb") as file:
            file.write(bytes_data)
        
        try:
            uid, candidate_name, course_name, org_name = extract_certificate("certificate.pdf")
            displayPDF("certificate.pdf")
            os.remove("certificate.pdf")

            # ✅ Ensure proper formatting before hashing
            data_to_hash = f"{uid.strip()}{candidate_name.strip()}{course_name.strip()}{org_name.strip()}".encode('utf-8')
            certificate_id = hashlib.sha256(data_to_hash).hexdigest()

            print(f"Computed Certificate ID: {certificate_id}")

            # ✅ Blockchain Verification
            result = contract.functions.isVerified(certificate_id).call()
            if result:
                st.success("Certificate validated successfully! 🎉")
            else:
                st.error("Invalid Certificate! Certificate might be tampered.")
        except Exception as e:
            st.error("Invalid Certificate! Certificate might be tampered.")
            print(f"Exception: {e}")

elif selected == options[1]:
    form = st.form("Validate-Certificate")
    certificate_id = form.text_input("Enter the Certificate ID")
    submit = form.form_submit_button("Validate")
    if submit:
        try:
            view_certificate(certificate_id)

            # ✅ Check if the certificate exists on the blockchain
            result = contract.functions.isVerified(certificate_id).call()
            if result:
                st.success("Certificate validated successfully! 🎉")
            else:
                st.error("Invalid Certificate ID!")
        except Exception as e:
            st.error("Invalid Certificate ID!")
            print(f"Exception: {e}")

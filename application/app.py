import streamlit as st
from PIL import Image
from utils.streamlit_utils import hide_icons, hide_sidebar, remove_whitespaces
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
hide_icons()
hide_sidebar()
remove_whitespaces()

# Center header and subheader using flex styling
st.markdown("<h1 style='display: flex; justify-content: center;'>Certificate Validation System</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='display: flex; justify-content: center; '>Select Your Role</h3>", unsafe_allow_html=True)

# Display Institute option (logo and button) centered with flex
st.markdown(
    "<div style='display: flex; flex-direction: column; align-items: center; justify-content: center;'>",
    unsafe_allow_html=True,
)
institute_logo = Image.open("../assets/image-removebg-preview.png")
st.image(institute_logo, output_format="jpg", width=230)
clicked_institute = st.button("Institute")
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Display Verifier option (logo and button) centered with flex
st.markdown(
    "<div style='display: flex; flex-direction: column; align-items: center; justify-content: center;'>",
    unsafe_allow_html=True,
)
company_logo = Image.open("../assets/image-removebg-preview (1).png")
st.image(company_logo, output_format="jpg", width=230)
clicked_verifier = st.button("Verifier")
st.markdown("</div>", unsafe_allow_html=True)

# Navigation logic
if clicked_institute:
    st.session_state.profile = "Institute"
    switch_page('login')
elif clicked_verifier:
    st.session_state.profile = "Verifier"
    switch_page('login')

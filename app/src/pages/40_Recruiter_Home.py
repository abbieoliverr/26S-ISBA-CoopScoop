import streamlit as st

st.set_page_config(layout='wide')

if 'recruiter_id' not in st.session_state:
    st.error('No recruiter logged in. Please return to the home page.')
    st.stop()

st.title('Recruiter Dashboard')
st.write(f"Welcome, {st.session_state.get('first_name', 'Recruiter')}!")
st.write('Use the sidebar to manage your listings, applicants, and view hiring analytics.')

from modules.nav import SideBarLinks
SideBarLinks()
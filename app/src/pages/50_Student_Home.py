import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.title(f"Welcome, {st.session_state['first_name']}!")
st.write('### What would you like to do today?')

if st.button('Browse Company Reviews & Interview Questions', use_container_width=True):
    st.switch_page('pages/51_Student_Reviews.py')

if st.button('My Applications & Notes', use_container_width=True):
    st.switch_page('pages/52_Student_Applications.py')

if st.button('Browse Co-op Listings', use_container_width=True):
    st.switch_page('pages/53_Student_Listings.py') 
import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

if 'advisor_id' not in st.session_state:
    st.error('No advisor logged in. Please return to the home page.')
    st.stop()

SideBarLinks()

st.title(f"Welcome, {st.session_state.get('first_name', 'Advisor')}!")
st.write('Use the links below or the sidebar to navigate your advisor tools.')

col1, col2, col3 = st.columns(3)

with col1:
    if st.button('Student Roster', use_container_width=True, type='primary'):
        st.switch_page('pages/30_Advisor_Roster.py')

with col2:
    if st.button('Student Profile & Notes', use_container_width=True, type='primary'):
        st.switch_page('pages/31_Advisor_Student_Profile.py')

with col3:
    if st.button('Cohort Stats & Offers', use_container_width=True, type='primary'):
        st.switch_page('pages/32_Advisor_Cohort_Stats.py')

import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

st.title(f"Welcome Coop-Scoop Administrator, {st.session_state['first_name']}.")
st.write('### What would you like to do today?')

SideBarLinks()


if st.button('View Users',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/21_User_Base.py')

if st.button('View Data Integrity Dashboard',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/22_Integrity_Dashboard.py')

if st.button('View Company Data',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/23_Company_Reviews.py')

if st.button('View Review Log',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/24_Review_Log.py')

if st.button('View Reviews Pending Approval',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/25_Pending_Reviews.py')


if st.button('Update Co-Op Cycle',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/26_Archive_Old.py')
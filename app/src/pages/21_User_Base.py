import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout='wide')

SideBarLinks()

st.title('User Database')

response = requests.get('http://api:4000/admins/users')

if response.status_code == 200:
    users = response.json()
    if users:
        for r in users:
            st.write(f"**User ID:** {r['userId']}")
            st.write(f"**Status:** {r['accountStatus']}")
            st.divider()
    else:
        st.info('No users found in the database.')
else:
    st.error(f'Error connecting to API: {response.text}')
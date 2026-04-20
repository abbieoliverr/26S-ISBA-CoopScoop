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
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(f"**User ID:** {r['userId']}")
                st.write(f"**Status:** {r['accountStatus']}")
            with col2:
                if r['accountStatus'] == "Active":
                    button_label = "Suspend"
                    target_status = "Suspended"
                else:
                    button_label = "Activate"
                    target_status = "Active"

                if st.button(button_label, key=f"switch_{r['userId']}"):
                        response = requests.put(f'http://api:4000/admins/users/{r["userId"]}/status', json={'status': target_status})
                        if response.status_code == 200:
                            st.rerun()
            st.divider()
    else:
        st.info('No users found in the database.')
else:
    st.error(f'Error connecting to API: {response.text}')
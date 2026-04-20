import logging
logger = logging.getLogger(__name__)
from datetime import datetime, timedelta
import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout='wide')

SideBarLinks()
st.title("Update Co-Op Cycle")

with st.expander("Add New Cycle"):
    with st.form("new"):
        name = st.text_input("Cycle Name")
        submit = st.form_submit_button("Create Cycle")
        if submit:
            if name:
                try:
                    response = requests.post("http://api:4000/admins/ccopcycle", json={"name": name})
                    if response.status_code == 201:
                        st.success(f"Successfully added cycle.")
                        st.rerun()
                    else:
                        st.error(f"Error: {response.json().get('error', 'Unknown error')}")
                except Exception as e:
                    st.error(f"Connection error: {e}")
            else:
                st.warning("Cycle is missing a name.")

st.divider()


st.subheader("Sync Data")

try:
    response = requests.get("http://api:4000/admins/coopcycle")
    if response.status_code == 200:
        cycles = response.json()
        if cycles:
            cur = 0
            for i in range(len(cycles)):
                if cycles[i]['current']:
                    cur = i
            cycle = st.selectbox(
                "Select the current co-op cycle.",
                options=cycles,
                index=cur,
                format_func=lambda x: x['name']
            )

            if st.button("Sync Data", type="primary"):
                response = requests.put(f"http://api:4000/admins/coopcycle/{cycle['cycleId']}/makecurrent")
                if response.status_code == 200:
                    st.success(f"Synced data.")
                    st.rerun()
                else:
                    st.error("Data failed to sync.")
        else:
            st.info("No cycles found.")
    else:
        st.error("Failed to fetch data from API.")

except Exception as e:
    st.error(f"Connection failed: {e}")
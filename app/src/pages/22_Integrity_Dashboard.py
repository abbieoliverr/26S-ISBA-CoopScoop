import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout='wide')

SideBarLinks()
st.title("Integrity Dashboard")

try:
    response = requests.get("http://api:4000/admins/data/integritydb")
    if response.status_code == 200:
        data = response.json()

        total_issues = sum(len(v) for v in data.values())
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Logic Errors", len(data['invalid_offer']) + len(data['invalid_search']))
        m2.metric("Incomplete Records", len(data['null_name']))
        m3.metric("Missing Relations", len(data['unassigned_advisor']))
        m4.error(f"Critical Issues: {total_issues}")

        st.divider()

        tab_overview, tab_logic, tab_users, tab_security = st.tabs([
            "Overview", "Logic & Cycles", "User Data", "Suspended Activity"
        ])

        with tab_overview:
            st.subheader("Inconsistencies")
            counts = {k: len(v) for k, v in data.items()}
            st.bar_chart(pd.Series(counts))

        with tab_logic:
            st.subheader("Search & Offer Discrepancies")
            if data['invalid_search']:
                st.warning("Students with searchStatus 'Searching' but co-op cycle not current:")
                st.table(data['invalid_search'])

            if data['invalid_offer']:
                st.error("Received offers without application status as 'Offered'")
                st.table(data['invalid_offer'])

        with tab_users:
            st.subheader("Missing first name or last name (or both)")
            if data['null_name']:
                st.dataframe(data['null_name'], use_container_width=True)

            if data['unassigned_advisor']:
                st.subheader("Not assigned an advisor")
                st.dataframe(data['unassigned_advisor'], use_container_width=True)

        with tab_security:
            st.subheader("Suspended User Actions")
            if data['suspended_activity']:
                st.error("Actions made by accounts that are suspended")
                st.dataframe(data['suspended_activity'], use_container_width=True)
            else:
                st.success("No activity from suspended users")

            if data['time_mismatch']:
                st.warning("Reviews with updates before creation")
                st.write(data['time_mismatch'])

    else:
        st.error(f"Failed to fetch data: {response.status_code}")

except Exception as e:
    st.error(f"Connection Error: {e}")
import logging
logger = logging.getLogger(__name__)
from datetime import datetime, timedelta
import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout='wide')

SideBarLinks()
st.title("Review Log")

col1, col2 = st.columns(2)
with col1:
    start = st.date_input("Start Date", datetime.now() - timedelta(days=30))
with col2:
    end = st.date_input("End Date", datetime.now())

if st.button("View Reviews Created in This Date Range"):
    params = {
        "start": start.strftime('%Y-%m-%d 00:00:00'),
        "end": end.strftime('%Y-%m-%d 23:59:59')
    }

    response = requests.get("http://api:4000/admins/reviews/log", params=params)

    if response.status_code == 200:
        reviews = response.json()
        st.metric("Reviews in this Range: ", len(reviews))

        if reviews:
            st.markdown("Review Details")
            c1, c2, c3, c4, c5 = st.columns([1, 1, 2, 2, 3])
            c1.write("**Date Created**")
            c2.write("**Last Updated**")
            c3.write("**Student**")
            c4.write("**Company**")
            c5.write("**Review**")
            st.divider()

            for r in reviews:
                c1, c2, c3, c4, c5 = st.columns([1, 1, 2, 2, 3])
                creation = datetime.strptime(r['creationTime'], '%a, %d %b %Y %H:%M:%S %Z')
                c1.write(creation.strftime('%m/%d/%Y'))
                last_update = datetime.strptime(r['lastUpdated'], '%a, %d %b %Y %H:%M:%S %Z')
                c2.write(last_update.strftime('%m/%d/%Y'))

                if r['anonymous']:
                    name = "Anonymous"
                else:
                    first = r.get('firstName')
                    last = r.get('lastName')
                    name = f"{first} {last}".strip()
                c3.write(name)
                c4.write(r['companyName'])
                with c5:
                    with st.expander(f"{r['content'][:30]}..."):
                        st.write(r['content'])
        else:
            st.warning("No submissions found for this time period.")
import logging
logger = logging.getLogger(__name__)
from datetime import datetime, timedelta
import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout='wide')

SideBarLinks()
st.title("Pending Reviews")

try:
    response = requests.get("http://api:4000/admins/reviews/pending")

    if response.status_code == 200:
        reviews = response.json()
        st.metric("Reviews pending approval: ", len(reviews))

        if reviews:
            st.markdown("Review Details")
            c1, c2, c3, c4, c5 = st.columns([1, 1, 1, 2, 2])
            c1.write("**Student**")
            c2.write("**Company**")
            c3.write("**Rating**")
            c4.write("**Content**")
            c5.write("**Approval**")
            st.divider()

            for r in reviews:
                if r['anonymous']:
                    name = "Anonymous"
                else:
                    first = r.get('firstName')
                    last = r.get('lastName')
                    name = f"{first} {last}".strip()

                c1, c2, c3, c4, c5, c6= st.columns([1, 1, 1, 2, 1, 1])
                c1.write(name)
                c2.write(r['companyName'])
                c3.write(r['rating'])
                with c4:
                    with st.expander(f"{r['content'][:30]}..."):
                        st.write(r['content'])
                with c5:
                    if st.button("Approve", key=f"app_{r['reviewId']}"):
                        res = requests.put(f"http://api:4000/admins/reviews/{r['reviewId']}/status",
                                         json={"status": "approved"})
                        if res.status_code == 200:
                            st.rerun()
                with c6:
                    if st.button("Reject", key=f"rej_{r['reviewId']}"):
                        res = requests.put(f"http://api:4000/admins/reviews/{r['reviewId']}/status",
                                         json={"status": "rejected"})
                        if res.status_code == 200:
                            st.rerun()
                st.divider()
        else:
            st.warning("No pending reviews.")
except Exception as e:
    st.error(f"Connection failed: {e}")
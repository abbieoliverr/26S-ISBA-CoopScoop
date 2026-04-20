import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout='wide')

SideBarLinks()
st.title("Company Reviews")

st.markdown("Sync Data")
if st.button("Sync Review Data", type="primary"):
    res = requests.post("http://api:4000/admins/reviews/sync")
    if res.status_code == 200:
        st.success(res.json().get('message'))
        st.rerun()


st.divider()
c1, c2, c3, c4, c5, c6, c7 = st.columns([2, 1, 3, 2, 2, 1, 2])
c1.markdown("**Company**")
c2.markdown("**Rating**")
c3.markdown("**Review**")
c4.markdown("**Review Status**")
c5.markdown("**Student**")
c6.markdown("**User ID**")
c7.markdown("**Account Status**")
st.divider()

response = requests.get('http://api:4000/admins/reviews')

if response.status_code == 200:
    reviews = response.json()
    for r in reviews:
        c1, c2, c3, c4, c5, c6, c7 = st.columns([2, 1, 3, 2, 2, 1, 2])
        if r['anonymous']:
            name = "Anonymous"
        else:
            first = r.get('firstName')
            last = r.get('lastName')
            name = f"{first} {last}".strip()

        r_color = "green"
        a_color = "grey"

        if r['approval'] == 'Rejected':
            r_color = "red"
        elif r['approval'] == 'Pending':
            r_color = "orange"

        if (r['accountStatus'] == 'Suspended' and r['approval'] != 'Rejected'):
            a_color = "red"


        c1.write(r['companyName'])
        c2.write(r['rating'])
        with c3:
            with st.expander(f"{r['content'][:30]}..."):
                st.write(r['content'])
        c4.markdown(f":{r_color}[{r['approval']}]")
        c5.write(name)
        c6.write(r['userId'])
        c7.markdown(f":{a_color}[{r['accountStatus']}]")
else:
    st.error("Data unavailable.")
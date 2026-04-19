import streamlit as st
import requests
 
st.set_page_config(layout='wide')
 
st.title('Browse Company Reviews')
 
company_id = st.number_input('Enter Company ID', min_value=1, step=1)
 
if st.button('See Reviews'):
    response = requests.get(f'http://api:4000/s/companies/{company_id}/reviews')
    if response.status_code == 200:
        reviews = response.json()
        if reviews:
            for r in reviews:
                st.subheader(r['position'])
                st.write(f"Rating: {r['rating']}/5")
                st.write(r['content'])
                st.divider()
        else:
            st.info('No approved reviews for this company yet.')
    else:
        st.error(f'Error: {response.text}')
 
st.divider()
st.subheader('Interview Questions')
 
if st.button('Get Interview History'):
    response = requests.get(f'http://api:4000/s/companies/{company_id}/interview-history')
    if response.status_code == 200:
        history = response.json()
        if history:
            for h in history:
                st.write(f"**{h['position']}**: {h['question']}")
        else:
            st.info('No interview history for this company yet.')
    else:
        st.error(f'Error: {response.text}')
 
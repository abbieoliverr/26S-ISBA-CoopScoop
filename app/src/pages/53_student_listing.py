import streamlit as st
import requests
 
st.set_page_config(layout='wide')
 
st.title('Browse Co-op Listings')
 
min_salary = st.number_input('Minimum Hourly Pay ($)', min_value=0, step=1)
min_rating = st.number_input('Minimum Peer Rating (0-5)', min_value=0, max_value=5, step=1)
cycle_id = st.selectbox('Co-op Cycle', options=[0, 1, 2, 3], format_func=lambda x: {0: 'All Cycles', 1: 'Spring 2026', 2: 'Fall 2025', 3: 'Spring 2025'}[x])
 
if st.button('Search Listings'):
    params = {'min_salary': min_salary, 'min_rating': min_rating}
    if cycle_id != 0:
        params['cycle_id'] = cycle_id
 
    response = requests.get('http://api:4000/s/listings', params=params)
    if response.status_code == 200:
        listings = response.json()
        if listings:
            st.dataframe(listings)
        else:
            st.info('Oh no! No listings match your filters.')
    else:
        st.error(f'Error: {response.text}')
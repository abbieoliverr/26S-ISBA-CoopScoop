import streamlit as st
import requests

st.set_page_config(layout='wide')

if 'recruiter_id' not in st.session_state:
    st.error('No recruiter logged in. Please return to the home page.')
    st.stop()

company_id = st.session_state['company_id']

st.title('Post a New Co-op Listing')

cycles_response = requests.get('http://api:4000/students/listings')

position_title = st.text_input('Position Title')
description = st.text_area('Description')
skills_required = st.text_input('Required Skills (e.g. Python, SQL, Git)')
location = st.text_input('Location')
salary = st.number_input('Hourly Pay ($)', min_value=0, step=1)
cycle_id = st.selectbox('Co-op Cycle', options=[1, 2, 3], format_func=lambda x: {1: 'Spring 2026', 2: 'Fall 2025', 3: 'Spring 2025'}[x])

if st.button('Post Listing'):
    if not position_title or not description or not location:
        st.warning('Please fill in all required fields.')
    else:
        payload = {
            'positionTitle': position_title,
            'description': description,
            'skillsRequired': skills_required,
            'location': location,
            'salary': salary,
            'companyId': company_id,
            'cycleId': cycle_id
        }
        response = requests.post('http://api:4000/recruiters/listings', json=payload)
        if response.status_code == 201:
            st.success('Listing posted successfully!')
        else:
            st.error(f'Error posting listing: {response.text}')

st.divider()
st.subheader('Update or Delete an Existing Listing')

listing_id = st.number_input('Listing ID to update/delete', min_value=1, step=1)

with st.expander('Update Listing'):
    new_title = st.text_input('New Position Title', key='update_title')
    new_desc = st.text_area('New Description', key='update_desc')
    new_skills = st.text_input('New Skills', key='update_skills')
    new_location = st.text_input('New Location', key='update_loc')
    new_salary = st.number_input('New Salary', min_value=0, step=1, key='update_sal')

    if st.button('Update Listing'):
        payload = {
            'positionTitle': new_title,
            'description': new_desc,
            'skillsRequired': new_skills,
            'location': new_location,
            'salary': new_salary
        }
        response = requests.put(f'http://api:4000/recruiters/listings/{listing_id}', json=payload)
        if response.status_code == 200:
            st.success('Listing updated.')
        else:
            st.error(f'Error: {response.text}')

if st.button('Delete Listing', type='primary'):
    response = requests.delete(f'http://api:4000/recruiters/listings/{listing_id}')
    if response.status_code == 200:
        st.success('Listing deleted.')
    else:
        st.error(f'Error: {response.text}')

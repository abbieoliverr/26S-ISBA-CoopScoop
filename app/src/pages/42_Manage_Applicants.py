import streamlit as st
import requests
import pandas as pd

st.set_page_config(layout='wide')

if 'recruiter_id' not in st.session_state:
    st.error('No recruiter logged in. Please return to the home page.')
    st.stop()

company_id = st.session_state['company_id']

st.title('Manage Applicants')

listing_id = st.number_input('Listing ID', min_value=1, step=1)
status_filter = st.selectbox('Filter by Status', options=['All', 'Pending', 'Interviewing', 'Offered', 'Rejected'])

params = {}
if status_filter != 'All':
    params['status'] = status_filter

response = requests.get(f'http://api:4000/recruiters/listings/{listing_id}/applications', params=params)

if response.status_code == 200:
    applicants = response.json()
    if applicants:
        df = pd.DataFrame(applicants)
        st.dataframe(df, use_container_width=True)

        st.subheader('Advance or Reject a Candidate')
        app_id = st.number_input('Application ID', min_value=1, step=1)
        new_status = st.selectbox('New Status', options=['Pending', 'Interviewing', 'Offered', 'Rejected'])

        if st.button('Update Status'):
            res = requests.put(
                f'http://api:4000/recruiters/applications/{app_id}/status',
                json={'status': new_status}
            )
            if res.status_code == 200:
                st.success(f'Application {app_id} updated to {new_status}.')

                if new_status == 'Interviewing':
                    st.subheader('Schedule an Interview')
                    interviewer_name = st.text_input('Interviewer Full Name')
                    interviewer_email = st.text_input('Interviewer Email')
                    interview_dt = st.text_input('Date and Time (YYYY-MM-DD HH:MM:SS)')
                    position = st.text_input('Position Title')
                    student_id = st.number_input('Student ID', min_value=1, step=1)

                    if st.button('Schedule Interview'):
                        payload = {
                            'headInterviewerFullName': interviewer_name,
                            'headInterviewerEmail': interviewer_email,
                            'dateTime': interview_dt,
                            'position': position,
                            'listingId': listing_id,
                            'studentId': student_id,
                            'companyId': company_id
                        }
                        ires = requests.post('http://api:4000/recruiters/interviews', json=payload)
                        if ires.status_code == 201:
                            st.success('Interview scheduled.')

                            st.subheader('Opted-In Former Co-ops at Your Company')
                            alumni_res = requests.get(f'http://api:4000/recruiters/companies/{company_id}/alumni')
                            if alumni_res.status_code == 200:
                                alumni = alumni_res.json()
                                if alumni:
                                    st.dataframe(pd.DataFrame(alumni), use_container_width=True)
                                else:
                                    st.info('No opted-in alumni found for this company.')
                        else:
                            st.error(f'Error scheduling interview: {ires.text}')
            else:
                st.error(f'Error updating status: {res.text}')
    else:
        st.info('No applicants found for this listing with the selected filter.')
else:
    st.error('Could not retrieve applicants. Check the listing ID.')

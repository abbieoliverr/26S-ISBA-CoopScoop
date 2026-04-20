import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

if 'advisor_id' not in st.session_state:
    st.error('No advisor logged in. Please return to the home page.')
    st.stop()

SideBarLinks()

advisor_id = st.session_state['advisor_id']

st.title('Co-Op Advisor Dashboard')
st.write(f"Welcome, {st.session_state.get('first_name', 'Advisor')}!")

response = requests.get(f'http://api:4000/advisor/{advisor_id}/students')

if response.status_code != 200:
    st.error('Could not retrieve student roster.')
    st.stop()

data = response.json()

if not data:
    st.info('No students found on your roster.')
    st.stop()

df = pd.DataFrame(data)
df.columns = [col.lower() for col in df.columns]

total_students = len(df)
total_applications = int(df['applicationcount'].sum())
active_students = int((df['searchstatus'] == 'Searching').sum())
needs_attention = int((df['applicationcount'] == 0).sum())

col1, col2, col3, col4 = st.columns(4)
col1.metric('Total Students', total_students)
col2.metric('Total Applications', total_applications)
col3.metric('Active (Searching)', active_students)
col4.metric('Needs Attention (0 Apps)', needs_attention)

st.divider()

search = st.text_input('Search by name')
status_filter = st.selectbox('Filter by Status', options=['All', 'Searching', 'Accepted Offer', 'Completed'])

filtered = df.copy()
if search:
    mask = (
        filtered['firstname'].str.contains(search, case=False, na=False) |
        filtered['lastname'].str.contains(search, case=False, na=False)
    )
    filtered = filtered[mask]
if status_filter != 'All':
    filtered = filtered[filtered['searchstatus'] == status_filter]

st.subheader(f'Students ({len(filtered)} shown)')

header = st.columns([3, 2, 2, 2])
header[0].markdown('**Name**')
header[1].markdown('**Status**')
header[2].markdown('**Applications**')
header[3].markdown('**Action**')

for _, row in filtered.iterrows():
    alert = '🚨 ' if row['applicationcount'] == 0 else ''
    cols = st.columns([3, 2, 2, 2])
    cols[0].write(f"{alert}{row['firstname']} {row['lastname']}")
    cols[1].write(row['searchstatus'])
    cols[2].write(int(row['applicationcount']))
    if cols[3].button('View Profile', key=f"view_{row['studentid']}"):
        st.session_state['selected_student_id'] = int(row['studentid'])
        st.session_state['selected_student_name'] = f"{row['firstname']} {row['lastname']}"
        st.switch_page('pages/31_Advisor_Student_Profile.py')

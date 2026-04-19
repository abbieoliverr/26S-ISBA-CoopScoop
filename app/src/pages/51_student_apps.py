import streamlit as st
import requests
 
st.set_page_config(layout='wide')
 
if 'student_id' not in st.session_state:
    st.error('No student logged in. Please return to the home page.')
    st.stop()
 
student_id = st.session_state['student_id']
 
st.title('My Applications')
 
response = requests.get(f'http://api:4000/s/{student_id}/applications')
if response.status_code == 200:
    applications = response.json()
    if applications:
        st.dataframe(applications)
    else:
        st.info('No applications yet! :(')
else:
    st.error(f'Error: {response.text}')
 
st.divider()
st.subheader('My Notes')
 
notes_response = requests.get(f'http://api:4000/s/{student_id}/notes')
if notes_response.status_code == 200:
    notes = notes_response.json()
    if notes:
        for note in notes:
            st.write(f"- {note['content']}")
    else:
        st.info('No notes yet!')
 
st.subheader('Add a Note')
new_note = st.text_input('New Note')
if st.button('Add Note'):
    response = requests.post(f'http://api:4000/s/{student_id}/notes', json={'content': new_note})
    if response.status_code == 201:
        st.success('Note added :)')
        st.rerun()
    else:
        st.error(f'Error: {response.text}')
 
st.subheader('Delete a Note')
note_id = st.number_input('Note ID to delete', min_value=1, step=1)
if st.button('Delete Note'):
    response = requests.delete(f'http://api:4000/s/{student_id}/notes/{note_id}')
    if response.status_code == 200:
        st.success('Note deleted!')
        st.rerun()
    else:
        st.error(f'Error: {response.text}')
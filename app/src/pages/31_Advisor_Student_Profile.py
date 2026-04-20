import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

if 'advisor_id' not in st.session_state:
    st.error('No advisor logged in. Please return to the home page.')
    st.stop()

SideBarLinks()

advisor_id = st.session_state['advisor_id']

if 'selected_student_id' not in st.session_state:
    st.warning('No student selected. Go to the Roster and click "View Profile".')
    if st.button('Go to Roster'):
        st.switch_page('pages/30_Advisor_Roster.py')
    st.stop()

student_id = st.session_state['selected_student_id']
student_name = st.session_state.get('selected_student_name', f'Student #{student_id}')

st.title(f'Student Profile: {student_name}')

if st.button('← Back to Roster'):
    st.switch_page('pages/30_Advisor_Roster.py')

st.divider()

# ---- Existing notes ---------------------------------------------------------

st.subheader('Advisor Notes')

notes_res = requests.get(f'http://api:4000/advisor/{advisor_id}/students/{student_id}/notes')

if notes_res.status_code == 200:
    notes = notes_res.json()
    if notes:
        for note in notes:
            note_id = note['advisorNoteId']
            timestamp = str(note.get('dateTime', ''))
            with st.expander(f"📝 {timestamp}"):
                st.write(note['content'])
                if st.button('Delete', key=f'del_{note_id}'):
                    del_res = requests.delete(f'http://api:4000/advisor/notes/{note_id}')
                    if del_res.status_code == 200:
                        st.success('Note deleted.')
                        st.rerun()
                    else:
                        st.error('Failed to delete note.')
    else:
        st.info('No notes yet for this student.')
else:
    st.error('Could not load notes.')

st.divider()

# ---- Add new note -----------------------------------------------------------

st.subheader('Add a Note')
new_note = st.text_area('Note content', key='new_note_input')

if st.button('Save Note'):
    if new_note.strip():
        res = requests.post(
            f'http://api:4000/advisor/{advisor_id}/notes',
            json={'studentId': student_id, 'content': new_note.strip()}
        )
        if res.status_code == 201:
            st.success('Note saved.')
            st.rerun()
        else:
            st.error(f'Failed to save note: {res.text}')
    else:
        st.warning('Note content cannot be empty.')

st.divider()

# ---- Update search status ---------------------------------------------------

st.subheader('Update Search Status')
new_status = st.selectbox('Status', options=['Searching', 'Accepted Offer', 'Completed'])

if st.button('Update Status'):
    res = requests.put(
        f'http://api:4000/advisor/{advisor_id}/students/{student_id}/status',
        json={'searchStatus': new_status}
    )
    if res.status_code == 200:
        st.success(f'Status updated to "{new_status}".')
    else:
        st.error(f'Failed to update status: {res.text}')

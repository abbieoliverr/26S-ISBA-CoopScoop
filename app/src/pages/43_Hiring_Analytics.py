import streamlit as st
import requests
import pandas as pd

st.set_page_config(layout='wide')

if 'recruiter_id' not in st.session_state:
    st.error('No recruiter logged in. Please return to the home page.')
    st.stop()

company_id = st.session_state['company_id']

st.title('Hiring Analytics')

response = requests.get(f'http://api:4000/recruiters/companies/{company_id}/analytics')

if response.status_code == 200:
    data = response.json()
    if data:
        df = pd.DataFrame(data)
        df.columns = [col.lower() for col in df.columns]

        total_applicants = df['totalapplicants'].sum()
        total_offers = df['totaloffers'].sum()
        overall_rate = round((total_offers / total_applicants * 100), 1) if total_applicants > 0 else 0
        active_positions = len(df)

        col1, col2, col3, col4 = st.columns(4)
        col1.metric('Total Applicants', total_applicants)
        col2.metric('Total Offers', total_offers)
        col3.metric('Overall Acceptance Rate', f'{overall_rate}%')
        col4.metric('Active Positions', active_positions)

        st.divider()

        st.subheader('Applicants Per Position')
        st.bar_chart(df.set_index('positiontitle')['totalapplicants'])

        st.subheader('Pipeline Breakdown')
        st.dataframe(
            df[['positiontitle', 'totalapplicants', 'ininterview',
                'totaloffers', 'totalrejected', 'acceptanceratepct', 'avgdaystointerview']],
            use_container_width=True
        )
    else:
        st.info('No analytics data found for your company.')
else:
    st.error('Could not retrieve analytics data.')

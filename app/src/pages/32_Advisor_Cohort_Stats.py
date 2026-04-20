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

st.title('Co-Op Offer Tracker')

# ---- Cohort stats -----------------------------------------------------------

stats_res = requests.get(f'http://api:4000/advisor/{advisor_id}/stats')

if stats_res.status_code == 200:
    stats = stats_res.json()
    if stats:
        df_stats = pd.DataFrame(stats)
        df_stats.columns = [col.lower() for col in df_stats.columns]

        companies_count = len(df_stats)
        total_accepted = int(df_stats['acceptedoffers'].sum())
        total_apps = int(df_stats['totalapplications'].sum())
        overall_rate = round(total_accepted / total_apps * 100, 1) if total_apps > 0 else 0
        avg_salary_val = pd.to_numeric(df_stats['avgsalary'], errors='coerce').dropna().mean()
        avg_salary_str = f'${avg_salary_val:,.0f}' if pd.notna(avg_salary_val) else 'N/A'

        col1, col2, col3 = st.columns(3)
        col1.metric('Companies Applied To', companies_count)
        col2.metric('Overall Acceptance Rate', f'{overall_rate}%')
        col3.metric('Avg Offer Salary', avg_salary_str)

        st.divider()
        st.subheader('Per-Company Breakdown')

        for _, row in df_stats.iterrows():
            with st.expander(f"{row['companyname']} — {int(row['totalapplications'])} applications"):
                c1, c2, c3, c4 = st.columns(4)
                c1.metric('Total Applications', int(row['totalapplications']))
                c2.metric('Accepted Offers', int(row['acceptedoffers']))
                rate = row['acceptancerate'] if pd.notna(row['acceptancerate']) else 0
                c3.metric('Acceptance Rate', f'{rate}%')
                sal = pd.to_numeric(row['avgsalary'], errors='coerce')
                c4.metric('Avg Salary', f'${sal:,.0f}' if pd.notna(sal) else 'N/A')
    else:
        st.info('No stats data available for your cohort.')
else:
    st.error('Could not load cohort stats.')

st.divider()

# ---- Individual offer outcomes ----------------------------------------------

st.subheader('Individual Offer Outcomes')

offers_res = requests.get(f'http://api:4000/advisor/{advisor_id}/offers')

if offers_res.status_code == 200:
    offers = offers_res.json()
    if offers:
        df_offers = pd.DataFrame(offers)
        df_offers.columns = [col.lower() for col in df_offers.columns]

        status_filter = st.selectbox(
            'Filter by Acceptance Status',
            options=['All', 'Accepted', 'Rejected', 'Pending']
        )

        if status_filter != 'All':
            df_offers = df_offers[df_offers['acceptancestatus'] == status_filter]

        st.dataframe(df_offers, use_container_width=True)
    else:
        st.info('No offer data available for your cohort.')
else:
    st.error('Could not load offer outcomes.')

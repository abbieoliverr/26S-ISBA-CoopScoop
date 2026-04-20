# Idea borrowed from https://github.com/fsmosca/sample-streamlit-authenticator

# This file has functions to add links to the left sidebar based on the user's role.

import streamlit as st


# ---- General ----------------------------------------------------------------

def home_nav():
    st.sidebar.page_link("Home.py", label="Home", icon="🏠")


def about_page_nav():
    st.sidebar.page_link("pages/30_About.py", label="About", icon="🧠")


# ---- Role: pol_strat_advisor ------------------------------------------------

def pol_strat_home_nav():
    st.sidebar.page_link(
        "pages/00_Pol_Strat_Home.py", label="Political Strategist Home", icon="👤"
    )


def world_bank_viz_nav():
    st.sidebar.page_link(
        "pages/01_World_Bank_Viz.py", label="World Bank Visualization", icon="🏦"
    )


def map_demo_nav():
    st.sidebar.page_link("pages/02_Map_Demo.py", label="Map Demonstration", icon="🗺️")


# ---- Role: usaid_worker -----------------------------------------------------

def usaid_worker_home_nav():
    st.sidebar.page_link(
        "pages/10_USAID_Worker_Home.py", label="USAID Worker Home", icon="🏠"
    )


def ngo_directory_nav():
    st.sidebar.page_link("pages/14_NGO_Directory.py", label="NGO Directory", icon="📁")


def add_ngo_nav():
    st.sidebar.page_link("pages/15_Add_NGO.py", label="Add New NGO", icon="➕")


def prediction_nav():
    st.sidebar.page_link(
        "pages/11_Prediction.py", label="Regression Prediction", icon="📈"
    )


def api_test_nav():
    st.sidebar.page_link("pages/12_API_Test.py", label="Test the API", icon="🛜")


def classification_nav():
    st.sidebar.page_link(
        "pages/13_Classification.py", label="Classification Demo", icon="🌺"
    )


# ---- Role: administrator ----------------------------------------------------

def admin_home_nav():
    st.sidebar.page_link("pages/20_Admin_Home.py", label="System Admin", icon="🖥️")

def user_base_nav():
    st.sidebar.page_link("pages/21_User_Base.py", label="User Database", icon="👥")

def integrity_dashboard_nav():
    st.sidebar.page_link("pages/22_Integrity_Dashboard.py", label="Data Integrity Dashboard", icon="📊")

def company_data_nav():
    st.sidebar.page_link("pages/23_Company_Reviews.py", label="Company Review Data", icon="💼")

def review_log_nav():
    st.sidebar.page_link("pages/24_Review_Log.py", label="Review Log", icon="➕")

def pending_reviews_nav():
    st.sidebar.page_link("pages/25_Pending_Reviews.py", label="Pending Reviews", icon="⭐")


# ---- Role: recruiter --------------------------------------------------------

def recruiter_home_nav():
    st.sidebar.page_link("pages/40_Recruiter_Home.py", label="Recruiter Home", icon="💼")

def post_listing_nav():
    st.sidebar.page_link("pages/41_Post_Listing.py", label="Post Listing", icon="➕")

def manage_applicants_nav():
    st.sidebar.page_link("pages/42_Manage_Applicants.py", label="Manage Applicants", icon="👥")

def hiring_analytics_nav():
    st.sidebar.page_link("pages/43_Hiring_Analytics.py", label="Hiring Analytics", icon="📊")


# ---- Role: student ----------------------------------------------------------

def student_home_nav():
    st.sidebar.page_link("pages/50_Student_Home.py", label="Student Home", icon="🎓")

def student_reviews_nav():
    st.sidebar.page_link("pages/52_Student_Rev.py", label="Browse Reviews", icon="⭐")

def student_apps_nav():
    st.sidebar.page_link("pages/51_student_apps.py", label="My Applications", icon="📋")

def student_listings_nav():
    st.sidebar.page_link("pages/53_student_listing.py", label="Browse Listings", icon="🔍")


# ---- Role: advisor ----------------------------------------------------------

def advisor_home_nav():
    st.sidebar.page_link("pages/30_Advisor_Home.py", label="Advisor Home", icon="🏠")


def advisor_roster_nav():
    st.sidebar.page_link("pages/30_Advisor_Roster.py", label="Student Roster", icon="👥")


def advisor_student_profile_nav():
    st.sidebar.page_link("pages/31_Advisor_Student_Profile.py", label="Student Profile", icon="👤")


def advisor_cohort_stats_nav():
    st.sidebar.page_link("pages/32_Advisor_Cohort_Stats.py", label="Cohort Stats", icon="📊")


def AdvisorHomeLinks():
    advisor_home_nav()
    advisor_roster_nav()
    advisor_student_profile_nav()
    advisor_cohort_stats_nav()


# ---- Sidebar assembly -------------------------------------------------------

def SideBarLinks(show_home=False):
    """
    Renders sidebar navigation links based on the logged-in user's role.
    The role is stored in st.session_state when the user logs in on Home.py.
    """

    # Logo appears at the top of the sidebar on every page
    st.sidebar.image("assets/logo.png", width=150)

    # If no one is logged in, send them to the Home (login) page
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.switch_page("Home.py")

    if show_home:
        home_nav()

    if st.session_state["authenticated"]:

        if st.session_state["role"] == "pol_strat_advisor":
            pol_strat_home_nav()
            world_bank_viz_nav()
            map_demo_nav()

        if st.session_state["role"] == "usaid_worker":
            usaid_worker_home_nav()
            ngo_directory_nav()
            add_ngo_nav()
            prediction_nav()
            api_test_nav()
            classification_nav()

        if st.session_state["role"] == "administrator":
            admin_home_nav()
            user_base_nav()
            integrity_dashboard_nav()
            company_data_nav()
            review_log_nav()
            pending_reviews_nav()
            pending_updates_nav()

        if st.session_state["role"] == "recruiter":
            recruiter_home_nav()
            post_listing_nav()
            manage_applicants_nav()
            hiring_analytics_nav()

        if st.session_state["role"] == "student":
            student_home_nav()
            student_reviews_nav()
            student_apps_nav()
            student_listings_nav()

        if st.session_state["role"] == "advisor":
            AdvisorHomeLinks()

    # About link appears at the bottom for all roles
    about_page_nav()

    if st.session_state["authenticated"]:
        if st.sidebar.button("Logout"):
            del st.session_state["role"]
            del st.session_state["authenticated"]
            st.switch_page("Home.py")


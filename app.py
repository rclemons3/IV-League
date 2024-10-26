# Import python packages
import streamlit as st
import snowflake.connector
import datetime
from sf_lib import sf_conn
import pandas as pd
from utilities import get_affiliate_options
from utilities import StateGroup


# Set page configuration
st.set_page_config(
    layout="wide",
    page_title="Affiliate User Update",
    page_icon="",
)

session = sf_conn()  # Assuming sf_conn() returns an active Snowflake session

# User Authentication using Azure AD Headers
if not "user_id" in st.session_state.keys():
    if "X-Ms-Client-Principal-Name" in st.context.headers:
        st.session_state["user_id"] = st.context.headers["X-Ms-Client-Principal-Name"]
    else:
        st.session_state["user_id"] = "rick.clemons@moser-inc.com"  # Default for testing

# Ensure user is logged in
if st.session_state.user_id == "":
    st.write("You are not authorized to use this service.")
else:
    # Display current user
    st.write(f"Currently logged in as {st.session_state['user_id']}")

    # Display notification if present
    if "toasts_to_show" in st.session_state:
        for message, icon in st.session_state["toasts_to_show"]:
            st.toast(message, icon=icon)
        st.session_state["toasts_to_show"] = []

    # Survey Form and Results Display
    @st.fragment()
    def display_survey_form(session, time_zone):
        """Display the survey form and handle form submission"""
        
        st.title("Affiliate User Update")
        
        # Collect user information
        Fname = st.text_input("User First Name", value="", placeholder="Enter user first name")
        Lname = st.text_input("User Last Name", value="", placeholder="Enter user last name")
        email = st.text_input("Email", value="", placeholder="Enter user email")

        # Fetch affiliate options from Snowflake
        affiliate_options = get_affiliate_options(session)  # Fetch affiliate options as a list
        affiliate = st.selectbox("Affiliate", options=affiliate_options)  # Populate dropdown
        
        # Form submission
        if st.button("Submit"):
            if Fname and Lname and email and affiliate:
                submission_time = datetime.datetime.now()
                data = {
                    "Fname": Fname,
                    "Lname": Lname,
                    "email": email,
                    "affiliate": affiliate,
                    "submission_time": submission_time,
                }
                insert_data(session, data)  # Insert into Snowflake
                st.success("User has been added")
            else:
                st.error("Please fill in all required fields.")

    def insert_data(session, data):
        """Insert form data into Snowflake"""
        try:
            insert_query = f"""
            INSERT INTO HC_GIRLS_INC.REFINED.USER_AFFILIATE_XREF
            (affiliate,affiliate_old, USERPRINCIPALNAME)
            VALUES (?, ?, ?)
            """
            # Use session.sql() method to execute the query
            session.sql(
                insert_query,
                params=(
                    data["affiliate"] , 
                    data["affiliate"] , 
                    data["email"]
                )
            ).collect()  # collect() runs the query in Snowflake
            st.success("Data inserted successfully")
        except Exception as e:
            st.error("Error inserting data into Snowflake: " + str(e))

    def display_results(session):
        """Display results from Snowflake"""
        try:
            query = "SELECT * FROM HC_GIRLS_INC.REFINED.USER_AFFILIATE_XREF ORDER BY submission_time DESC LIMIT 10"
            df = pd.read_sql(query, session)
            st.dataframe(df)
        except Exception as e:
            st.error("Error fetching results from Snowflake: " + str(e))

    # Display the survey form
    display_survey_form(session, datetime.timezone.utc)

    # Display recent submissions
    st.write("Recent Submissions")
    display_results(session)

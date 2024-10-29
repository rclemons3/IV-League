import streamlit as st
import datetime
import pandas as pd
from utilities import get_engagement_options, get_affiliate_options


def load_search_data(
    _session,
):
    """Gets the search results from the database based on the search query

    Args:
        `_session` (`Session`): the session object to use to connect to Snowflake
        
    Returns:
        `pd.dataframe`: a `dataframe` containing two columns:
            `AFFILIATE_ID`: the id of an affiliate
            `AFFILIATE_NAME`: the name of an affiliate
        """
    
    sql = """
            SELECT
                affiliate_id,
                affiliate_name,
                USERPRINCIPALNAME
                
            FROM 
            
        """

   
    try:
        event_df = session.sql(
            sql,
            params=(
                affiliate_id,
                affiliate_name,
            ),
        ).to_pandas()
    except Exception as e:
        print("No affiliates found ")
        print(e)


def display_affiliate_search(session, state_group):
    """Display the affiliate search section

    Args:
        session (Session): the session object used to interact with the database
        state_group (StateGroup): the StateGroup object used to reset the widgets.
    """

    # First, define session state variables we will need. These are defined here because they are only used in this file.
    # the search results to display
    if "affiliate_search_results" not in st.session_state.keys():
        st.session_state["affiliate_search_results"] = load_search_data(
            session,
        )

    # used to reset the search results' edit row, same as in search_section.py
    if "affiliate_results_key" not in st.session_state.keys():
        st.session_state["affiliate_results_key"] = 1
  

    # Render search results
    if len(st.session_state["affiliate_search_results"]) == 0:
        st.markdown("No affilaites found")
    else:
        st.markdown(
            f"Displaying **{len(st.session_state['affiliate_search_results'])}** affiliate{'' if len(st.session_state['affiliate_search_results']) == 1 else 's'}"
        )
        st.markdown(
            "*Click button on the left of a row to view affiliate information*\n\n*Hover over data for more options*"
        )

        





        # Get all affiliates (this is cached so its not a huge deal to overreach like this)
        affiliate_df = get_affiliate_options(session)
       
        

import streamlit as st
import pandas as pd
import datetime


# Runs a query to get the affiliate options users should be able to select and the associated affiliate_id
@st.cache_data()

def display_error_message(error, context):
    st.error(f"An error occurred while trying to {context}: {str(error)}")

def get_affiliate_options(session):
    # get our names with a sql statement
    try:
        affiliate_df = session.sql(
            "SELECT  FROM "
        )
        # the previous statement returned a Snowflake DataFrame, but Pandas is easier to work with, so get that instead
        affiliate_df = affiliate_df.to_pandas()
    except Exception as e:
        display_error_message(e, "fetch affiliate options")
        affiliate_df = pd.DataFrame(columns=["", ""])

    # For some reason the resulting list contains all of the data in a seemingly random order, so sort the list to make
    # sure the options appear in the same order every time
    return _df.sort_values(by=[""])


# Returns the posible engagement type options for the user to choose from.



def create_time_since_date_string(pre_date_message, datetime_utc, time_zone):
    time_since_logged = datetime.datetime.now(tz=datetime.timezone.utc) - datetime_utc
    if time_since_logged.days > 7:
        logged_string = f"{pre_date_message} {datetime.datetime.strftime(st.session_state['event_data']['DATE_LOGGED'].astimezone(time_zone),'%x, %I:%M %p',)}"
    else:
        logged_string = f"{pre_date_message} **"
        if time_since_logged.days > 0:
            logged_string += f"{time_since_logged.days} day{'' if time_since_logged.days == 1 else 's'} ago"
        elif time_since_logged.seconds > 3600:
            logged_string += f"{time_since_logged.seconds // 3600} hour{'' if time_since_logged.seconds // 3600 == 1 else 's'} ago"
        elif time_since_logged.seconds > 60:
            logged_string += f"{time_since_logged.seconds // 60} minute{'' if time_since_logged.seconds // 60  == 1 else 's'} ago"
        elif time_since_logged.seconds > 30:
            logged_string += f"{time_since_logged.seconds} second{'' if time_since_logged.seconds == 1 else 's'} ago"
        else:
            logged_string += "just now"
        logged_string += f"** ({datetime.datetime.strftime(datetime_utc.astimezone(time_zone),'%D, %I:%M %p')})"
    return logged_string


class StateGroup:
    def __init__(self, name, initial_items={}):
        self.name = name
        self._keys = []
        st.session_state[self.name] = 1

        for key, value in initial_items.items():
            self.set_value(key, value)

    def __str__(self):
        out = "{\n"
        for key in self._keys:
            out += f"{key} : {self.get_value(key)},\n"
        return out + "}"

    def get_key(self, key):
        str_key = f"{self.name}_{key}_{str(st.session_state[self.name])}"
        if str_key not in self._keys:
            self._keys.append(key)
        return str_key

    def get_value(self, key):
        return st.session_state[self.get_key(key)]

    def set_value(self, key, value):
        st.session_state[self.get_key(key)] = value

    def reset(self):
        st.session_state[self.name] += 1

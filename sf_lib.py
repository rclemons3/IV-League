from snowflake.snowpark import Session
import streamlit as st
from os import getenv
import json
from pathlib import Path


# so we don't have to keep making our connection object again and again and again and...
@st.cache_resource(ttl="3h59s")
def sf_conn():
    connection_parameters = {
       
    }


   


    #def is_docker():
     #   cgroup = Path('/proc/self/cgroup')
      #  return Path('/.dockerenv').is_file() or cgroup.is_file() and 'docker' in cgroup.read_text()

   # if is_docker():
    #    connection_parameters = {
     #    "account": ""
      #   "user": "",
      #   "role": ""
         #"warehouse":"",
         #"database": ""
      #     }
        #connection_parameters = json.loads(connection_str)
    #connection_parameters["password"] = getenv('DS_SNOWFLAKE_PASSWORD')
    
    #else:
     #   with open('/Users/rick.clemons/Girls/affiliate-engagement-app/creds.json') as f:
      #      connection_parameters = json.load(f)

    session = Session.builder.configs(connection_parameters).create()
    # print(session.connection.client_session_keep_alive)
    return session
#     conn = snowflake.connector.connect(user=connection_parameters["user"],
#                                        password=connection_parameters["password"],
#                                        account=connection_parameters["account"],
#                                        warehouse=connection_parameters["warehouse"],
#                                        database=connection_parameters["database"],
#                                        role=connection_parameters["role"]

#                                        )
#     return conn

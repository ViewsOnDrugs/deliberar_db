
import streamlit as st
import json
import streamlit_authenticator as stauth
from analysis_form import analysis_form
from user_form import user_form


# watch out for the incompatibility of bcrypt https://github.com/matrix-org/synapse/pull/2288
# https://github.com/matrix-org/synapse/issues/2345#issuecomment-314076318

# config = json.loads(st.secrets["auth"])
#
# authenticator = stauth.Authenticate(
#     config['credentials'],
#     config['cookie']['name'],
#     config['cookie']['key'],
#     config['cookie']['expiry_days'],
#     config['preauthorized']
# )
username = "admin_deliberar"
# name, authentication_status, username = authenticator.login('Login', 'main')
#
# if authentication_status:
#     authenticator.logout('Logout', 'main')
#
#     user_form(username)
#
# elif authentication_status == False:
#     st.warning('Please enter your username and password')
#
# elif authentication_status == None:
#     st.error('Username/password is incorrect')


user_form(username)

# st.sidebar.markdown("# Main page")

import streamlit as st
import json
import streamlit_authenticator as stauth
from news_form import news_form

st.set_page_config(layout="wide")
# watch out for the incompatibility of bcrypt https://github.com/matrix-org/synapse/pull/2288
# https://github.com/matrix-org/synapse/issues/2345#issuecomment-314076318

config = json.loads(st.secrets["auth"])

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

h1, h2 = st.columns(2)
with h1:
    st.header(f"Begleitfragebogen zur Substanzprobenanalyse")


with h2:
    head1 = f' [<img src="https://pad.gwdg.de/uploads/5ee8c971-ba67-467f-9dab-03e08cd6b9a1.png" alt="drawing" width="250"/>](https://www.ift.de/)'
    st.markdown(head1, unsafe_allow_html=True)

name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    authenticator.logout('Logout', 'main')

    news_form(username)

elif  authentication_status == False:
    st.warning('Please enter your username and password')
elif authentication_status == None:
    st.error('Username/password is incorrect')


# st.sidebar.markdown("# Main page")
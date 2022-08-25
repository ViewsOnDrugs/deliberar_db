import streamlit as st
from .tedi import tedi_form


def main_form(username):

    if st.button('main form'):
        tedi_form(username)
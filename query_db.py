import pandas as pd
import json
import streamlit as st

try:
    with open("local_db.json", "r") as jsf:
        json_data = json.load(jsf)
except (json.decoder.JSONDecodeError, FileNotFoundError):
    st.write("No DB found")


def return_db():
    db_full = pd.DataFrame.from_dict(json_data).T
    st.dataframe(db_full)
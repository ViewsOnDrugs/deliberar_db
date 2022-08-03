import pandas as pd
import json
import streamlit as st
from google.cloud import firestore
from google.oauth2 import service_account

# Authenticate to Firestore with the JSON account key.

key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds, project="substances-db")


try:
    with open("local_db.json", "r") as jsf:
        json_data = json.load(jsf)
except (json.decoder.JSONDecodeError, FileNotFoundError):
    st.write("No DB found")


def return_db(online=True):
    if online:
        # And then render each post, using some light Markdown
        posts_ref = db.collection("substances")
        dict_to_df = {}
        for doc in posts_ref.stream():
            post = doc.to_dict()
            dict_to_df[post["sample_uid"]] = post
        db_full = pd.DataFrame.from_dict(dict_to_df).T
        st.dataframe(db_full)
    else:
        db_full = pd.DataFrame.from_dict(json_data).T
        st.dataframe(db_full)
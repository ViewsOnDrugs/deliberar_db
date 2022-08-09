import pandas as pd
import json
import requests
import streamlit as st
from google.cloud import firestore
from google.oauth2 import service_account

# Authenticate to Firestore with the JSON account key.

key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds, project="substances-db")

# Load TEDI guidelines
with open(
        "guides.json") as jsd:
    GUIDELINES = json.load(jsd)

# check for internet connection
def internet_online(url='https://elespectador.com', timeout=5):
    """

    :param url: test url
    :param timeout: timeout
    :return:
    """

    try:
        _ = requests.head(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        return False


def load_db():

    try:
        with open("local_db.json", "r") as jsf:
            json_data = json.load(jsf)
    except (json.decoder.JSONDecodeError, FileNotFoundError):
        with open("local_db.json", "w") as ldb:
            json_data = {}
            json.dump(json_data, ldb, indent=4)
    return json_data

def return_db(online=True):
    """

    :param online:
    :return:
    """
    if internet_online():
        # And then render each post, using some light Markdown
        posts_ref = db.collection("substances")
        dict_to_df = {}
        for doc in posts_ref.stream():
            post = doc.to_dict()
            dict_to_df[post["sample_uid"]] = post
        db_full = pd.DataFrame.from_dict(dict_to_df).T
        st.dataframe(db_full)
    else:
        db_json = load_db()

        db_full = pd.DataFrame.from_dict(db_json).T
        st.dataframe(db_full)


def post_to_db (dict_in, sample_id):
    """

    :param dict_in:
    :param sample_id:
    :return:
    """

    if internet_online():
        # Create a reference to the Google post.
        doc_ref = db.collection("substances").document(sample_id)
        doc_ref.set(dict_in[sample_id])
        st.text(F"Sample {sample_id} was successfully submitted")

    else:

        db_json = load_db()

        if sample_id in db_json:
            st.warning(f" ""Sample {sample_id} exists in the database,"
"to override/update the values use the Update button below""")
        else:
            db_json[sample_id] = dict_in[sample_id]
            with open("local_db.json", "w") as ldb:
                json.dump(db_json, ldb, indent=4)

        queried_substance_1 = dict_in[sample_id]["substance_1"]
        queried_alert = dict_in[sample_id]["alert"]

        st.subheader(f"Post: {queried_substance_1}")
        st.write(f"Alert: {queried_alert}")


def update_db():

    db_json = load_db()

    with st.form("Update"):

        st.markdown("# Update db")

        sample_id_list = [x for x in db_json]
        id_update = st.selectbox("select id to be updated", sample_id_list)

        result_update = st.text_input(f"Update {id_update} substance_1 result: ")
        submit2 = st.form_submit_button("Update")

        if submit2:

            st.text("[ronts")

            if result_update:
                db_json[id_update]["substance_1"] = result_update

                st.text(f"{result_update}, {db_json[id_update]}")
                with open("local_db.json", "w") as ldb:
                    json.dump(db_json, ldb, indent=4)

                st.success(f"{id_update} > {result_update} updated!")
            else:
                st.error(f"{id_update} no result provided")


import streamlit as st
from google.cloud import firestore
import uuid
import pycountry
from google.oauth2 import service_account
import json
import requests
from query_db import return_db
import os
from PIL import Image


country_list = [c.name for c in pycountry.countries]
country_list.insert(0, country_list.pop(country_list.index("Germany")))


# Authenticate to Firestore with the JSON account key.

key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds, project="substances-db")

# Load TEDI guidelines
with open(
        "guides.json") as jsd:
    GUIDELINES = json.load(jsd)

test_list = GUIDELINES["test_method"]["VOCABULARY"]
required_fields = [x for x in GUIDELINES if GUIDELINES[x]["REQUIREMENT_LEVEL"] == 'required']

sample_id_pre = str(uuid.uuid4())[:8]

def load_image(image_file):
    img = Image.open(image_file)
    return img

def internet_online(url='https://elespectador.com', timeout=5):

    try:
        _ = requests.head(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        return False


def post_to_db (dict_in, sample_id):
    """

    :param dict_in:
    :param sample_uid:
    :return:
    """

    if internet_online():
        # Create a reference to the Google post.
        doc_ref = db.collection("substances").document(sample_id)
        doc_ref.set(dict_in[sample_id])
        st.text(F"Sample {sample_id} was successfully submitted")
        # And then render each post, using some light Markdown
        posts_ref = db.collection("substances")
        for doc in posts_ref.stream():
            post = doc.to_dict()
            queried_substance_1 = post["substance_1"]
            queried_alert = post["alert"]

            st.subheader(f"Posted: {queried_substance_1}")
            st.write(f"Alert: {post}")
    else:
        try:
            with open("local_db.json", "r") as jsf:
                json_data = json.load(jsf)
        except (json.decoder.JSONDecodeError, FileNotFoundError):
            with open("local_db.json", "w") as ldb:
                json_data = {}
                json.dump(json_data, ldb, indent=4)

        if sample_id in json_data:
            st.warning(f" Sample {sample_id} exists in the database, do you want to override/update the values?")
            choice_db = st.selectbox("", ["cancel", "update", "override"])
            if choice_db == 'cancel':
                st.text("db won't be changed")
            else:
                st.text("db will be overwritten")

                json_data[sample_id] = dict_in[sample_id]

                with open("local_db.json", "w") as ldb:
                    json.dump(json_data, ldb, indent=4)

        else:
            json_data[sample_id] = dict_in[sample_id]

        with open("local_db.json", "w") as ldb:
            json.dump(json_data, ldb, indent=4)

        queried_substance_1 = dict_in[sample_id]["substance_1"]
        queried_alert = dict_in[sample_id]["alert"]

        st.subheader(f"Post: {queried_substance_1}")
        st.write(f"Alert: {queried_alert}")


# Streamlit widgets to let user create a new post

h1, h2, h3 = st.columns(3)
with h1:
    st.header("Substance Submission Form")

with h2:
    head1 = f' [<img src="https://i2.wp.com/reverdeser.org/wp-content/uploads/2017/07/paschido.png?fit=520%2C431" alt="drawing" width="150"/>](http://reverdeser.org/inicio-a/programa-de-analisis-de-sustancias/)'
    head_alt =  '[<img src="https://vivid-hamburg.de/wp-content/uploads/2020/05/logo_lang.jpg"  style="object-fit:cover; object-position: center; width:200px; height:125px; border: solid 1px #CCC"/>](https://vivid-hamburg.de/)'
    st.markdown(head_alt, unsafe_allow_html=True)

with h3:
    head1 = f' [<img src="https://www.tedinetwork.org/wp-content/uploads/2022/02/TEDI_logo.jpg" alt="drawing" width="150"/>](https://www.tedinetwork.org/)'
    st.markdown(head1, unsafe_allow_html=True)

with st.form("Sample Form"):

    col1, col2 = st.columns(2)

    with col1:
        date = str(st.date_input(GUIDELINES["date"]["VARIABLE_NAME"], key="1"))
        organisation = st.selectbox(GUIDELINES["organisation"]["VARIABLE_NAME"], options=["VIVID", "Deliberar"])
        country = st.selectbox(GUIDELINES["country"]["VARIABLE_NAME"], options=country_list, key="4")
        city = st.text_input( GUIDELINES["city"]["VARIABLE_NAME"] , key=" 5")
        sold_as = st.text_input(GUIDELINES["sold_as"]["VARIABLE_NAME"] , key="8")
        sample_form = st.text_input(GUIDELINES["sample_form"]["VARIABLE_NAME"] , key="11")
        colour = st.text_input(GUIDELINES["colour"]["VARIABLE_NAME"], key="12")
        geo_context = st.text_area(GUIDELINES["geo_context"]["VARIABLE_NAME"], key="6")
        provider_relation = st.text_area(GUIDELINES["provider_relation"]["VARIABLE_NAME"], key=" 7")
        alias = st.text_input(GUIDELINES["alias"]["VARIABLE_NAME"], key="9")
        used_prior = st.checkbox(GUIDELINES["used_prior"]["VARIABLE_NAME"], key="10")
        logo = st.text_input(GUIDELINES["logo"]["VARIABLE_NAME"], key="13")
        st.markdown("##### (*) Required Field")
        st.info(f"### Sample id: `{sample_id_pre}`")
        sample_uid = st.text_input(GUIDELINES["sample_uid"]["VARIABLE_NAME"] , key="11")

    with col2:

        width = st.number_input(GUIDELINES["width"]["VARIABLE_NAME"], key="14")
        thickness = st.number_input(GUIDELINES["thickness"]["VARIABLE_NAME"], key="15")
        height = st.number_input(GUIDELINES["height"]["VARIABLE_NAME"], key="16")
        weight = st.number_input(GUIDELINES["weight"]["VARIABLE_NAME"], key="17")
        unit_price = st.number_input(GUIDELINES["unit_price"]["VARIABLE_NAME"])
        price_currency = st.text_input(GUIDELINES["price_currency"]["VARIABLE_NAME"], key="18")
        gender = st.selectbox(GUIDELINES["gender"]["VARIABLE_NAME"], options=GUIDELINES["gender"]["VOCABULARY"], key="19")
        age = st.number_input(GUIDELINES["age"]["VARIABLE_NAME"], key="20")
        test_method = st.selectbox(GUIDELINES["test_method"]["VARIABLE_NAME"], options=GUIDELINES["test_method"]["VOCABULARY"], key="21")
        service_type = st.text_input(GUIDELINES["service_type"]["VARIABLE_NAME"], key="22")
        substance_1 = st.text_input(GUIDELINES["substance_1"]["VARIABLE_NAME"] , key="23")
        subs1_quant = st.text_input(GUIDELINES["subs1_quant"]["VARIABLE_NAME"], key="24")
        subs1_unit = st.text_input(GUIDELINES["subs1_unit"]["VARIABLE_NAME"], key="25")
        substance_9 = st.text_input(GUIDELINES["substance_9"]["VARIABLE_NAME"], key="26")
        subs9_quant = st.text_input(GUIDELINES["subs9_quant"]["VARIABLE_NAME"], key="27")
        subs9_unit = st.text_input(GUIDELINES["subs9_unit"]["VARIABLE_NAME"], key="28")
        alert = st.checkbox("Check if an alert was issued", key="29")

    submit = st.form_submit_button("Submit sample")

    dic_set = {
        sample_uid: {"date": date, "organisation": organisation, "sample_uid": sample_uid,
                     "country": country, "city": city, "geo_context": geo_context, "relationship": provider_relation,
                     "sold_as": sold_as, "alias": alias, "used_prior": used_prior, "sample_form": sample_form,
                     "colour": colour, "logo": logo, "width": width, "thickness": thickness, "height": height,
                     "weight": weight, "unit_price": unit_price, "gender": gender, "age": age,
                     "test_method": test_method, "service_type": service_type, "substance_1": substance_1,
                     "subs1_quant": subs1_quant, "subs1_unit": subs1_unit, "substance_9": substance_9,
                     "subs9_quant": subs9_quant, "subs9_unit": subs9_unit, "alert": alert}
               }

    if submit:
        if sample_uid and organisation and sample_form:

            # Once the user has submitted, upload it to the database
            if not substance_1:
                post_to_db(dic_set, sample_uid)

            else:
                post_to_db(dic_set, sample_uid)

        else:

            missing_fields = [x for x in dic_set[sample_uid] if x in required_fields if not dic_set[sample_uid][x] if x != "alert"]
            # missing_fields = [c for c in [sample_uid and organisation and sample_form and substance_1] if c in required_fields]
            st.warning(f"Missing required fields for submission: \n {missing_fields}")

st.markdown("##")
st.subheader("Upload Image")
image_file = st.file_uploader("Upload Images", type=["png", "jpg", "jpeg"])
if image_file:
    if st.button("Confirm upload image"):
        pic_pil = load_image(image_file)
        pic_ext = image_file.type.split("/")[1]
        pic_pil.save(os.path.join("images_db", f"{sample_uid}.PNG"))
        st.success(f"Image `{sample_uid}.{pic_ext}` saved")
st.markdown("##")

if st.button("Show DB"):
    return_db()


# # Then get the data at that reference.
# doc = doc_ref.get()
#
# # Let's see what we got!
# st.write("The id is: ", doc.id)
# st.write("The contents are: ", doc.to_dict())

import streamlit as st
from google.cloud import firestore
import uuid
import pycountry

country_list = [c.name for c in pycountry.countries]


# cred = credentials.Certificate("/Users/fran/substances-db-firebase-adminsdk-wvxtn-6ac075e333.json")
# firebase_admin.initialize_app(cred)

# Authenticate to Firestore with the JSON account key.
db = firestore.Client.from_service_account_json("/Users/fran/substances-db-firebase-adminsdk-wvxtn-6ac075e333.json")

test_list = ["ANTIBODY TEST STRIPS",
             "REAGENT TESTING",
             "TLC",
             "UV SPECTROSCOPY",
             "FTIR/ RAMAN",
             "(U)HPLC-UV",
             "(U)HPLC-MS ",
             "GC-MS",
             "DIRECT MS",
             "LC-HRMS", ]


with st.form("sample_form"):

    sample_id = str(uuid.uuid4())[:8]

    # Streamlit widgets to let a user create a new post

    h1, h2, h3 = st.columns(3)
    with h1:
        st.header("Substance Submission Form")

    with h2:
        head1 = f' [<img src="https://i2.wp.com/reverdeser.org/wp-content/uploads/2017/07/paschido.png?fit=520%2C431" alt="drawing" width="150"/>](http://reverdeser.org/inicio-a/programa-de-analisis-de-sustancias/)'
        st.markdown(head1, unsafe_allow_html=True)

    with h3:
        head1 = f' [<img src="https://www.tedinetwork.org/wp-content/uploads/2022/02/TEDI_logo.jpg" alt="drawing" width="150"/>](https://www.tedinetwork.org/)'
        st.markdown(head1, unsafe_allow_html=True)



    col1, col2 = st.columns(2)

    with col1:
        st.info(f"## Sample_id: `{sample_id}`")
        date = str(st.date_input("Date", key="1 "))
        Organisation = st.selectbox("Organisation", options=["VIVID", "Deliberar"])
        Country = st.selectbox("Country", options=country_list, key=" 4 ")
        City = st.text_input("City", key="  5")
        geo_context = st.text_area("geo_context", key=" 6 ")
        Relationship_prov = st.text_area("Relationship_prov", key="  7")
        Sold_as = st.text_input("Sold_as", key=" 8 ")
        alias = st.text_input("alias ", key=" 9")
        used_prior = st.text_input("used_prior", key=" 10")
        Sample_form = st.text_input("Sample_form", key="11 ")
        Colour = st.text_input("Colour", key=" 12")
        Logo = st.text_input("Logo", key=" 13")

    with col2:

        width = st.number_input("width", key=" 14")
        thickness = st.number_input("thickness", key=" 15")
        Height = st.number_input("Height", key=" 16")
        Weight = st.number_input("Weight", key=" 17")
        unit_price = st.text_input("unit_price", key=" 18")
        Gender = st.selectbox("Gender", options=["M", "F", "NB"], key=" 19")
        Age = st.number_input("Age", key=" 20")
        test_method = st.selectbox("test_method", options=test_list, key=" 21")
        service_type = st.text_input("service_type", key=" 22")
        Substance_1 = st.text_input("Substance_1", key=" 23")
        Subst1_Quant = st.text_input("Subst1_Quant", key="24 ")
        Subst1_Unit = st.text_input("Subst1_Unit", key=" 25")
        Substance_9 = st.text_input("Substance_9", key=" 26")
        Subst9_Quant = st.text_input("Subst9_Quant", key=" 27")
        Subst9_Unit = st.text_input("Subst9_Unit", key=" 28")
        Alert = st.checkbox("Check if an Alert was emitted", key="29 ")


    st.subheader("Image")
    image_file = st.file_uploader("Upload Images", type=["png", "jpg", "jpeg"])
    st.markdown("## ")

    submit = st.form_submit_button("Submit sample")


    dic_set = {"Date (yyyy-mm-dd)": date,
    "Organisation": Organisation,
    "Sample UID": sample_id,
    "Country*": Country,
    "City*": City,
    "Geography/Context (where sample was purchased)": geo_context,
    "Relationship with provider": Relationship_prov,
    "Sold-As*": Sold_as,
    "Alias (optional)": alias,
    "Sample used prior to test": used_prior,
    "Sample Form*": Sample_form,
    "Colour": Colour,
    "Logo": Logo,
    "Width (mm)": width,
    "Thickness (mm)": thickness,
    "Height (mm)": Height,
    "Weight (mg)": Weight,
    "Price per unit (EUR)": unit_price,
    "Gender": Gender,
    "Age": Age,
    "Test Method": test_method,
    "Service Type" : service_type,
    "Substance-1": Substance_1,
    "Subst1-Quant": Subst1_Quant,
    "Subst1-Unit": Subst1_Unit,
    "Substance-9": Substance_9,
    "Subst9-Quant": Subst9_Quant,
    "Subst9-Unit": Subst9_Unit,
    "Alert": Alert}

    if submit:
        # Once the user has submitted, upload it to the database
        if sample_id and Organisation and Sample_form and Substance_1:
            # Create a reference to the Google post.
            doc_ref = db.collection("substances").document(dic_set["Sample UID"])
            doc_ref.set(dic_set)
            st.text("Sample {sample_id} was successfully submitted")
            # And then render each post, using some light Markdown
            posts_ref = db.collection("substances")
            for doc in posts_ref.stream():
                post = doc.to_dict()
                substance_1 = post["Substance-1"]
                alert = post["Alert"]

                st.subheader(f"Post: {substance_1}")
                st.write(f"{alert}")

        else:
            st.text("Missing required fields for submission: Sample_id, Organisation, Sample_form or Substance_1")


# # Then get the data at that reference.
# doc = doc_ref.get()
#
# # Let's see what we got!
# st.write("The id is: ", doc.id)
# st.write("The contents are: ", doc.to_dict())
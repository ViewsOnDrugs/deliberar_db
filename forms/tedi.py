
import streamlit as st
import uuid
import pycountry
import json
from query_db import return_db, post_to_db, update_db
import os
from PIL import Image
from lib.orga_lib import load_orga_lib



orga_dict = load_orga_lib()


def load_image(image_file):
    img = Image.open(image_file)
    return img


def tedi_form(username):

    lang_main = orga_dict[username]["lan"]

    # Load TEDI guidelines
    with open(f"lan/{lang_main}.json", "r") as jsd:
        GUIDELINES = json.load(jsd)

    interface_dic = GUIDELINES['_interface']

    required_fields = [x for x in GUIDELINES if GUIDELINES[x]["REQUIREMENT_LEVEL"] == 'required']

    country_list = [c.name for c in pycountry.countries]

    country_list.insert(0, country_list.pop(country_list.index(orga_dict[username]['country_first'])))

    # Streamlit widgets to let user create a new post

    h1, h2, h3 = st.columns(3)
    with h1:
        st.header(f" {interface_dic['form_tittle']}")

    with h2:
        head_0 = orga_dict[username]['head']
        st.markdown(head_0, unsafe_allow_html=True)

    with h3:
        head1 = f' [<img src="https://www.tedinetwork.org/wp-content/uploads/2022/02/TEDI_logo.jpg" alt="drawing" width="150"/>](https://www.tedinetwork.org/)'
        st.markdown(head1, unsafe_allow_html=True)

    with st.form("Sample Form"):
        sample_id_pre = str(uuid.uuid4())[:8]

        col1, col2 = st.columns(2)

        with col1:
            date = str(st.date_input(GUIDELINES["date"]["VARIABLE_NAME"], key="1"))
            organisation = interface_dic['organization']
            st.markdown(f"##### {organisation}")
            st.markdown(f"#### {orga_dict[username]['name']}")
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
            st.info(f"### {interface_dic['sample_id']}: {sample_id_pre}")
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
            alert = st.checkbox(GUIDELINES['alert']["DESCRIPTION"], key="29")

        st.markdown(f"##### {interface_dic['req_field']}")
        submit = st.form_submit_button(f" {interface_dic['submit_samp']}")

        dic_set = {
            sample_uid: {"date": date, "organisation": str(organisation), "sample_uid": sample_uid,
                         "country": country, "city": city, "geo_context": geo_context, "relationship": provider_relation,
                         "sold_as": sold_as, "alias": alias, "used_prior": used_prior, "sample_form": sample_form,
                         "colour": colour, "logo": logo, "width": width, "thickness": thickness, "height": height,
                         "weight": weight, "unit_price": unit_price, "gender": gender, "age": age,
                         "test_method": test_method, "service_type": service_type, "substance_1": substance_1,
                         "subs1_quant": subs1_quant, "subs1_unit": subs1_unit, "substance_9": substance_9,
                         "subs9_quant": subs9_quant, "subs9_unit": subs9_unit, "alert": alert}
                   }

        if submit:

            st.text(f"{sample_uid}, {str(organisation)}, {sample_form}")

            if sample_uid and organisation and sample_form:

                # Once the user has submitted, upload it to the database
                if not substance_1:
                    st.warning(f"{sample_uid} {interface_dic['warning']}")
                    post_to_db(dic_set, sample_uid)

                else:
                    post_to_db(dic_set, sample_uid)

            else:

                missing_fields = [x for x in dic_set[sample_uid] if x in required_fields if not dic_set[sample_uid][x] if x != "alert"]
                # missing_fields = [c for c in [sample_uid and organisation and sample_form and substance_1] if c in required_fields]
                st.warning(f"{interface_dic['warning_req_fields']} \n {missing_fields}")

    st.markdown("##")
    st.subheader(interface_dic['upload_img'])
    image_file = st.file_uploader("Upload Images", type=["png", "jpg", "jpeg"])
    if image_file:
        if st.button(interface_dic['confirm_upload']):
            pic_pil = load_image(image_file)
            pic_ext = image_file.type.split("/")[1]
            pic_pil.save(os.path.join("../images_db", f"{sample_uid}.PNG"))
            st.success(f" {interface_dic['saved_img']} `{sample_uid}.{pic_ext}`")
    st.markdown("##")

    if st.button(interface_dic['show_db']):
        return_db()

    update_db()

    # # Then get the data at that reference.
    # doc = doc_ref.get()
    #
    # # Let's see what we got!
    # st.write("The id is: ", doc.id)
    # st.write("The contents are: ", doc.to_dict())
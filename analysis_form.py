import streamlit as st
import uuid
import pycountry
from query_db import return_db, post_to_db, update_db
import os
from PIL import Image
from lib.orga_lib import load_orga_lib
from lan.load_lan import load_lan


orga_dict = load_orga_lib()


def load_image(image_file):
    img = Image.open(image_file)
    return img


def analysis_form(username):

    lang_main = orga_dict[username]["lan"]

    # Load TEDI guidelines
    GUIDELINES = load_lan(lang_main)

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
            st.markdown(f"##### {interface_dic['organization']}")
            width = st.number_input(GUIDELINES["width"]["VARIABLE_NAME"], key="14")
            thickness = st.number_input(GUIDELINES["thickness"]["VARIABLE_NAME"], key="15")
            height = st.number_input(GUIDELINES["height"]["VARIABLE_NAME"], key="16")
            weight = st.number_input(GUIDELINES["weight"]["VARIABLE_NAME"], key="17")
            test_method = st.selectbox(GUIDELINES["test_method"]["VARIABLE_NAME"], options=GUIDELINES["test_method"]["VOCABULARY"], key="21")
            service_type = st.text_input(GUIDELINES["service_type"]["VARIABLE_NAME"], key="22")
            substance_1 = st.text_input(GUIDELINES["substance_1"]["VARIABLE_NAME"] , key="23")
            subs1_quant = st.text_input(GUIDELINES["subs1_quant"]["VARIABLE_NAME"], key="24")

        with col2:

            subs1_unit = st.text_input(GUIDELINES["subs1_unit"]["VARIABLE_NAME"], key="25")
            substance_9 = st.text_input(GUIDELINES["substance_9"]["VARIABLE_NAME"], key="26")
            subs9_quant = st.text_input(GUIDELINES["subs9_quant"]["VARIABLE_NAME"], key="27")
            subs9_unit = st.text_input(GUIDELINES["subs9_unit"]["VARIABLE_NAME"], key="28")
            alert = st.checkbox(GUIDELINES['alert']["DESCRIPTION"], key="29")

        st.markdown(f"##### {interface_dic['req_field']}")
        submit = st.form_submit_button(f" {interface_dic['submit_samp']}")

        dic_set = {
            sample_uid: {"organisation": orga_dict[username]['name'], "sample_uid": sample_uid,
                          "width": width, "thickness": thickness, "height": height,
                         "weight": weight,
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
    image_file = st.file_uploader(interface_dic['upload_img'], type=["png", "jpg", "jpeg"])
    if image_file:
        if st.button(interface_dic['confirm_upload']):
            pic_pil = load_image(image_file)
            pic_ext = image_file.type.split("/")[1]
            pic_pil.save(os.path.join("../images_db", f"{sample_uid}.PNG"))
            st.success(f" {interface_dic['saved_img']} `{sample_uid}.{pic_ext}`")
    st.markdown("##")

    if st.button(interface_dic['show_db']):

        st.dataframe(return_db()[1])

    update_db(interface_dic)

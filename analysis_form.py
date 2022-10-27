import streamlit as st
import pycountry
from query_db import return_db, post_to_db
import os
from PIL import Image
from lib.orga_lib import load_orga_lib
from lan.load_specs import load_specs


orga_dict = load_orga_lib()

def load_image(image_file):
    img = Image.open(image_file)
    return img

current_db = return_db()[0]
entered_id_s = [x for x in current_db if 'substance_1' in current_db[x]]

def analysis_form(username):

    lang_main = orga_dict[username]["lan"]

    # Load TEDI guidelines
    lang_main = orga_dict[username]["lan"]
    interface_dic = load_specs(lang_main, "interface")['_interface']
    core_guidelines = load_specs(lang_main, "specs")["TEDI"]
    deliberar_guidelines = load_specs(lang_main, "specs")['DELIBERAR']

    required_core_fields = [x for x in core_guidelines if core_guidelines[x]["REQUIREMENT_LEVEL"] == 'required']
    required_deliberar_fields = [x for x in deliberar_guidelines if deliberar_guidelines[x]["REQUIREMENT_LEVEL"] == 'required']

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

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"##### {interface_dic['organization']}")

            analysis_update={

            "place_holder_sample_uid": st.empty(),
            "width": st.number_input(core_guidelines["width"]["VARIABLE_NAME"]),
            "thickness": st.number_input(core_guidelines["thickness"]["VARIABLE_NAME"]),
            "height": st.number_input(core_guidelines["height"]["VARIABLE_NAME"]),
            "weight": st.number_input(core_guidelines["weight"]["VARIABLE_NAME"]),
            "test_method": st.selectbox(core_guidelines["test_method"]["VARIABLE_NAME"],
                                       options=core_guidelines["test_method"]["VOCABULARY"]),
            "service_type": st.selectbox(core_guidelines["service_type"]["VARIABLE_NAME"],
                                         options=core_guidelines["service_type"]["VOCABULARY"]),
            "substance_1": st.selectbox(core_guidelines["substance_1"]["VARIABLE_NAME"],
                                                   options=core_guidelines["substance_1"]["VOCABULARY"]),
            "subs1_quant": st.text_input(core_guidelines["subs1_quant"]["VARIABLE_NAME"], key="24")
            }

        with col2:

            analysis_update = analysis_update | {
            "subs1_unit":  st.text_input(core_guidelines["subs1_unit"]["VARIABLE_NAME"], key="25"),
            "substance_9":  st.text_input(core_guidelines["substance_9"]["VARIABLE_NAME"], key="26"),
            "subs9_quant":  st.text_input(core_guidelines["subs9_quant"]["VARIABLE_NAME"], key="27"),
            "subs9_unit":  st.text_input(core_guidelines["subs9_unit"]["VARIABLE_NAME"], key="28"),
            "alert":  st.checkbox(core_guidelines['alert']["DESCRIPTION"])
            }

        st.markdown(f"##### {interface_dic['req_field']}")
        submit = st.form_submit_button(f" {interface_dic['submit_samp']}")

    with analysis_update["place_holder_sample_uid"]:
        sample_uid = st.selectbox("ID de la muestra", options=entered_id_s)
        analysis_update["sample_uid"] = sample_uid

    updated_dict = {x: (analysis_update[x] if x in analysis_update else current_db[sample_uid][x]) for x in current_db[sample_uid]}

    # import pandas as pd
    # st.dataframe(pd.DataFrame.from_dict(analysis_update).T)

    if submit:

        dic_set = {
            updated_dict["sample_uid"]: updated_dict}

        st.text(f"{analysis_update['sample_uid']}, {analysis_update['substance_1']}")

        if analysis_update['sample_uid'] and analysis_update['substance_1']:

            post_to_db(dic_set, analysis_update['sample_uid'])
            st.success(dic_set)

        else:

            missing_fields = [x for x in analysis_update['sample_uid'] if x in required_core_fields if not analysis_update['sample_uid'][x] if x != "alert"]
            # missing_fields = [c for c in [sample_uid and organisation and sample_form and substance_1] if c in required_fields]
            st.warning(f"{interface_dic['warning_req_fields']} \n {missing_fields}")

    st.markdown("##")
    st.subheader(interface_dic['upload_img'])
    image_file = st.file_uploader(interface_dic['upload_img'], type=["png", "jpg", "jpeg"])
    if image_file:
        if st.button(interface_dic['confirm_upload']):
            pic_pil = load_image(image_file)
            pic_ext = image_file.type.split("/")[1]
            pic_pil.save(os.path.join("../images_db", f"{analysis_update['sample_uid']}.PNG"))
            st.success(f" {interface_dic['saved_img']} `{analysis_update['sample_uid']}.{pic_ext}`")
    st.markdown("##")

    if st.button(interface_dic['show_db']):

        st.dataframe(return_db()[1])

    # update_db(interface_dic)

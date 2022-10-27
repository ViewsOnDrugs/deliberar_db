
import streamlit as st
import uuid
from query_db import post_to_db, return_db, analysis_init, update_db
import os
import geonamescache
from PIL import Image
from lib.orga_lib import load_orga_lib
from lan.load_specs import load_specs


def load_image(image_file):
    img = Image.open(image_file)
    return img

@st.experimental_memo
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

orga_dict = load_orga_lib()
gc = geonamescache.GeonamesCache()
cities_all=gc.get_cities()

# don't allow to send a sample without this variables:
compulsory_data= ['organisation', 'date', 'city', 'sample_form', 'sold_as', 'reasons_dc_visit']

def render_other(dict_out, place_holders,  var_name, guidelines, interface_dict, key_numb):
    with dict_out[place_holders[0]]:

        dict_out[var_name[0]] = st.selectbox(guidelines[var_name[0]]["VARIABLE_NAME"], options=guidelines[var_name[0]]["VOCABULARY"], key=key_numb)

    if len(var_name) == 1:
        with dict_out[place_holders[1]]:
            if interface_dict["other"] in dict_out[var_name[0]] or "und zwar" in dict_out[var_name[0]]:
                dict_out[var_name[0]] = st.text_input(f"{dict_out[var_name[0]]}:", key=key_numb)

    elif len(var_name) == 2:
        with dict_out[place_holders[1]]:
            if dict_out[var_name[0]] == interface_dict["yes_trigger"]:
                dict_out[var_name[1]] = st.multiselect(guidelines[var_name[1]]["VARIABLE_NAME"],
                                                        options=guidelines[var_name[1]]["VOCABULARY"])
                with dict_out[place_holders[2]]:
                    if interface_dict["other"] in dict_out[var_name[1]]:
                        dict_out[var_name[1]] += [
                            st.text_input(f"{interface_dict['other_option']} {guidelines[var_name[1]]['VARIABLE_NAME']}")]


def news_form(username):

    # Load TEDI guidelines
    lang_main = orga_dict[username]["lan"]
    interface_dic = load_specs(lang_main, "interface")['_interface']
    core_guidelines = load_specs(lang_main, "specs")["TEDI"]
    news_guidelines = load_specs(lang_main, "specs")['NEWS']

    collection_name = f"NEWS_{orga_dict[username]['name']}"

    # Streamlit widgets to let user create a new post

    h1, h2,  = st.columns(2)
    with h1:
        head1 = f' [<img src="https://pad.gwdg.de/uploads/8c4a40cd-8e23-4cac-aec1-0ae649872df4.png" alt="drawing" width="350"/>](https://mindzone.info/news/)'
        st.markdown(head1, unsafe_allow_html=True)

    with h2:
        head_0 = orga_dict[username]['head']
        st.markdown(head_0, unsafe_allow_html=True)


    with st.form("Sample Form"):

        col1, col2 = st.columns(2)

        with col1:
            # TEDI fields

            tedi_fieds_1 = {"organisation": orga_dict[username]['name'],
                           "date":  str(st.date_input(core_guidelines["date"]["VARIABLE_NAME"])),
                           "placeholder_city": st.empty(),
                           "alias": st.text_input(core_guidelines["alias"]["VARIABLE_NAME"], key="9"),
                            "placeholder_sold_as": st.empty(),
                            "placeholder_other_sold_as": st.empty(),
                            "placeholder_sample_form": st.empty(),
                            "placeholder_other_sample_form": st.empty(),
                            "colour": st.color_picker(core_guidelines["colour"]["VARIABLE_NAME"], key="12"),
                           }

        with col2:
            news_fields = {
                "placeholder_reasons_dc_visit": st.empty(),
                "placeholder_other_reasons_dc_visit": st.empty(),
                "use_frequency": st.selectbox(news_guidelines["use_frequency"]["VARIABLE_NAME"],
                                              options=news_guidelines["use_frequency"]["VOCABULARY"]),
                "placeholder_effect_unexp": st.empty(),
                "placeholder_list_effect_unexp": st.empty(),
                "placeholder_other_effect_unexp": st.empty(),

            }
            tedi_fieds_2 = {"unit_price": st.number_input(core_guidelines["unit_price"]["VARIABLE_NAME"]),
                            "placeholder_price_currency": st.empty(),
                            "placeholder_other_price_currency": st.empty(),
                            "placeholder_unit_substance": st.empty(),
                           "placeholder_other_unit_substance": st.empty(),
                            "placeholder_provider_relation": st.empty(),
                            "placeholder_other_provider_relation": st.empty()
                            }

        st.markdown(f"##### {interface_dic['req_field']}")
        submit = st.form_submit_button(f" {interface_dic['submit_form']}")

    tedi_fieds_1["country"] ='DE'
    with tedi_fieds_1["placeholder_city"]:
        country_cities = [""]+[cities_all[x]['name'] for x in cities_all if
                          cities_all[x]['countrycode'] == tedi_fieds_1["country"]]
        tedi_fieds_1["city"] = st.selectbox(core_guidelines["city"]["VARIABLE_NAME"], options=country_cities, key="6")

    ## render multi options
    render_other(tedi_fieds_1, ["placeholder_sold_as",  "placeholder_other_sold_as"],
                 ["sold_as"], core_guidelines, interface_dic, 0)
    render_other(tedi_fieds_1, ["placeholder_sample_form",  "placeholder_other_sample_form"],
                 ["sample_form"], core_guidelines, interface_dic, 1)

    render_other(tedi_fieds_2, ["placeholder_unit_substance",  "placeholder_other_unit_substance"],
                 ["unit_substance"], core_guidelines, interface_dic, 2)

    render_other(tedi_fieds_2, ["placeholder_price_currency",  "placeholder_other_price_currency"],
                 ["price_currency"], core_guidelines, interface_dic, 3)

    render_other(news_fields, ["placeholder_reasons_dc_visit", "placeholder_other_reasons_dc_visit"]
                 ,  ["reasons_dc_visit"], news_guidelines, interface_dic, "4b")

    render_other(tedi_fieds_2, ["placeholder_provider_relation", "placeholder_other_provider_relation"]
                 ,  ["provider_relation"], core_guidelines, interface_dic, "5b")


    # conditional fields
    tedi_fields = tedi_fieds_1 | tedi_fieds_2

    combined_gidelines = news_guidelines | core_guidelines

    if submit:

        submit_dict = analysis_init | tedi_fields | news_fields
        submit_dict = {x: submit_dict[x] for x in submit_dict if not x.startswith("placeholder")}

        if submit_dict["organisation"] and submit_dict['sample_form'] and submit_dict['sold_as']:

            submit_dict["sample_uid"] = str(uuid.uuid4())[:8]
            st.info(f"### {interface_dic['sample_id']}: {submit_dict['sample_uid']}")


            dic_set = {
                submit_dict["sample_uid"]: submit_dict}

            st.text(f"{submit_dict['sample_uid']}, {str(tedi_fields['organisation'])}, {submit_dict}")
            post_to_db(dic_set, submit_dict['sample_uid'], collection_name)

        else:

            missing_fields = [combined_gidelines[x]["VARIABLE_NAME"] for x in compulsory_data if not submit_dict[x]]
            st.warning(f"{interface_dic['warning_req_fields']} \n {missing_fields}")
    current_data = return_db(collection_name)[1]


    if st.button(interface_dic['show_db'], key="5a"):
        st.dataframe(current_data)

    _, db2 = st.columns(2)

    with db2:
        csv = convert_df(current_data)

        file_name = f'{tedi_fields["date"]}_{tedi_fields["organisation"]}_DB'

        st.download_button(
            f"{interface_dic['download_csv']}",
            csv,
            f"{file_name}.csv",
            "text/csv",
            key='download-csv'
        )


    st.markdown("##")
    st.subheader(interface_dic['upload_img'])
    image_file = st.file_uploader(interface_dic['upload_img'], type=["png", "jpg", "jpeg"])





    if image_file:
        if st.button(interface_dic['confirm_upload'], key=6):
            pic_pil = load_image(image_file)
            pic_ext = image_file.type.split("/")[1]
            pic_pil.save(os.path.join("../images_db", f"{submit_dict['sample_uid']}.PNG"))
            st.success(f" {interface_dic['saved_img']} `{submit_dict['sample_uid']}.{pic_ext}`")
    st.markdown("##")

    if st.button(interface_dic['show_db'], key=7):

        st.dataframe(return_db(collection_name)[1])

    update_db(interface_dic, collection_name)

    # # Then get the data at that reference.
    # doc = doc_ref.get()
    #
    # # Let's see what we got!
    # st.write("The id is: ", doc.id)
    # st.write("The contents are: ", doc.to_dict())
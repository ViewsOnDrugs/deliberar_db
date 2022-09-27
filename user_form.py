
import streamlit as st
import uuid
import geonamescache
from query_db import post_to_db
from lib.orga_lib import load_orga_lib
from lan.load_lan import load_lan

orga_dict = load_orga_lib()

gc = geonamescache.GeonamesCache()
countries = gc.get_countries()
cities_all=gc.get_cities()


def user_form(username):

    lang_main = orga_dict[username]["lan"]

    # Load TEDI guidelines
    GUIDELINES = load_lan(lang_main)

    interface_dic = GUIDELINES['_interface']

    required_fields = [x for x in GUIDELINES if x not in ['substances', '_interface'] and GUIDELINES[x]["REQUIREMENT_LEVEL"] == 'required']

    country_list = [countries[x]['name'] for x in countries]
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

    if 'country' not in st.session_state:
        st.session_state.country = []

    input_country = st.selectbox(GUIDELINES["country"]["VARIABLE_NAME"], options=country_list, key="4")

    if input_country:
        selected_country = [x for x in countries if countries[x]['name'] == input_country][0]

        country_cities = [cities_all[x]['name'] for x in cities_all if
                          cities_all[x]['countrycode'] == selected_country]


    with st.form("Sample Form"):


        col1, col2 = st.columns(2)

        with col1:
            date = str(st.date_input(GUIDELINES["date"]["VARIABLE_NAME"], key="1"))
            st.markdown(f"##### {interface_dic['organization']}")
            organisation = orga_dict[username]['name']
            city = st.selectbox(GUIDELINES["city"]["VARIABLE_NAME"], options=country_cities,  key=" 5")
            gender = st.selectbox(GUIDELINES["gender"]["VARIABLE_NAME"], options=GUIDELINES["gender"]["VOCABULARY"], key="19")
            age = st.selectbox(GUIDELINES["age"]["VARIABLE_NAME"], options=range(0,200), key="20")



        with col2:

            sold_as = st.selectbox(GUIDELINES["sold_as"]["VARIABLE_NAME"], options=GUIDELINES["sold_as"]["VOCABULARY"], key="8")
            sample_form = st.selectbox(GUIDELINES["sample_form"]["VARIABLE_NAME"], options=GUIDELINES["sample_form"]["VOCABULARY"], key="11")
            colour = st.color_picker(GUIDELINES["colour"]["VARIABLE_NAME"], key="12")
            geo_context = st.selectbox(GUIDELINES["geo_context"]["VARIABLE_NAME"], options=GUIDELINES["geo_context"]["VOCABULARY"], key="6")
            provider_relation = st.selectbox(GUIDELINES["provider_relation"]["VARIABLE_NAME"], options=GUIDELINES["provider_relation"]["VOCABULARY"], key=" 7")
            alias = st.text_input(GUIDELINES["alias"]["VARIABLE_NAME"], key="9")
            used_prior = st.checkbox(GUIDELINES["used_prior"]["VARIABLE_NAME"], key="10")
            logo = st.text_input(GUIDELINES["logo"]["VARIABLE_NAME"], key="13")

        st.markdown(f"##### {interface_dic['req_field']}")
        submit = st.form_submit_button(f" {interface_dic['submit_samp']}")


        if submit:

            if organisation and sample_form and sold_as:

                sample_uid = str(uuid.uuid4())[:8]
                st.info(f"### {interface_dic['sample_id']}: {sample_uid}")

                dic_set = {
                    sample_uid: {"date": date, "organisation": orga_dict[username]['name'], "sample_uid": sample_uid,
                                 "country": input_country, "city": city, "geo_context": geo_context,
                                 "relationship": provider_relation,
                                 "sold_as": sold_as, "alias": alias, "used_prior": used_prior,
                                 "sample_form": sample_form,
                                 "colour": colour, "logo": logo,
                                 "gender": gender, "age": age}
                }

                st.text(f"{sample_uid}, {str(organisation)}, {sample_form}")
                post_to_db(dic_set, sample_uid)

            else:

                missing_fields = ['organisation', 'sample_form', 'sold_as']
                st.warning(f"{interface_dic['warning_req_fields']} \n {missing_fields}")


    # # Then get the data at that reference.
    # doc = doc_ref.get()
    #
    # # Let's see what we got!
    # st.write("The id is: ", doc.id)
    # st.write("The contents are: ", doc.to_dict())
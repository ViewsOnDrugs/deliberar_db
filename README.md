# TEDI streamlit form for data collection, storing, and sharing

This repository hosts a prototype of the TEDI data collection tool developed for the NGO [Deliberar](https://deliberar.org/).
As a proof of concept, it implements the [expanded version](https://github.com/harmreduction/tedi_guidelines/blob/main/README.md) of the TEDI guidelines

It uses Streamlit as the python library for the form and Google Firebase for the data storage

Click on [![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://viewsondrugs-deliberar-db-streamlit-app-q1n3n4.streamlitapp.com/) to see the live version. For login access please contact francisco@mybrainmychoice.de

## Requirements

- python 3.9
- streamlit 1.10+
- [`requirements.txt`](https://github.com/ViewsOnDrugs/deliberar_db/blob/main/requirements.txt)

### DB 
This prototype uses Google Firebase and a local database stored as a JSON file for offline work.
Information on how to set up and config other DB types may be added in the future.


### Set up DB

To set up the firebase DB and the authentication methods follow [these instructions](https://blog.streamlit.io/streamlit-firestore/#part-2-setting-up-firestore)

### Set up Web Tool

Only after setting up the DB, it's offline set-up is on dev.

#### offline set-up:

  - clone this repository to your local system. `git clone https://github.com/ViewsOnDrugs/deliberar_db.git`
  - cd into the created directory and run `pip install -r requirements.txt`
  - run `streamlit run streamlit_app.py`
  
  A `local_db.json` file will be created to store the submitted information through the form.
  

#### online set-up: 

A detailed guide on how to set up a streamlit application can be found [here](https://docs.streamlit.io/streamlit-cloud/get-started/deploy-an-app)

- fork this repository to your organization's/private repository

- create a streamlit account

- add your forked repository to your streamlit account. you can control the access to the form through your streamlit account

#### Authentication set-up

  TBD partially from https://towardsdatascience.com/how-to-add-a-user-authentication-service-in-streamlit-a8b93bf02031
  - add secrets to the streamlit admin page



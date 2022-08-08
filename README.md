# TEDI streamlit form for data collection, storing, and sharing

This repository hosts a prototype of the TEDI data collection tool developed for the NGO [Deliberar](https://deliberar.org/).
As a proof of concept, it implements the [expanded version](https://github.com/harmreduction/tedi_guidelines/blob/main/README.md) of the TEDI guidelines

It uses streamlit as the python library for the form and google firebase for the data storage

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

only after setting up the DB, offline set-up is on dev.

#### local set-up:

  - clone this repository to your local system. 
  - cd into the created directory and run `pip install -r requirements.txt`
  - run `streamlit run streamlit_app.py`
  
  a file `local_db.json` will be created to store the submitted information through the form.
  

#### online set-up: 

A detailed guide on how to set up a streamlit application can be found [here](https://docs.streamlit.io/streamlit-cloud/get-started/deploy-an-app)

- fork this repository to your organization's/private repository

- create a streamlit account

- add your forked repository to your streamlit account. you can control the access to the form through your streamlit account



import os
import openpyxl
import json
import requests
from st_on_hover_tabs import on_hover_tabs
import time
import pandas as pd
import numpy as np
import smtplib
from email.message import EmailMessage
from streamlit_lottie import st_lottie
from st_aggrid import AgGrid
from datetime import datetime
import streamlit.components.v1 as components
import altair as alt
from annotated_text import annotated_text
import time
import streamlit as st

st.set_page_config(layout="wide")
st.markdown('<style>' + open('./style.css').read() + '</style>', unsafe_allow_html=True)

#Defining the side hover bar of the website
with st.sidebar:
    tabs = on_hover_tabs(tabName=['Beranda', 'Akses Pasar UMKM', 'Contact', 'Info'], 
                         iconName=['home', 'code', 'mail', 'feed'],
                         styles = {'navtab': 
                                   {'background-color':'#111','color': '#D2DADA','font-size': '18px','transition': '.3s','white-space': 'nowrap','text-transform': 'capitalize'},
                                   'tabOptionsStyle': {':hover :hover': {'color': '#FFD700','cursor': 'pointer'}},
                                   'iconStyle':{'position':'fixed','left':'7.5px','text-align': 'left'},
                                   'tabStyle' : {'list-style-type': 'none','margin-bottom': '30px','padding-left': '30px'}}, 
                key="1")

#Defining the main home page of the website
if tabs =='Home':

    col1, col2 = st.columns(2)
    with col1:
        st.title("Garuda Mandiri -  Akses Pasar UMKM AI")
        st.subheader("GAMAN untuk Hackathon Bank Indonesia")

    with col2:
        def load_lottieurl(url:str):
            r = requests.get(url)
            if r.status_code != 200:
                return None
            return r.json()
        lottie_animation = load_lottieurl("https://lottie.host/2973be8b-d627-4cf1-9103-6cbcf7bc3f3a/HvqShH2SRQ.json")
        st_lottie(lottie_animation, key="animation")   

#Defining the main webpage page
elif tabs == 'Akses Pasar UMKM':
    st.title("Garuda Mandiri -  Akses Pasar UMKM AI")
    st.subheader("Portal GAMAN - Garuda Mandiri ini memfasilitasi para wirausaha UMKM dalam mencari pasar untuk menjual produknya! ")
    st.caption("Silahkan Pilih!")
    st.markdown("")

    def load_data():
        data = pd.read_excel('Federal Crowdsourcing and Citizen Science Catalog.xlsx', engine='openpyxl')
        return data
    data = load_data()

    #Creating the first filter using topic column
    topic_values = data["geographic scope"].unique()

    search_value_topic = st.selectbox("Select a project location where you are interested in: ", topic_values, format_func=lambda x: 'Select an option' if x == '.' else x)
    topic_data = data[data["geographic scope"] == search_value_topic]

    #Creating the second filter using language column
    language_values = topic_data["agency sponsor"].unique()
    search_value_language = st.selectbox("Select a agency sponsor or institution that you are interested in: ", sorted(language_values), format_func=lambda x: 'Select an option' if x == '.' else x)
    language_data = topic_data[topic_data["agency sponsor"] == search_value_language]

    #Creating the third filter using tags column
    delimiter = ',' 
    column_with_multiple_entries = "fields of science"
    combined_list = []
    language_data[column_with_multiple_entries] = language_data[column_with_multiple_entries].astype(str)
    for row in language_data[column_with_multiple_entries]:
        elements = [element.strip() for element in str(row).split(delimiter)]
        combined_list.extend(elements)

    #Extracted unique tags from the data so far filtered
    unique_tags_value = list(set(combined_list))

    search_value_tags = st.multiselect("Select the top 10 fields of science of your expertises: ", sorted(unique_tags_value), max_selections=10, format_func=lambda x: 'Select an option' if x == '.' else x)
    tags_data = language_data[language_data["fields of science"].apply(lambda x: any(tag in x for tag in search_value_tags))]

    columns_to_display = ["Name of Project", "project description", "geographic scope", "keywords", "email"]

    #Dictionary to map original column names to display names
    display_names = {
        "Name of Project": "Project",
        "project description": "Description",
        "geographic scope": "Location",
        "keywords": "keywords",
        "email": "email"
    }
    
    tags_data_display = tags_data[columns_to_display].rename(columns=display_names)

    #Displaying the final table
    #Generate HTML table with center-aligned headers and without the index
    html_table = tags_data_display.to_html(render_links=True, escape=False, index=False)
    
    html_table = html_table.replace('<thead>', '<thead style="text-align: center;">')
    html_table = html_table.replace('<th>', '<th style="text-align: center;">')

    #Display the modified HTML table using Markdown
    st.markdown(html_table, unsafe_allow_html=True)

#Defining the contact page
elif tabs == 'Contact':
    col1, col2 = st.columns(2)
    with col1:
        st.title("Please Contact Us")
        st.subheader('We would love to know your interests and hear your feedback!')
        st.markdown("")
        
        def load_lottieurl(url:str):
            r = requests.get(url)
            if r.status_code != 200:
                return None
            return r.json()
        lottie_animation_1 = load_lottieurl("https://lottie.host/88388127-1326-42e4-825a-2688f1501dce/3gmaAzsf2L.json")
        st_lottie(lottie_animation_1, key="animation1")   
    
    with col2:
        st.title(" ")
        #Defining the form fields
        with st.form('Contact Form'):
            name = st.text_input('Name')
            email = st.text_input('Email')
            number = st.text_input('Phone Number')
            message = st.text_area('Message')
            submit_button = st.form_submit_button(label='Submit')

        #Processing the form submission
        if submit_button:
            print(f'Name: {name}')
            print(f'Email: {email}')
            print(f'Phone Number : {number}')
            print(f'Message: {message}')
            st.success('Thank you for reaching out to me. I will get back to you as soon as possible.')
            st.balloons()

#Defining the about page of the project
elif tabs == 'About':

    st.title("About NASA Project Creator + Contributor Zone by GAMAN")
    st.markdown("### Developing A Marketplace for Open Science Projects for NASA Space Apps Challenge 2023")

    st.markdown("#### Project Description")
    annotated_text("NASA Project Creator + Contributor Zone is ", (" a Web App ", " ", "#fea"), " This Web App suggests and recommends users the most appropriate NASA Open Science Project based on keywords, fields of science, agency sponsor, geographic scope, and participation tasks.")
    
    st.markdown("#### Pain Point")
    annotated_text(" Currently, there is no place online for Open Science project creators and skilled participants to find each other, mingle, and foster professional relationships to work on interesting open research projects. Thus, we propose the creation of this project: ", ("NASA Project Creator + Contributor Zone. ", " " , "#fea"), " The idea behind this project is to provide a valuable solution that open science contributors in looking for interesting and relevant project ideas based on their interest and expertises.")
    
    st.markdown("#### Objectives")
    annotated_text("The main objectives of this web app is to create a marketplace for open science projects so that open science projects will be more accessible for everyone who eager to contribute to science projects related to their interests. Also, we want to build a marketplace for project creators to find creators who match with all skills & expertise required in the project. We will be building this marketplace in web application using Machine Learning, Large Language Model (LLM), Generative AI and Natural Language Processing (NLP).")
    
    st.markdown("#### Links")
    annotated_text("Github Repository ",("[link to the project](https://github.com/fickya1987/)","  " ,"#fea"), " and ", ("[link to the Dataset](https://docs.google.com/spreadsheets/d/1xHPhXiCOfWn2t6HTlKytXKKO0J0dqUi0lcyylb1JMlQ/edit#gid=0)","  " ,"#fea"), " used in this project.", (""))
    
    st.markdown("#### Let's Connect!")
    linkedin_button = '<a href="https://www.linkedin.com/in/ficky-alkarim-a89353a9/" target="_blank" style="text-align: center; margin: 0px 10px; padding: 5px 10px; border-radius: 5px; color: white; background-color: #0077B5; text-decoration: none">LinkedIn</a>'
    github_button = '<a href="https://github.com/fickya1987/" target="_blank" style="text-align: center; margin: 0px 10px; padding: 5px 10px; border-radius: 5px; color: white; background-color: #24292E; text-decoration: none">GitHub</a>'
    st.markdown("Connect with me on my socials - " f'{linkedin_button}{github_button} ', unsafe_allow_html=True)

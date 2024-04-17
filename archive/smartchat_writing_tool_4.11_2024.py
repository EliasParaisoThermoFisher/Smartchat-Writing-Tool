# BEGINNING OF CODE
# layout: 1 column with left sidebar
# model: GPT-3.5-Turbo

from openai import AzureOpenAI
import streamlit as st
from streamlit_chat import message
# from langchain.chat_models import AzureChatOpenAI
from langchain_openai import AzureChatOpenAI
from langchain.schema import (SystemMessage,HumanMessage,AIMessage)
import os
from dotenv import load_dotenv

# get the credentials from .env
load_dotenv()
AZURE_KEY = os.getenv('GENEAIGPT35_KEY')
AZURE_ENDPOINT = os.getenv('GENEAIGPT35_ENDPOINT')
AZURE_NAME = os.getenv('GENEAIGPT35_DEPLOYMENT_NAME')
AZURE_VERSION = os.getenv('GENEAIGPT35_VERSION')

# begin: function definitions, must be at the top before the code that calls them

# end: function definitions

# begin: main page setup
st.set_page_config(layout="wide",page_title="Your own ChatGPT",page_icon=":dna:")
st.header("Welcome to the Smart Chat writing assistant!")
st.success("** GPT-3.5-Turbo, trained on data up to September 2021 **")
# end: main page setup

# begin: left sidebar
clear_button = st.sidebar.button("New Chat", key="clear")
with open("sidebar.md") as sidebar_file:
    sidebar_content = sidebar_file.read()
st.sidebar.markdown(f'<font style="font-size: 20px;">Status:&nbsp;&nbsp;&nbsp;</font><a href="http://abmaint.test.thermofisher.com/MCDashboard/verticlechat_mvp.cfm" style="text-decoration: none;" title="In Pilot">:airplane:</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;<a href="https://geneai.thermofisher.com/ask-gene" target="_blank" style="text-decoration: none;" title="Available in Prod">:star: </a>', unsafe_allow_html=True)
st.sidebar.markdown(sidebar_content)
# add a download button 

# add a view code button for displaying the code in column 1
viewCode = st.sidebar.button('View Code')
# end: left sidebar

# begin: main code
# st.session_state['writing_option'] = []
writing_options = ['Grammar', 'ReWrite', 'Summarize', 'Lengthen', 'Shorten', 'Email Subjects']
cols = st.columns(len(writing_options))
for col, writing_option in zip(cols, writing_options):
    if col.button(writing_option):
        st.session_state['writing_option'] = writing_option
        print("Writing option " + writing_option + " selected.")
    
    # reset everything
if clear_button:
    st.session_state['messages'] = [
        SystemMessage(content="You are a helpful assistant.")
    ]

# initialize message history
if "messages" not in st.session_state:
    st.session_state.messages = [
        SystemMessage(content="You are a helpful assistant.")
    ]

# capture the user's prompt
user_input = st.chat_input("Enter your prompt here... ", key="user_input")

llm = AzureChatOpenAI(deployment_name=AZURE_NAME, openai_api_version=AZURE_VERSION, openai_api_key=AZURE_KEY, azure_endpoint=AZURE_ENDPOINT)

# handle user prompt
if user_input:
    with st.spinner("Thinking..."):
        st.session_state.messages.append(HumanMessage(content=user_input))

        # Check which writing tool option is selected and modify the prompt accordingly
        if st.session_state['writing_option'] == 'Grammar':
            user_input = "Please correct the grammar: " + user_input
            print(user_input)
        elif st.session_state['writing_option'] == 'ReWrite':
            user_input = "Please rewrite this to make it more clear: " + user_input
        elif st.session_state['writing_option'] == 'Summarize':
            user_input = "Please summarize this: " + user_input
        elif st.session_state['writing_option'] == 'Lengthen':
            user_input = "Please elaborate on this: " + user_input
        elif st.session_state['writing_option'] == 'Shorten':
            user_input = "Please shorten this: " + user_input
        elif st.session_state['writing_option'] == 'Email Subjects':
            user_input = "Please suggest a subject line for this email: " + user_input

        print(st.session_state['writing_option'])
        print("Session state messages: " , st.session_state.messages)

        # st.session_state.messages.append(HumanMessage(content=user_input))
        temp_messages = [SystemMessage(content='You are a helpful assistant.'), HumanMessage(content=user_input)]
        # response = llm(st.session_state.messages)
        response = llm(temp_messages)

    st.session_state.messages.append(AIMessage(content=response.content))

# display message history
messages = st.session_state.get('messages', [])
for i, msg in enumerate(messages[1:]):
    if i % 2 == 0:
        message(msg.content, is_user=True, key=str(i) + '_user')
    else:
        message(msg.content, is_user=False, key=str(i) + '_ai')


# END OF CODE
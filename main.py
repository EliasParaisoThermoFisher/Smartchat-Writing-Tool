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
import re
import zipfile

# get the credentials from .env
load_dotenv()
AZURE_KEY = os.getenv('GENEAIGPT35_KEY')
AZURE_ENDPOINT = os.getenv('GENEAIGPT35_ENDPOINT')
AZURE_NAME = os.getenv('GENEAIGPT35_DEPLOYMENT_NAME')
AZURE_VERSION = os.getenv('GENEAIGPT35_VERSION')

llm = AzureChatOpenAI(deployment_name=AZURE_NAME, openai_api_version=AZURE_VERSION, openai_api_key=AZURE_KEY, azure_endpoint=AZURE_ENDPOINT)    

# Initialize a session state variable that tracks the sidebar state (either 'expanded' or 'collapsed').
if 'sidebar_state' not in st.session_state:
    st.session_state.sidebar_state = 'expanded'

# st.set_page_config(layout="wide",page_title="Your own ChatGPT",page_icon=":dna:")
st.set_page_config(layout="wide", page_title="Your own ChatGPT",page_icon=":dna:", initial_sidebar_state=st.session_state.sidebar_state)
st.header("Welcome to the Smart Chat Writing Assistant!")

# begin: function definitions, must be at the top before the code that calls them

# Adjusts the number of results displayed to improve user experience
def set_message_history(num_results):
    messages = st.session_state.get('messages', []) 
    num_messages = (len(messages)-1)/2  
    if num_messages > num_results:
        if num_results % 2 == 0:
            print("Adjusting ...")
            st.session_state['messages'] = messages[num_results:] #2 works great
        else:
            st.session_state['messages'] = messages[num_results+1:]

# capture the user's prompt with on_change callback
def on_change():
    print(st.session_state['user_input'])
    st.session_state['user_text'] = st.session_state['user_input']
     # Check if the enter key was pressed by comparing the current value with the session state
    if st.session_state['user_input'] != st.session_state.get('last_input', ''):
        st.session_state['last_input'] = st.session_state['user_input']
        # if writing_option not in st.session_state:
        #     st.session_state['writing_option'] = 'Rewrite'
        handle_submit(st.session_state['user_input'])

# Check which writing tool option is selected and modify the prompt accordingly
def get_rewrite_prompt(user_input):
        if st.session_state['writing_option'] == 'Grammar':
            user_input = "Please correct the grammar: " + user_input
        elif st.session_state['writing_option'] == 'Rewrite':
            user_input = "Please rewrite this to make it more clear: " + user_input
        elif st.session_state['writing_option'] == 'Summarize':
            user_input = "Please summarize this: " + user_input
        elif st.session_state['writing_option'] == 'Lengthen':
            user_input = "Please elaborate on this: " + user_input
        elif st.session_state['writing_option'] == 'Shorten':
            user_input = "Please shorten this: " + user_input
        elif st.session_state['writing_option'] == 'Email Subjects':
            user_input = "Please suggest a subject line for this email: " + user_input
        return user_input

# Define a function to handle the submission
def handle_submit(user_input):
    with st.spinner("Thinking..."):
        #Clears out input field upon each submission
        st.session_state.input = st.session_state.user_input
        st.session_state.user_input = ''
        st.session_state.messages.append(HumanMessage(content=user_input))
        temp_messages = [SystemMessage(content='You are a helpful writing assistant.'), HumanMessage(content=get_rewrite_prompt(user_input))]
        print(f"\n\n TEMP MESSAGES: {temp_messages} \n\n")
        response = llm(temp_messages)
    st.session_state.messages.append(AIMessage(content=response.content))
    set_message_history(st.session_state['num_results'])

# EXCLUDE:START
def get_export_code():
    with open(__file__) as f:
        lines = f.readlines()
    codeout = []
    excludeon = False
    for line in lines:
        if "# EXCLUDE:START" in line:
            excludeon = True
        if not excludeon:
            codeout.append(line)
        if 'if' not in line and "# EXCLUDE:END" in line:
            excludeon = False
    code = ''.join(codeout)
    return code

def get_env_file():
    with open(__file__) as f:
        lines = f.readlines()
    captured = []
    capture = False
    for line in lines:
        if capture and '#' in line:
            capture = False
        if capture:
            captured.append(line)
        if "# SET KEYS" in line:
            capture = True
    newlines = []
    pattern = r'(?:os\.getenv\(\'|os\.getenv\(")(.*)(?:\'\)|"\))'
    for capturedline in captured:
        match = re.search(pattern,capturedline)
        if match:
            newlines.append(f'{match.group(1)} = TBD\n')
    envlines = ''.join(newlines)
    if not os.path.exists('.env'):
        with open('.env','w') as f:
            f.write(envlines)
    return envlines

def create_zip(projname, export_extras=[]):
    export_files = ['requirements.txt','README.md']
    export_files.extend(export_extras)
    filename = projname + ".zip"
    with zipfile.ZipFile(filename, 'w') as z:
        for file in export_files:
            if os.path.exists(file):
                z.write(file)
        z.writestr('main.py', get_export_code())
        z.writestr('.env', get_env_file())

def show_code():
    code = get_export_code()
    st.code(code, language='python')

sidebar_content = None;
if os.path.exists("sidebar.md"):
    with open("sidebar.md") as sidebar_file:
        sidebar_content = sidebar_file.read()
projectname = os.path.split(os.path.abspath(os.curdir))[1]
if projectname == 'smartchat_writing_assistant':
    projectname = 'SmartChat Writing Assistant'

# exportfiles - list of files to export.   Always expect there to be:
# - main.py (this file)
# - README.md
# - requirements.txt
# If others required, make sure to ad them to export_extras (relative to current dir)

# Ex:
# export_extras = ['main2.py','subdir/file2']
export_extras = []

# While thisis being actively developed, keep recreatezip = True.   Once ready for primetime, set to False
recreatezip = True  # Set to False when ready for primetime

if not os.path.exists(projectname + ".zip") or recreatezip:
    create_zip(projectname,export_extras)
zipfile = open(projectname + ".zip", 'rb').read()
with st.sidebar:
    st.header(projectname)
    if os.path.exists("sidebar.png"):
        st.image("sidebar.png")
    if sidebar_content:
        st.markdown(sidebar_content, unsafe_allow_html=True)

    st.button('View Source',on_click=show_code)
    st.download_button(label='Download Source',data=zipfile,mime='application/zip',file_name=projectname + ".zip")

# EXCLUDE:END

# Main AI Code

# end: function definitions

# begin: main page setup
# end: main page setup

# begin: left sidebar

# end: left sidebar

# begin: main code

# initialize message history
if "messages" not in st.session_state:
    st.session_state.messages = [
        SystemMessage(content="You are a helpful writing assistant.")
    ]
    
if "user_text" not in st.session_state:
    st.session_state['user_text'] = ""

if "writing_option" not in st.session_state:
    st.session_state['writing_option'] = 'Rewrite'

if input not in st.session_state:
    st.session_state.input = ''

if 'num_results' not in st.session_state:
    st.session_state['num_results'] = 2

writing_options = ['Rewrite', 'Grammar', 'Summarize', 'Lengthen', 'Shorten', 'Email Subjects']
cols = st.columns(len(writing_options))
for col, writing_option in zip(cols, writing_options):
    if col.button(writing_option):
        # st.session_state['writing_option'] = writing_option
        st.session_state.writing_option = writing_option
        handle_submit(st.session_state['user_text'])

# Keep success message as low as possible in the code so that it has the most up to date session state
st.success(f"** Use this tool to rewrite any given text in the selected format! Select a button to process your input. Current selection: {st.session_state.writing_option}**")

user_input = st.text_input("Enter your prompt here... ", key="user_input", on_change=on_change, help="Enter the text you want to process and then select a button.")

col1, col2, _ = st.columns([1] + [2] + [2])
clear_button = col1.button("Clear", key="clear")
if clear_button:
    st.session_state['messages'] = [
        SystemMessage(content="You are a helpful writing assistant.")
    ]

display_slider = col2.slider("How many messages do you want to display?", 1, 5, st.session_state['num_results'], 1)
if display_slider:
    st.session_state['num_results'] = display_slider
st.markdown('''
<style>
data-baseweb {
height: 5px;
} 
</style>
''', unsafe_allow_html=True)
# display message history
messages = st.session_state.get('messages', [])
for i, msg in enumerate(messages[1:]):
    if i % 2 == 0:
        message(msg.content, is_user=True, key=str(i) + '_user')
    else:
        message(msg.content, is_user=False, key=str(i) + '_ai')


# END OF CODE
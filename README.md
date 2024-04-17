# Project Title
Smart Chat Writing Assistant 

## Introduction
This app is designed to provide users with a convenient way to rephrase text in a specific format of their choice. It allows users to input their desired text, which could be a sentence, a paragraph, or even an entire document.

## Requirements
Python 3.

## Installation and Setup
Follow these steps to get the application up and running on your local machine.

### Step 1: Unzip the Code
The code for this project is provided in a compressed (ZIP) file. After downloading the file, you need to extract its contents. You can do this by 
- (Win) right-clicking on the file and selecting 'Extract All...' 
- (MacOS) double-clicking the archive
- (other) or by using any standard unzipping tool.

### Step 2: Set up Virtual Environment
Virtual Environments allows you to set a specific version of Python, as well as to isolate extra packages you may download.  This will allow apps to have different version of the same package.   For more information go to [https://docs.python.org/3/library/venv.html](https://docs.python.org/3/library/venv.html)

After unzipping, navigate to the project directory containing the project files that you just unzipped. 

Usage:

`python -m venv .venv`
> [!NOTE]
> This assumes that you are executing the command from the project directory.   You should see the directory .venv at the project root, with a number of sub-directories.  

You must activate the virtual environment.
Win: ``.\.venv\Scripts\activate``
MacOS, Linux: ``source .venv/bin/activate``

Your command/terminal prompt will now be prefixed with (.venv)

### Step 3: Install Required Packages
From your activated terminal, install the required Python packages by running the following command:

`pip install -r requirements.txt`

This command will automatically install all the necessary packages listed in the `requirements.txt` file.

### Step 4: Request API Keys

Go to http://geneaipilot.thermofisher.com/accelerator.cfm and request API keys.  Once you receive the credentials, open .env and replace the placeholder code with them.

```python
GENEAIAPI_KEY = TBD
GENEAIAPI_AZURE_ENDPOINT = TBD
GENEAIAPI_DEPLOYMENT_NAME = TBD
GENEAIAPI_VERSION = TBD
```

> [!IMPORTANT]
> Do not put quotes around the values for the key or endpoint.

In your code, you will see a code block similar to:
```python
AZURE_KEY = os.getenv('GENEAIAPI_KEY')
AZURE_ENDPOINT = os.getenv('GENEAIAPI_AZURE_ENDPOINT')
AZURE_NAME = os.getenv('GENEAIAPI_DEPLOYMENT_NAME')
AZURE_VERSION = os.getenv('GENEAIAPI_VERSION')
```
If your key names are different, that is OK.   They will normally be named with the MODEL_KEYPURPOSE pattern.   Just match the _KEYPURPOSE from your key to the appropriate variable.

Sample initializtion code for various libraries:
- langchain-community.chat_models
  -  `model = AzureChatOpenAI(deployment_name=AZURE_NAME, openai_api_version=AZURE_VERSION, openai_api_key=AZURE_KEY, openai_api_base=AZURE_ENDPOINT)`
- openai
  - `model = AzureOpenAI(azure_endpoint=AZURE_ENDPOINT,api_key=AZURE_KEY,api_version=AZURE_VERSION)`
  - ```python
    # openai uses the model (or AZURE_NAME) in a function call
    response = client.chat.completions.create(
        model=AZURE_NAME,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Does Azure OpenAI support customer managed keys?"}
        ]
    )
    ```
- pandasai.llm
  - ```python
    model = AzureOpenAI(
        api_version=AZURE_VERSION,
        api_token=AZURE_KEY,
        azure_endpoint=AZURE_ENDPOINT,
        deployment_name=AZURE_NAME,
        is_chat_model=True # <--- NOTICE!
    )
    ```

> [!WARNING]
> **DO NOT** share these keys
> 
> **DO NOT** share this file.
> 
> The `.env` file is a hidden file that contains the credentials to access the Model.  Sharing this information can lead to key revokation


### Step 4: Running the Application
Once the packages are installed and credentials are saved, you can start the application. Type the following command in the terminal or command prompt:

`streamlit run main.py`

This will start the Streamlit server and open the application in your default web browser.


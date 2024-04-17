# Project Title
SmartChat Writing Assistant 

## Introduction
This app provides tools to assist with writing tasks. 

## Key Features
When run from the code you create, a side bar will be present that contains:
- Application Name
- A description of the application 
- What the purpose of it is/problem it attemps to solve
- Help text if needed
- View code button
- Download code button


When the app is run, it will create the preview code content and the download file content from the code you create!

> [!NOTE]
> The code presented in the View Code and is downloaded will **not** contain the side bar or any of its functionality.   The sidebar is merely there for the demo code being created.

## Contents
Some files are used with the development of the sample app, and others are skeletons that will need to be completed and will be part of the distribution package.
- .env : Skeleton .env file.   Fill this out with your keys.   The keys you add here will *not* be distributed to the end user. (development)
- aiBpRequirements.txt : Requirements for the boiler plate app. (development)
- main.py : the sample application file (both)
- README-AITEAMDEV.md : This file (development)
- README.md : The README that should be distributed to the end user (distribution)
- requirements.txt : The requirements that will be distributed to the end user (distribution)
- sidebar.md : Skeleton filefor the sidebar shown on the Innovation Hub (development)
- sidebar.png : Image to display with app on Innovation Hub. *Hint: use the DALL-E 3 image creation sample app.* (development)

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

`python -m venv venv`
> [!NOTE]
> This assumes that you are executing the command from the project directory.   You should see the directory .venv at the project root, with a number of sub-directories.  

> [!NOTE]
> Do not use ".venv".   Use "venv" for the location of the virtual envronment files.  Not using "venv" will cause later step to break.  

You must activate the virtual environment.
Win: ``.\.venv\Scripts\activate``
MacOS, Linux: ``source .venv/bin/activate``

Your command/terminal prompt will now be prefixed with (.venv)

### Step 3: Install Required Packages
From your activated terminal, install the required Python packages by running the following command:

`pip install -r aiBpRequirements.txt`

This command will automatically install all the necessary packages listed in the `aiBpRequirements.txt` file.

> [!NOTE]
> Do not run this against requirements.txt.   Requirements.txt needs to contain only the items relevent to the downloaded app (without the sidebar).   

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

### Step 5: Create your app
Create your app as normal.   

Modify the file `sidebar.md`, updating the following:
- A description of the application 
- What the purpose of it is/problem it attemps to solve
- Help text if needed

Sidebar.md and sidebar.png will automatically be imported in on run of the app.

Make sure any functionality for the side bar remains in the existing block surrounded by `# EXCLUDE:START` and `# EXCLUDE:END`, or create a new block with `# EXCLUDE:START` and `# EXCLUDE:END`.

### Step 6: Prep app for QA/Production
#### Create requirements.txt
from the command line, run `pipreqs`.   This will capture required libraries based on your imports.  Open the new requirements.txt, and remove any package from there that is listed the the block of imports from "EXCLUDE:START LIBS" to "EXCLUDE:END LIBS" and save it.

#### Set app to not recreate zip on every load
Find the line `recreatezip = True  # Set to False when ready for primetime` and change it to `recreatezip = False  # Set to False when ready for primetime`

#### Run the application, and verify contents of the zip file
1. Verify that only the packages needed to run without the sidebar are present.
2. Verify that all of the code between `# EXCLUDE:START` and `# EXCLUDE:END` are not present in the main.py from the zip file, or in the code from view code.
3. That the README.md is completed
4. That the .env file has TBD for the key values.


### Step 4: Running the Application
Once the packages are installed and credentials are saved, you can start the application. Type the following command in the terminal or command prompt:

`streamlit run main.py`

This will start the Streamlit server and open the application in your default web browser.


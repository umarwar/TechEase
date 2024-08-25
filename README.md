# Tech Ease

Tech Ease is a Streamlit application designed to assist users with solutions for electronic device and mobile phone issues. By inputting a description of their problem, users receive AI-generated solutions, which can be translated into different languages, summarized, or used to find related articles. This application leverages IBM Watsonx AI for generating solutions and Google Custom Search API for retrieving relevant articles. The translation feature uses Google Translate.

## Features

- **Issue Description Input**: Users can describe the issue with their device or phone.
- **Generate Solution**: AI-generated solutions based on the input description.
- **Translation**: Translate the solution into various languages.
- **Summarization**: Obtain a summarized version of the solution.
- **Search for Related Articles**: Find related articles using Google Custom Search.
- **Past Searches History**: Keeps track of past searches and solutions.
- **Dynamic Language Selection**: Choose the output language for translations.

## Requirements

To run this application, you need to install the following Python packages:

- `streamlit==1.37.1`
- `requests==2.32.2`
- `ibm-watsonx-ai==1.1.6`
- `googletrans==4.0.0rc1`
- `google-api-python-client==2.73.0`

## Setup Instructions

### Creating and Using a Virtual Environment

A virtual environment helps manage project-specific dependencies and avoids conflicts with other Python projects. Follow these steps to create and use a virtual environment for this project:

#### 1. Create a Virtual Environment

Open a terminal or command prompt and navigate to your project directory. Run the following command to create a virtual environment named `venv`:

```sh
python -m venv venv
```
#### 2. Activating the Virtual Environment
```
venv\Scripts\activate
```

### 3. Download all the dependencies and Libraries

```
pip install -r requirements.txt

```

### 4. Run the File
```
streamlit run <filename>.py
```

## License

### This project is licensed under the MIT License. See the LICENSE file for more details.




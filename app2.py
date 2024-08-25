import streamlit as st
import requests
from ibm_watsonx_ai import APIClient, Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.foundation_models.utils.enums import ModelTypes
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from ibm_watsonx_ai.foundation_models.utils.enums import DecodingMethods
from googletrans import Translator  # Install googletrans with `pip install googletrans==4.0.0-rc1`

# Initialize credentials
credentials = Credentials(
    url="https://us-south.ml.cloud.ibm.com",  # Ensure this URL is correct for your region
    api_key="your_api_key"  # Replace with your actual API key
)

# Initialize API client
client = APIClient(credentials)

# Set default project
project_id = '7a78f733-6524-44ea-bd00-e71314499c69'
client.set.default_project(project_id)

# Initialize model inference
model_id = ModelTypes.GRANITE_13B_CHAT_V2
model = ModelInference(
    model_id=model_id,
    params={
        GenParams.DECODING_METHOD: DecodingMethods.GREEDY,
        GenParams.MIN_NEW_TOKENS: 500,  # Adjust to allow for detailed responses
        GenParams.MAX_NEW_TOKENS: 2000,  # Increased for potentially longer responses
        GenParams.STOP_SEQUENCES: ["\n"]
    },
    credentials=credentials,
    project_id=project_id
)

# Initialize Translator
translator = Translator()

# Google Custom Search API details
API_KEY = ''
SEARCH_ENGINE_ID = ''

# Function to summarize text (dummy implementation, replace with actual summarization)
def summarize_text(text):
    # Example summarization (replace with real summarization logic)
    return text[:min(1000, len(text))]  # Simplistic approach for example

# Function to search for articles using Google Custom Search API
def search_articles(query):
    search_url = f"https://www.googleapis.com/customsearch/v1"
    params = {
        'key': API_KEY,
        'cx': SEARCH_ENGINE_ID,
        'q': query
    }
    response = requests.get(search_url, params=params)
    if response.status_code == 200:
        results = response.json()
        articles = results.get('items', [])
        return [(article['title'], article['link']) for article in articles]
    else:
        return []

# Streamlit UI
st.title("Tech Ease")
st.header("Get Solutions for Your Device Issues")

# Sidebar
st.sidebar.header("Options")

# User input section
st.sidebar.subheader("Describe Your Issue")
input_text = st.sidebar.text_area("Enter the issue with your electronic device or mobile phone:", "")

# Language selection
language = st.sidebar.selectbox(
    "Select Output Language",
    ["English", "Spanish", "French", "German", "Chinese"]  # Add other languages as needed
)

# Past search history
if 'history' not in st.session_state:
    st.session_state.history = []

st.sidebar.subheader("Past Searches")
if st.session_state.history:
    for i, (text, result) in enumerate(st.session_state.history):
        st.sidebar.write(f"{i+1}. {text}")
else:
    st.sidebar.write("No past searches.")

# Button to get solution
if st.sidebar.button("Get Solution"):
    if input_text:
        prompt = f"Provide a detailed solution to fix the following issue with a mobile power IC. Describe the possible causes of the issue and the steps to troubleshoot and repair it. Issue: {input_text}"
        
        try:
            response = model.generate_text(prompt=prompt)
            st.write("Generated Solution:")
            st.success(response)  # Display the response
            
            # Save the response to session state
            st.session_state.current_response = response
            
            # Save to history
            st.session_state.history.append((input_text, response))
        except Exception as e:
            st.error(f"Failed to generate solution: {e}")
    else:
        st.warning("Please describe the issue before generating a solution.")

# Button to translate text
if 'current_response' in st.session_state:
    if st.sidebar.button("Translate"):
        if language != "English":
            try:
                translated_response = translator.translate(st.session_state.current_response, dest=language).text
                st.write(f"Translated Solution ({language}):")
                st.success(translated_response)
            except Exception as e:
                st.error(f"Failed to translate: {e}")
        else:
            st.warning("No translation needed; the response is already in English.")

# Button to summarize text
if 'current_response' in st.session_state:
    if st.sidebar.button("Summarize"):
        try:
            summarized_text = summarize_text(st.session_state.current_response)
            st.write("Summarized Solution:")
            st.success(summarized_text)
        except Exception as e:
            st.error(f"Failed to summarize: {e}")

# Button to search for related articles
if st.sidebar.button("Find Articles"):
    if input_text:
        try:
            articles = search_articles(input_text)
            if articles:
                st.write("Related Articles:")
                for title, link in articles:
                    st.markdown(f"[{title}]({link})")
            else:
                st.write("No articles found.")
        except Exception as e:
            st.error(f"Failed to fetch articles: {e}")
    else:
        st.warning("Please describe the issue before searching for articles.")

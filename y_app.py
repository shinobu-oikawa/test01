import openai  
import streamlit as st  
from streamlit_chat import message  
  
openai.api_type = "azure"  
openai.api_base = "https://gpt-mxteam.openai.azure.com/"  
openai.api_version = "2023-03-15-preview"  
openai.api_key = st.secrets.get("AOAI_API_KEY")  
  
response = openai.ChatCompletion.create(
  engine="GPTshinobu",
  messages = [{"role":"system","content":"You are an AI assistant that helps people find information."}],
  temperature=0.7,
  max_tokens=1974,
  top_p=0.95,
  frequency_penalty=0,
  presence_penalty=0,
  stop=None)

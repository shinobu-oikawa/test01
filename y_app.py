import openai
import streamlit as st
from streamlit_chat import message

openai.api_type = "azure"
openai.api_base = "https://gpt-mxteam.openai.azure.com/"
openai.api_version = "2023-03-15-preview"
openai.api_key = st.secrets["AOAI_API_KEY"]

if 'prompts' not in st.session_state:
    st.session_state['prompts'] = [{"role": "system", "content": "あなたは非常に優秀なAIアシスタントです。文系商社マンが納得できるよう説明してくれます。"}]
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []

# Define the 'generate_response' function to send the user's message to the AI model 
# and append the response to the 'generated' list.
def generate_response(prompt):
    st.session_state['prompts'].append({"role": "user", "content":prompt})
    completion=openai.ChatCompletion.create(
        engine="GPTshinobu", # The 'engine' parameter specifies the name of the OpenAI GPT-3.5 Turbo engine to use.
        temperature=0.7, # The 'temperature' parameter controls the randomness of the response.
        max_tokens=512, # The 'max_tokens' parameter controls the maximum number of tokens in the response.
        top_p=0.95, # The 'top_p' parameter controls the diversity of the response.
        # The 'messages' parameter is set to the 'prompts' list to provide context for the AI model.
        messages = st.session_state['prompts']
    )
    # The response is retrieved from the 'completion.choices' list and appended to the 'generated' list.
    message=completion.choices[0].message.content
    return message

user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

         st.write(speaker + ": " + message["content"])

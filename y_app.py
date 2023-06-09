import openai
import streamlit as st
from streamlit_chat import message

openai.api_type = "azure"
openai.api_base = "https://gpt-mxteam.openai.azure.com/"
openai.api_version = "2023-03-15-preview"
openai.api_key = st.secrets["AOAI_API_KEY"]

if 'prompts' not in st.session_state:
st.session_state['prompts'] = [{"role": "system", "content": "あなたは非常に優秀なAIアシスタントです。トップエンジニアが納得できるような説明します。特に定量的に説明するのが好きです。"}]
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
temperature=0.5, # The 'temperature' parameter controls the randomness of the response.
max_tokens=4000, # The 'max_tokens' parameter controls the maximum number of tokens in the response.
top_p=0.95, # The 'top_p' parameter controls the diversity of the response.
# The 'messages' parameter is set to the 'prompts' list to provide context for the AI model.
messages = st.session_state['prompts']
)
# The response is retrieved from the 'completion.choices' list and appended to the 'generated' list.
message=completion.choices[0].message.content
return message

# The 'new_topic_click' function is defined to reset the conversation history and introduce the AI assistant.
def new_topic_click():
st.session_state['prompts'] = [{"role": "system", "content": "あなたは非常に優秀なAIアシスタントです。トップエンジニアが納得できるような説明します。特に定量的に説明するのが好きです。"}]
st.session_state['past'] = []
st.session_state['generated'] = []
st.session_state['user'] = ""

def chat_click():
if st.session_state['user']!= '':
user_chat_input = st.session_state['user']
output=generate_response(user_chat_input)
st.session_state['past'].append({"role": "user", "content": user_chat_input})
st.session_state['generated'].append({"role": "assistant", "content": output})
st.session_state['prompts'].append({"role": "assistant", "content": output})
st.session_state['user'] = ""

# The user's input is retrieved from the 'user' session state.
with st.form(key='user_input_form'):
user_input=st.text_area("You:",height=150, key="user_input")
col1, col2, col3, col4, col5, col6 = st.columns([1,1,1,1,1,1])
with col1:
chat_button=st.form_submit_button("質問する", on_click=chat_click)
with col2:
new_topic_button=st.button("リセット", on_click=new_topic_click)

# The 'message' function is defined to display the messages in the conversation history.
if st.session_state['generated']:
for i in range(len(st.session_state['generated'])):
if st.session_state['generated'][i]["role"] == "assistant":
message(st.session_state['generated'][i]["content"], avatar_style='bottts', key=str(i))
else:
message(st.session_state['generated'][i]["content"], is_user=True, avatar_style='thumbs', key=str(i) + '_user')
```

import openai
import streamlit as st
from streamlit_chat import message

openai.api_type, openai.api_base, openai.api_version, openai.api_key = "azure", "https://gpt4shinobu.openai.azure.com/", "2023-03-15-preview", st.secrets["AOAI_API_KEY"]

st.title("MXTeam GPT-4 32k (Trial ver.)")

session_vars = ['prompts', 'generated', 'past']
for var in session_vars:
    if var not in st.session_state:
        st.session_state[var] = [] if var != 'prompts' else [{"role": "system", "content": "あなたは優秀なAIアシスタントで、箇条書きで非常に詳細に文量多く説明してくれます。"}]

def generate_response(prompt):
    st.session_state['prompts'].append({"role": "user", "content":prompt})
    completion=openai.ChatCompletion.create(engine="GPT4shinobu", temperature=0.7, max_tokens=4000, top_p=0.92, messages = st.session_state['prompts'])
    return completion.choices[0].message.content

def new_topic_click():
    for var in session_vars:
        st.session_state[var] = [] if var != 'prompts' else [{"role": "system", "content": "あなたは優秀なAIアシスタントで、箇条書きで非常に詳細に文量多く説明してくれます。"}]
    st.session_state['user'] = ""

def chat_click():
    if st.session_state['user'] != '':
        output=generate_response(st.session_state['user'])
        st.session_state['past'].append(st.session_state['user'])
        st.session_state['generated'].append(output)
        st.session_state['prompts'].append({"role": "assistant", "content": output})
        st.session_state['user'] = ""

user_input=st.text_area("You:",height=150, key="user")
col1, col2 = st.columns([1,1])
with col1:
    chat_button=st.button("質問する", on_click=chat_click)
with col2:
    new_topic_button=st.button("リセット", on_click=new_topic_click)

if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state['generated'][i], avatar_style='bottts', key=str(i))
        message(st.session_state['past'][i], is_user=True, avatar_style='thumbs', key=str(i) + '_user')

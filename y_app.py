import openai  
import streamlit as st  
from streamlit_chat import message  
  
openai.api_type = "azure"  
openai.api_base = "https://gpt-mxteam.openai.azure.com/"  
openai.api_version = "2023-03-15-preview"  
openai.api_key = st.secrets.get("AOAI_API_KEY")  
  
if 'prompts' not in st.session_state:  
    st.session_state['prompts'] = [{"role": "system", "content": "あなたは非常に優秀なAIアシスタントです。文系商社マンが納得できるよう説明してくれます。"}]  
if 'generated' not in st.session_state:  
    st.session_state['generated'] = []  
if 'past' not in st.session_state:  
    st.session_state['past'] = []  
  
def generate_response(prompt):  
    context = st.session_state['prompts'][-5:]  
    context.append({"role": "user", "content":prompt})  
    completion=openai.Completion.create(  
        engine="GPTshinobu",  
        prompt="\n".join([f"{message['role']}: {message['content']}" for message in context]),  
        temperature=0.7,  
        max_tokens=512,  
        top_p=0.95,  
    )  
    message = completion.choices[0].text.strip()  
    st.session_state['generated'].append(message)  
    return message  
  
   
def communicate():    
    user_input = st.session_state.get("user_input", "")    
    if user_input:    
        response = generate_response(user_input)    
        st.session_state['prompts'].append({"role": "assistant", "content":response})    
        st.session_state.sync()  # st.session_state を更新する  
        st.experimental_rerun()    
    else:    
        st.session_state['user_input'] = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)    
    
if st.session_state["prompts"]:    
    messages = st.session_state["prompts"]    
    
    for message in reversed(messages[1:]):     
        speaker = "🙂"    
        if message["role"]=="assistant":    
            speaker="🤖"    
    
        st.write(speaker + ": " + message["content"])    
    
communicate()  

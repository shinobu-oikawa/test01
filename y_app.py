import openai  
import streamlit as st  
from streamlit_chat import message  
  
openai.api_type = "azure"  
openai.api_base = "https://gpt-mxteam.openai.azure.com/"  
openai.api_version = "2023-03-15-preview"  
openai.api_key = st.secrets.get("AOAI_API_KEY")  
 
  # st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "あなたは優秀なアシスタントAIです。"}
        ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)
    
response = openai.ChatCompletion.create(  
  engine="GPTshinobu",  
  prompt=[{"role":"system","content":"You are an AI assistant that helps people find information."}],  
  temperature=0.7,  
  max_tokens=1974,  
  top_p=0.95,  
  frequency_penalty=0,  
  presence_penalty=0,  
  stop=None,  
  messages=api_messages  
)  
  
bot_message = response["choices"][0]["text"]  
messages.append({"role": "assistant", "content": bot_message})  


st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構築
st.title("My AI Assistant")
st.write("ChatGPT APIを使ったチャットボットです。")

user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])

# https://github.com/kobrinartem/mentalhealth-chatgpt-prototype/blob/main/app/app.py
import streamlit as st
from streamlit_chat import message as st_message
import openai
import json
import time
import ast
import os

#MODEL_ENGINE = "davinci:ft-neurons-lab-2023-01-25-17-40-57"
MODEL_ENGINE = "gpt-3.5-turbo"

# history in dict format for the ChatGPT model
history = [
    {
        "date": time.strftime("%Y-%m-%d, %H:%M:%S"),
        "role": "system",
        "message": """Olá! É um prazer conhecê-lo. Como psicólogo profissional, meu objetivo é ajudá-lo a melhorar sua saúde mental e bem-estar.
Para começar, como você está se sentindo hoje? É importante verificar com nós mesmos e nossas emoções regularmente.""",
    }
]

MESSAGE_TEMPLATE = """Forneça a próxima réplica como psicólogo profissional para a conversa no seguinte formato JSON:
```json
{{
    "date": "2023-08-01, 12:00:00",
    "role": "system",
    "message": "Olá! É um prazer conhecê-lo. Como psicólogo profissional, meu objetivo é ajudá-lo a melhorar sua saúde mental e bem-estar.
Para começar, como você está se sentindo hoje? É importante verificar com nós mesmos e nossas emoções regularmente."
}}
```

SEMPRE inclua em sua mensagem a pergunta e envolva a continuação da conversa. A conversa atual apresentada no formato JSON:
```json
{}
```

"""

# Set the page title and icon
st.set_page_config(page_title="I2A2 Psicologo Chat - Desafio 2", page_icon=":robot:")

# OpenAI API key
openai.api_key = os.environ['OPENAI_KEY']

# Set the page header
st.header("I2A2 Psicologo Chat - Desafio 2")
styl = f"""
<style>
    .stTextInput {{
      position: fixed;
      bottom: 3rem;
    }}
</style>
"""
st.markdown(styl, unsafe_allow_html=True)

# Initialize the session state
if "history" not in st.session_state:
    st.session_state["history"] = history

messages=[
    {"role": "system", "content": "Você é um psicólogo renomado com especialização. Responda o paciente com até 30 palavras."},
]
# ChatGPT query function
def query(message):
    response = openai.ChatCompletion.create(
        model=MODEL_ENGINE,
        messages=[
            {
                "role": "system",
                "content": "Você é um psicólogo renomado com especialização em adolescente. Responda o paciente com até 30 palavras."
            },
            {
                "role": "user",
                "content": f"{message}"
            },
        ],
        temperature=0.7
    ).choices[0]
    return response.message.content


# Get the user's message and return it as a dict
def get_patient_message():
    message = st.chat_input("Como posso ajudar?")
    if message:
        message_dict = {
            "date": time.strftime("%Y-%m-%d, %H:%M:%S"),
            "role": "user",
            "message": message,
        }
        return message_dict
    else:
        return {}


# Get the bot's message and return it as a dict
def get_bot_message(json_message):
    # Try to parse the JSON message
    try:
        message = ast.literal_eval(json_message)
    except Exception as e:
        print(e)
        st.markdown(f"**BEGINNING DEBUG**\n```{json_message}```\n**END DEBUG**")
        raise e
    message_dict = {
        "date": time.strftime("%Y-%m-%d, %H:%M:%S"),
        "role": "system",
        "message": message["message"],
    }
    return message_dict


# Create the history for the ChatGPT model
def create_history(history):
    json.dumps(history, indent=4, sort_keys=True)
    return history


# Get the user's message
user_input = get_patient_message()

if user_input:
    st.session_state.history.append(user_input)
    prompt = MESSAGE_TEMPLATE.format(create_history(st.session_state["history"]))
    output = get_bot_message(query(prompt))
    st.session_state.history.append(output)

if st.session_state["history"]:
    history = st.session_state["history"]
    for i in range(len(history)):
        item = history[i]
        if(item["role"]=="system"):
            st_message(f'{item["message"]}', key=i)
        else:
            st_message(f'{item["message"]}', is_user=True, key=f"{str(i)}_user")
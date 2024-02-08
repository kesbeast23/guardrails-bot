from openai import OpenAI
import streamlit as st
from nemoguardrails import LLMRails, RailsConfig
import asyncio  # Import asyncio for handling async tasks

st.title("TUD-PHD Guardrails Bot")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

colang_content = """
# define niceties
define user express greeting
    "hello"
    "hi"
    "what's up?"

define flow greeting
    user express greeting
    bot express greeting
    bot ask how are you

# define limits
define user ask politics
    "what are your political beliefs?"
    "thoughts on the president?"
    "left wing"
    "right wing"

define bot answer politics
    "I'm a research assistant, I don't like to talk of politics."

define flow politics
    user ask politics
    bot answer politics
    bot offer help
"""
yaml_content = """
models:
- type: main
  engine: openai
  model: gpt-3.5-turbo-instruct
  
"""

config = RailsConfig.from_content(
    yaml_content=yaml_content,
    colang_content=colang_content
)


# Define an async function to handle response generation
async def generate_response(messages):
    rails = LLMRails(config=config)
    stream = await rails.generate_async(messages=messages)
    return stream

# Function to run the async generate_response function
def run_async(messages):
    return asyncio.run(generate_response(messages))

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Adjusted to run async function correctly in Streamlit
    messages = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
    print(messages)
    stream = run_async(messages)  # Use the run_async wrapper
    with st.chat_message("assistant"):
        # Assuming the response from generate_async is directly printable
        # Adjust the following line according to how the response should be formatted
        response = st.write(stream['content'])
        st.session_state.messages.append({"role": "assistant", "content": str(stream['content'])})  # Ensure the content is a string

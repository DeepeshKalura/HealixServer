import streamlit as st
import websockets
import asyncio

st.title("Healix")
st.markdown("Welcome to Healix Chat! Type your messages below.")

# Initialize history
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Function to send and receive messages through WebSocket
def send_receive_ws_message(prompt):
    uri = "ws://127.0.0.1:8000/text"  
    response = None
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        response = loop.run_until_complete(send_receive_ws_message_async(prompt))
    except Exception as e:
        st.error(f"Error connecting to WebSocket: {e}")
    return response

async def send_receive_ws_message_async(prompt):
    uri = "ws://127.0.0.1:8000/text"  
    async with websockets.connect(uri) as ws:
        await ws.send(prompt)
        response_str = await ws.read_message()
    return response_str  # Return the string response

# Chat input
if prompt := st.chat_input("Message Healix"):
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Send user message to FastAPI WebSocket and get response
    response = send_receive_ws_message(prompt)

    # Display assistant response in chat message container
    with st.spinner("Waiting for response..."):
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

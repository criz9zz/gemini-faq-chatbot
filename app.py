
import streamlit as st
from google import genai

api_key = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=api_key)

business_faqs = """
Business Name: ABC Clothing Store
Opening Hours: 9 AM to 9 PM
Location: Kozhikode, Kerala
Delivery: Available across Kerala
Payment: UPI, Cash and Cards
Returns: Returns accepted within 7 days
"""

st.title("ABC Clothing Store")
st.write("Welcome! Ask us any question.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

question = st.chat_input("Type your question here...")

if question:
    st.session_state.messages.append(
        {"role": "user", "content": question}
    )

    prompt = f"""
    Answer using ONLY these business details:
    {business_faqs}

    If the answer is unavailable, say:
    Sorry, please contact our store for more information.

    Customer question: {question}
    """

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )

    answer = response.text

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )

    st.rerun()

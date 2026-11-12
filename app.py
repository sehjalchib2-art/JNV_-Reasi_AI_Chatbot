
import streamlit as st
import joblib
import json
import random

# Load trained machine learning model
model = joblib.load("model.pkl")

# Load school information
with open("school_data.json", "r") as file:
    school_info = json.load(file)

# School answers
school_answers = {
    "admission": "For admission details, please contact the school office.",
    "fees": "For fee details, contact the accounts office.",
    "library": "Our school library provides books and reading materials.",
    "exam": "Please check the official examination timetable.",
    "principal": f"The principal of our school is {school_info['principal']}.",
    "holidays": "Please check the official school holiday calendar.",
    "sports": "Our school encourages students to participate in sports.",
    "teachers": "Our teachers guide students in their academic activities.",
    "timings": "Please contact the school office for accurate timings.",
    "transport": "For transport details, contact the school office."
}

# Conversation responses
def conversation_response(question):
    q = question.lower().strip()

    if q in ["hi", "hello", "hey"]:
        return "Hello! Welcome to JNV Reasi. How can I help you?"

    elif "thank" in q:
        return "You're most welcome! Happy to help."

    elif "who are you" in q:
        return "I am the AI School Assistant of Jawahar Navodaya Vidyalaya, Reasi."

    elif "your name" in q:
        return "You can call me JNV AI Assistant!"

    elif "what can you do" in q:
        return "I can answer questions about admission, fees, library, exams, teachers, sports and more."

    else:
        return None

# Personal information responses
def personal_response(question):
    q = question.lower().strip()

    if any(x in q for x in ["who made you", "your developers",
                              "who created you", "who developed you",
                              "who built you"]):

        names = ", ".join(school_info["developers"])

        return (
            f"I was developed by {names}, students of "
            f"{school_info['name']}, under the guidance of "
            f"{school_info['ai_teacher']}."
        )

    elif "principal" in q:
        return f"The principal of our school is {school_info['principal']}."

    elif any(x in q for x in ["ai teacher", "project guide"]):
        return f"My project guide is {school_info['ai_teacher']}."

    elif any(x in q for x in ["school name", "about your school", "which school"]):
        return (
            f"I am the AI assistant of {school_info['name']}, "
            f"located in {school_info['location']}."
        )

    elif "motto" in q:
        return f"Our school motto is {school_info['motto']}."

    elif any(x in q for x in ["facilities", "facility"]):
        facilities = ", ".join(school_info["facilities"])
        return f"Our school facilities include: {facilities}."

    return None

# Website design
st.set_page_config(
    page_title="JNV Reasi AI Assistant",
    page_icon="🏫"
)

st.title("🏫 JNV Reasi AI School Assistant")
st.caption("Your smart school information assistant")

st.info("Ask me about admission, fees, exams, library, sports and more.")

# Store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
if prompt := st.chat_input("Type your question here..."):

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.write(prompt)

    # Generate response
    response = conversation_response(prompt)

    if response is None:
        response = personal_response(prompt)

    if response is None:
        probabilities = model.predict_proba([prompt])
        confidence = max(probabilities[0])

        if confidence >= 0.40:
            category = model.predict([prompt])[0]
            response = school_answers.get(
                category,
                "Please contact the school office for more information."
            )
        else:
            response = "Sorry, I couldn't understand that. Please ask me about JNV Reasi."

    st.session_state.messages.append({
        "role": "assistant",

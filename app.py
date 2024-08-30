import streamlit as st
import os
import google.generativeai as genai

API_KEY = "AIzaSyCThnASZ53viHUOfF7sqIBcc2-hBNLfZyw"

# Configure API key
genai.configure(api_key=API_KEY)

# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction=(
        "You are a letter generation assistant. Your task is to create personalized and professional letters based on the details provided by the user. "
        "Focus on the main purpose of the letter, such as an application, apology, or recommendation. Incorporate the key content provided by the user and adjust the tone and style accordingly (e.g., formal or friendly). "
        "Since specific recipient and sender details will not be provided, use general placeholders or salutation and sign-off formats like \"Dear [Recipient],\" and \"Sincerely, [Your Name].\" Ensure the letter is well-structured, clear, and tailored to its purpose."
    ),
)

def generate_letter(user_input):
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    "hi",
                ],
            },
            {
                "role": "model",
                "parts": [
                    "Please tell me what kind of letter you need help writing! For example, are you writing:\n\n"
                    "* **A job application?** Tell me about the position you're applying for and your relevant qualifications.\n"
                    "* **A letter of apology?** Tell me what you're apologizing for and what you plan to do to make things right.\n"
                    "* **A letter of recommendation?** Tell me about the person you're recommending and their strengths.\n"
                    "* **A formal complaint?** Tell me what the issue is and what you'd like to see happen.\n\n"
                    "The more information you give me, the better I can help you write a personalized and professional letter. 😊\n",
                ],
            },
            {
                "role": "user",
                "parts": [
                    user_input,
                ],
            },
        ]
    )

    response = chat_session.send_message("INSERT_INPUT_HERE")
    return response.text

# Streamlit UI
st.title('Letter Generator')
st.write(
    "Please tell me what kind of letter you need help writing! For example, are you writing:\n\n"
    "* **A job application?** Tell me about the position you're applying for and your relevant qualifications.\n"
    "* **A letter of apology?** Tell me what you're apologizing for and what you plan to do to make things right.\n"
    "* **A letter of recommendation?** Tell me about the person you're recommending and their strengths.\n"
    "* **A formal complaint?** Tell me what the issue is and what you'd like to see happen.\n\n"
    "The more information you give me, the better I can help you write a personalized and professional letter. 😊"
)

user_input = st.text_area("Enter the details for your letter:")

if st.button('Generate Letter'):
    if user_input:
        result = generate_letter(user_input)
        st.subheader('Generated Letter')
        st.write(result)
    else:
        st.error('Please provide the details for your letter.')


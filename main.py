import os
import streamlit as st
from functions.vectorstore import (
    get_pdf_text,
    get_text_chunks,
    get_vectorstore,
    get_conversation_chain,
    handle_userinput,
)
from PIL import Image
from dotenv import load_dotenv

load_dotenv()


api_key = os.getenv("OPENAI_API_KEY")


def main():
    favicon = Image.open("favicon.png")
    st.set_page_config(
        page_title="GenAI Demo | Trigent AXLR8 Labs",
        page_icon=favicon,
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Sidebar Logo
    logo_html = """
    <style>
        [data-testid="stSidebarNav"] {
            background-image: url(https://trigent.com/wp-content/uploads/Trigent_Axlr8_Labs.png);
            background-repeat: no-repeat;
            background-position: 20px 20px;
            background-size: 80%;
        }
    </style>
    """
    st.sidebar.markdown(logo_html, unsafe_allow_html=True)
    st.title("Legal document summarizer 📗")
    if api_key:
        success_message_html = """
        <span style='color:green; font-weight:bold;'>✅ Powering the Chatbot using Open AI's 
        <a href='https://platform.openai.com/docs/models/gpt-3-5' target='_blank'>gpt-3.5-turbo-0613 model</a>!</span>
        """

        # Display the success message with the link
        st.markdown(success_message_html, unsafe_allow_html=True)
        openai_api_key = api_key
    else:
        openai_api_key = st.text_input("Enter your OPENAI_API_KEY: ", type="password")
        if not openai_api_key:
            st.warning("Please, enter your OPENAI_API_KEY", icon="⚠️")
            stop = True
        else:
            st.success("Ask Tech voice assistant about your software.", icon="👉")

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    pdf_docs = st.file_uploader("Upload you pdf here 📝")
    if st.button("Summarize"):
        with st.spinner("summarizing 💡..."):
            raw_text = get_pdf_text(pdf_docs)

            text_chunks = get_text_chunks(raw_text)

            vectorstore = get_vectorstore(text_chunks)

            st.session_state.conversation = get_conversation_chain(vectorstore)

            handle_userinput("summarize the document")

    if st.session_state.conversation:
        st.subheader("Summary of the Document")
        for message in st.session_state["chat_history"]:
            st.write(message.content)

    # Footer
    footer_html = """
    <div style="text-align: right; margin-right: 10%;">
        <p>
            Copyright © 2024, Trigent Software, Inc. All rights reserved. | 
            <a href="https://www.facebook.com/TrigentSoftware/" target="_blank">Facebook</a> |
            <a href="https://www.linkedin.com/company/trigent-software/" target="_blank">LinkedIn</a> |
            <a href="https://www.twitter.com/trigentsoftware/" target="_blank">Twitter</a> |
            <a href="https://www.youtube.com/channel/UCNhAbLhnkeVvV6MBFUZ8hOw" target="_blank">YouTube</a>
        </p>
    </div>
    """

    # Custom CSS to make the footer sticky
    footer_css = """
    <style>
    .footer {
        position: fixed;
        z-index: 1000;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: white;
        color: black;
        text-align: center;
    }
    [data-testid="stSidebarNavItems"] {
        max-height: 100%!important;
    }
    </style>
    """

    # Combining the HTML and CSS
    footer = f"{footer_css}<div class='footer'>{footer_html}</div>"

    # Rendering the footer
    st.markdown(footer, unsafe_allow_html=True)


if __name__ == "__main__":
    main()

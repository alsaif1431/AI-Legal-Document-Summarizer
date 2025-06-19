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


def main():
    # Set up favicon and page configuration
    st.set_page_config(
        page_title="Legal Document Summarizer",
        page_icon="📔",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # -------------------------------
    # Updated Sidebar Content
    # -------------------------------
    st.sidebar.markdown(
        """
        <div style="background-color: #e0f7fa; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
            <h2 style="text-align: center; color: #00796b;">Legal Document Summarizer</h2>
            <p style="text-align: center; font-size: 14px; color: #004d40;">
                Welcome to our AI-powered legal document summarizer. Upload your PDF files to receive concise, insightful summaries in seconds.
            </p>
        </div>
        <div style="background-color: #ffffff; padding: 15px; border-radius: 10px;">
            <h4 style="color: #00796b;">Features</h4>
            <ul style="font-size: 13px; color: #004d40; line-height: 1.6;">
                <li>Extract text from PDF documents</li>
                <li>Efficient text chunking for processing</li>
                <li>AI-generated document summaries</li>
                <li>User-friendly and intuitive interface</li>
            </ul>
            <hr style="border-top: 1px solid #ccc;">
            <h4 style="color: #00796b;">How It Works</h4>
            <p style="font-size: 12px; color: #004d40;">
                Simply upload your legal PDF, click "Summarize", and let the AI do the rest!
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # -------------------------------
    # Main App Content
    # -------------------------------
    st.title("Legal Document Summarizer 📗")

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    pdf_docs = st.file_uploader("Upload your PDF here 📝", type=["pdf"])
    if st.button("Summarize"):
        if pdf_docs is not None:
            with st.spinner("Summarizing the document..."):
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunks(raw_text)
                vectorstore = get_vectorstore(text_chunks)
                st.session_state.conversation = get_conversation_chain(vectorstore)
                handle_userinput("summarize the document")
        else:
            st.error("Please upload a PDF document.")

    if st.session_state.conversation and st.session_state.chat_history:
        st.subheader("Summary of the Document")
        for message in st.session_state.chat_history:
            st.write(message.content)

    # -------------------------------
    # Updated Footer with LinkedIn and Github
    # -------------------------------
    footer_html = """
    <div style="text-align: center; margin: 10px;">
        <p>
            © 2024. All rights reserved. | 
            <a href="https://www.linkedin.com/in/saif-pasha-59643b197/" target="_blank">LinkedIn</a> | 
            <a href="https://github.com/alsaif1431" target="_blank">Github</a>
        </p>
    </div>
    """
    footer_css = """
    <style>
    .footer {
        position: fixed;
        z-index: 1000;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #f1f1f1;
        color: #333;
        text-align: center;
        padding: 10px 0;
    }
    </style>
    """
    footer = f"{footer_css}<div class='footer'>{footer_html}</div>"
    st.markdown(footer, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

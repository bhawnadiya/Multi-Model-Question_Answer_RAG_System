import streamlit as st
import os
from QAWithPDF.data_ingestion import load_data
from QAWithPDF.embedding import download_gemini_embedding
from QAWithPDF.model_api import load_model

def main():
    st.set_page_config(page_title="📄 Enterprise Multi-Modal Document Q&A", layout="wide")

    # Initialize session state
    if "query_engine" not in st.session_state:
        st.session_state.query_engine = None
    if "processed_file" not in st.session_state:
        st.session_state.processed_file = None

    st.title("📄 Enterprise Multi-Modal Document Q&A System")
    st.markdown("""
    Upload your documents and ask questions based on the content inside.  
    **Supported formats:** PDF, DOCX, XLSX, CSV, TXT, PPTX, Images,  Emails etc.  
    Max File Size: **200MB**
    """)

    st.header("📤 Upload Documents")
    uploaded_file = st.file_uploader("Drag & drop your file here or click to browse", 
                                     type=["doc", "docx", "txt", "msg", "pdf", "png", "jpeg", "jpg", "eml", "xlsx", "csv", "ppt", "pptx"])

    if uploaded_file:
        # Get file extension
        file_ext = os.path.splitext(uploaded_file.name)[1].lower()
        
        # Check if new file or same as previously processed
        if st.session_state.processed_file != uploaded_file.name:
            st.success(f"✅ Uploaded: {uploaded_file.name}")
            with st.spinner("🔄 Processing document..."):
                try:
                    # Reset the file pointer to beginning to avoid read errors
                    uploaded_file.seek(0)
                    document_chunks = load_data(uploaded_file)
                    model = load_model()
                    st.session_state.query_engine = download_gemini_embedding(model, document_chunks)
                    st.session_state.processed_file = uploaded_file.name
                    st.success("✅ Document processed successfully!")
                except Exception as e:
                    st.error(f"❌ Processing error: {str(e)}")
                    st.session_state.query_engine = None
        else:
            st.info("ℹ️ Using previously processed document")

        st.header("❓ Ask Questions About Your Documents")
        user_question = st.text_input("Enter your question")

        if st.button("Submit Question"):
            if not st.session_state.query_engine:
                st.warning("⚠️ Document not processed. Please re-upload.")
            elif user_question.strip() == "":
                st.warning("⚠️ Please enter a valid question.")
            else:
                with st.spinner("🤖 Generating answer..."):
                    try:
                        response = st.session_state.query_engine.query(user_question)
                        
                        # Display answer
                        st.subheader("📘 Answer")
                        st.markdown(response.response)

                        # Display metadata if available
                        if hasattr(response, "metadata"):
                            metadata = response.metadata
                            if 'page_label' in metadata:
                                st.info(f"📄 Page: {metadata['page_label']}")
                            elif 'page' in metadata:
                                st.info(f"📄 Page: {metadata['page']}")
                            if 'source' in metadata:
                                st.caption(f"📌 Source: {metadata['source']}")
                                
                    except Exception as e:
                        st.error(f"❌ Error generating answer: {str(e)}")

    else:
        st.warning("⚠️ Please upload a document before asking questions.")

if __name__ == "__main__":
    main()
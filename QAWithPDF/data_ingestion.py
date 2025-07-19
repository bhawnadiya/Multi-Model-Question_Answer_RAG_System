# from llama_index.core import SimpleDirectoryReader
# import sys
# from exception import customexception
# from logger import logging

# def load_data(data):
#     try:
#         logging.info("data loading started...")
#         loader = SimpleDirectoryReader("Data")
#         documents=loader.load_data()
#         logging.info("data loading completed...")
#         return documents
#     except Exception as e:
#         logging.info("exception in loading data...")
#         raise customexception(e,sys)

# from llama_index.core import SimpleDirectoryReader
# import sys
# from exception import customexception
# from logger import logging

# def load_data(data):
#     try:
#         logging.info("data loading started...")
#         loader = SimpleDirectoryReader("Data")
#         documents=loader.load_data()
#         logging.info("data loading completed...")
#         return documents
#     except Exception as e:
#         logging.info("exception in loading data...")
#         raise customexception(e,sys)

import os
import tempfile
import sys
import shutil
from exception import customexception
from logger import logging
from llama_index.core import SimpleDirectoryReader

# Supported file extensions
VALID_EXTENSIONS = [
    ".pdf", ".docx", ".doc", ".xlsx", ".xls", ".ppt", ".pptx", 
    ".jpg", ".jpeg", ".png", ".eml", ".msg", ".txt", ".csv"
]

def load_data(uploaded_file):
    try:
        logging.info("Data loading started...")
        
        # Validate file type
        file_ext = os.path.splitext(uploaded_file.name)[1].lower()
        if file_ext not in VALID_EXTENSIONS:
            raise ValueError(f"❌ Unsupported file type: {file_ext}. Supported types: {', '.join(VALID_EXTENSIONS)}")
        
        # Create temporary file with proper extension
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp_file:
            # Handle both in-memory and on-disk files
            if hasattr(uploaded_file, 'read'):
                # For file-like objects
                shutil.copyfileobj(uploaded_file, tmp_file)
            else:
                # For direct file paths (not used in Streamlit, but safe)
                with open(uploaded_file, 'rb') as f:
                    shutil.copyfileobj(f, tmp_file)
            
            tmp_file_path = tmp_file.name
        
        # Load from temporary path
        loader = SimpleDirectoryReader(input_files=[tmp_file_path])
        documents = loader.load_data()
        
        # Cleanup temporary file
        os.unlink(tmp_file_path)
        
        logging.info("Data loading completed...")
        return documents
    except Exception as e:
        logging.error(f"Exception in loading data: {str(e)}")
        raise customexception(e, sys)

    

    
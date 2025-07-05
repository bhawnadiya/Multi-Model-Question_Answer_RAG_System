import os
from pathlib import Path
import logging
list_of_files=[
    "QAWithPDF/_init__.py",
    "QAWithPDF/data_ingestion.py",
    "QAWithPDF/embedding.py",
    "QAWithPDF/model_api.py",
    "Experiments/experiment.ipynb",
    "StreamlitApp.py",
    "logger.py",
    "exception.py",
    "setup.py"
]
for filepath in list_of_files:
    filepath = Path(filepath)
    filedir,filename = os.path.split(filepath)

    if filedir!="":
        os.makedirs(filedir,exist_ok=True)
        logging.info(f"Creating Directory; {filedir} for the file {filename}")
    
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, 'w') as f:
            pass
    else:
        logging.info(f"{filename} is already created")
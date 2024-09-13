import os
import pandas as pd
from PIL import Image
import numpy as np
import pdfplumber

def ingest_data_from_directory(directory_path):
    """
    Ingests data from all files in the specified directory and its subdirectories based on their extensions.

    Parameters:
    directory_path (str): Path to the directory containing data files.

    Returns:
    dict: A dictionary where keys are file names and values are the data loaded from those files.
    """
    data_dict = {}

    # Helper function to process files and directories recursively
    def process_directory(path):
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                # Recursively process subdirectory
                process_directory(item_path)
            elif os.path.isfile(item_path):
                try:
                    if item.endswith('.csv'):
                        data = pd.read_csv(item_path)
                    elif item.endswith('.json'):
                        data = pd.read_json(item_path)
                    elif item.endswith('.xlsx') or item.endswith('.xls'):
                        data = pd.read_excel(item_path)
                    elif item.endswith('.parquet'):
                        data = pd.read_parquet(item_path)
                    elif item.endswith('.txt'):
                        with open(item_path, 'r') as file:
                            data = file.read()  # Read the entire file as a string
                    elif item.endswith('.jpg') or item.endswith('.jpeg'):
                        img = Image.open(item_path)
                        data = np.array(img)  # Convert image to numpy array
                    elif item.endswith('.pdf'):
                        # Extract text from PDF
                        with pdfplumber.open(item_path) as pdf:
                            text = ''
                            for page in pdf.pages:
                                text += page.extract_text() or ''  # Append text from each page
                            data = text
                    else:
                        raise ValueError("Unsupported file format: " + item.split('.')[-1])
                    
                    data_dict[item_path] = data
            
                except Exception as e:
                    print(f"Error reading file {item_path}: {e}")
                    data_dict[item_path] = None  # Indicate an issue with this file

    # Start processing from the root directory
    process_directory(directory_path)

    return data_dict

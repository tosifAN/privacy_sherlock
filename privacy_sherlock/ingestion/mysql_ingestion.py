import pandas as pd
import mysql.connector
import MySQLdb
from PIL import Image
import io
import easyocr

def extract_text_from_image(binary_data):
    reader = easyocr.Reader(['en'])  # Initialize the reader with the desired language(s)
    
    # Convert binary data to an image
    image = Image.open(io.BytesIO(binary_data))
    
    # Perform OCR on the image
    result = reader.readtext(image)
    
    # Combine extracted text
    text = '\n'.join([line[1] for line in result])
    return text

def ingest_data_from_mysql(db_config, query):
    try:
        connection = mysql.connector.connect(**db_config)
        data = pd.read_sql(query, connection)
        print("Data ingested from MySQL",data)
        connection.close()
        return data
    except Exception as e:
        print(f"Error ingesting data from MySQL: {e}")
        return None


def ingest_data_from_specific_database(db_config, database_name):
    # Update the db_config to use the specified database
    db_config['db'] = database_name
    try:
        # Establish connection to MySQL
        connection = MySQLdb.connect(**db_config)
        cursor = connection.cursor()

        # Step 1: Get all tables in the specific database
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()

        db_data = {}

        # Step 2: Loop through each table and retrieve data
        for table in tables:
            table_name = table[0]
            print(f"Fetching data from table: {table_name}")
            
            # Fetch all data from the table
            query = f"SELECT * FROM {table_name}"
            data = pd.read_sql(query, connection)

              
            # Check if the table has an 'image_data' column
            if 'image_data' in data.columns:
                # Apply the OCR function to the 'image_data' column
                data['image_text'] = data['image_data'].apply(lambda x: extract_text_from_image(x))
                # Drop the 'image_data' column if you no longer need it
                data = data.drop(columns=['image_data'])
            
            # Store the data in a dictionary with the table name as key
            db_data[table_name] = data

        # Close the connection
        connection.close()
        
        return db_data
    
    except Exception as e:
        print(f"Error: {e}")
        return None

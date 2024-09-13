import mysql.connector

def insert_image(db_config, file_path, image_name, image_type):
    try:
        # Connect to MySQL
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Read the image file as binary data
        with open(file_path, 'rb') as file:
            binary_data = file.read()

        # Insert the binary data into the database
        query = "INSERT INTO images (name, image_type, image_data) VALUES (%s, %s, %s)"
        cursor.execute(query, (image_name, image_type, binary_data))
        connection.commit()

        print(f"Image '{image_name}' inserted successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'Tosif@123',
        'database' : 'data'
    }

file_path = 'pancard.jpeg'  # Path to the image file
image_name = 'pancard.jpg'  # Image name to be stored in the database
image_type = 'image/jpeg'  # MIME type of the image

insert_image(db_config, file_path, image_name, image_type)

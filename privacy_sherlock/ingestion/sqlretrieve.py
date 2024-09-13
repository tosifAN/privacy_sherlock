import MySQLdb
from PIL import Image
import pytesseract
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



def fetch_and_extract_text(db_config, image_name):
    connection = None
    cursor = None
    try:
        print("Connecting to MySQL...")
        # Connect to MySQL using mysqlclient
        connection = MySQLdb.connect(
            host=db_config['host'],
            user=db_config['user'],
            passwd=db_config['password'],
            db=db_config['database']
        )
        cursor = connection.cursor()

        print("Fetching image data...")
        # Fetch the image data
        query = "SELECT image_data FROM images WHERE name = %s"
        cursor.execute(query, (image_name,))
        result = cursor.fetchone()

        if result:
            binary_data = result[0]

            # Convert binary data to an image
            image = Image.open(io.BytesIO(binary_data))

            # Perform OCR on the image
            print("Extracting text from image...")
            text = extract_text_from_image(binary_data)
            print(f"Extracted Text from '{image_name}':")
            print(text)
            return text
        else:
            print(f"Image '{image_name}' not found.")
            return None

    except MySQLdb.Error as err:
        print(f"Error: {err}")
        return None

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# Example usage
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Tosif@123',
    'database': 'data'
}
image_name = 'example_image.jpg'  # Name of the image in the database

fetch_and_extract_text(db_config, image_name)

import boto3
import pdfplumber
import io
from PIL import Image
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

def ingest_data_from_s3(bucket_name, aws_access_key, aws_secret_key):
    try:
        # Create S3 client
        s3 = boto3.client('s3', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)
        print("S3 client initialized")
        
        # List all objects in the bucket
        response = s3.list_objects_v2(Bucket=bucket_name)
        if 'Contents' not in response:
            print("No files found in the bucket.")
            return None
        
        all_text = ""
        
        for obj in response['Contents']:
            file_key = obj['Key']
            print(f"Processing file: {file_key}")
            
            # Get file from S3
            response = s3.get_object(Bucket=bucket_name, Key=file_key)
            file_content = response['Body'].read()
            
            # Determine file type and process accordingly
            if file_key.lower().endswith('.pdf'):
                # Process PDF file
                with pdfplumber.open(io.BytesIO(file_content)) as pdf:
                    file_text = ""
                    for page in pdf.pages:
                        file_text += page.extract_text()
                    all_text += f"\n\n--- End of File: {file_key} (PDF) ---\n\n"
                    all_text += file_text
            
            elif file_key.lower().endswith('.txt'):
                # Process text file
                file_text = file_content.decode('utf-8')
                all_text += f"\n\n--- End of File: {file_key} (Text) ---\n\n"
                all_text += file_text
            
            elif file_key.lower().endswith(('.jpg', '.jpeg', '.png')):
                # Process image file using OCR
                file_text = extract_text_from_image(file_content)
                all_text += f"\n\n--- End of File: {file_key} (Image) ---\n\n"
                all_text += file_text
                
            else:
                all_text += f"\n\n--- End of File: {file_key} (Unknown Type) ---\n\n"
                all_text += "Unsupported file type."
        
      
        return all_text
    except Exception as e:
        print(f"Error ingesting data from S3: {e}")
        return None

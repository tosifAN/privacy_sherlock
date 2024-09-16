# IDfy Hackathon - Privacy Sherlock

## PII Detection and Analysis

This project is a **Streamlit web app** that allows users to connect with various data sources like **MySQL**, **Amazon S3**, and **MongoDB**, load data, detect **Personally Identifiable Information (PII)**, classify it into different categories (financial, personal, etc.), and visualize the results.

### Features

- **MySQL Data Loading**: Connect to a MySQL database and load data via a SQL query.
- **Amazon S3 Data Loading**: Connect to an Amazon S3 bucket and load CSV files.
- **MongoDB Data Loading**: Connect to a MongoDB instance, load data from a specific collection.
- **PII Detection**: Detect PII using regular expressions (e.g., email, PAN, Aadhaar, credit card numbers).
- **PII Classification**: Classify the detected PII into categories like **financial** and **personal**.
- **Data Visualization**: Visualize the PII classification with an interactive pie chart.

### Technologies Used

- **Streamlit** for building the web app UI.
- **MySQL Connector** for interacting with MySQL databases.
- **Boto3** for accessing Amazon S3 buckets.
- **PyMongo** for connecting to MongoDB.
- **Pandas** for data manipulation.
- **Plotly** for data visualization.
- **Regular Expressions (Regex)** for PII detection.

### Installation

#### 1. Clone the Repository

        ```bash
        git clone https://github.com/tosifAN/privacy_sherlock.git
        cd privacy_sherlock
        ```

#### 2. Create a Virtual Environment and Activate It

# Install virtualenv if not already installed
```bash
pip install virtualenv
```

# Create a virtual environment
```bash
virtualenv venv
```

# Activate the virtual environment

# On Windows:
```bash
venv\Scripts\activate
```

# On macOS/Linux:
```bash
source venv/bin/activate
```

#### 3. Install Dependencies
 ```bash
 pip install -r requirements.txt
 ```

#### 4. Run the Streamlit App
``` bash
streamlit run app.py
```

The app will open in your default web browser at http://localhost:8501.

### Usage Instructions

#### MySQL Data Loading
Enter your MySQL connection details (host, user, password, database).
Write your SQL query (e.g., SELECT * FROM users).
Click "Load MySQL Data" to load and display the data.
#### Amazon S3 Data Loading
Enter your AWS Access Key and Secret Key.
Provide your S3 Bucket Name and File Key (the path to your CSV file in S3).
Click "Load Amazon S3 Data" to load and display the data.
#### MongoDB Data Loading
Enter your MongoDB URI, Database Name, and Collection Name.
Click "Load MongoDB Data" to load and display the data.
#### Extract PII
Once the data is loaded from any source, click "Extract PII".
The app will automatically detect PII based on predefined regular expressions.
#### Classify and Visualize PII
After extracting PII, click "Classify PII".
The app will classify the PII into categories (financial, personal, etc.).
A pie chart will be displayed to visualize the distribution of PII categories.

### Project Structure
```bash 
privacy_sherlock/
│
├── app.py                     # Streamlit app main file
├── ingestion/                  # Scripts for data ingestion
│   ├── mysql_ingestion.py
│   ├── s3_ingestion.py
├── detection/                  # PII detection logic
│   ├── regex_pii_detection.py
├── classification/             # PII classification logic
│   ├── classify_pii.py
├── risk_assessment/            # Risk assessment functions
│   ├── risk_score.py
├── visualization/              # Visualization scripts
│   ├── plot_pii_distribution.py
├── tests/                      # Unit tests for various modules
├── config/                     # Configurations for DB and S3
│   ├── db_config.json
│   ├── s3_config.json
├── requirements.txt            # Project dependencies
└── README.md                   # Project documentation

```

### Future Enhancements
Machine Learning PII Detection: Extend the PII detection using machine learning or NLP techniques.
Advanced Risk Scoring: Enhance the risk scoring mechanism by integrating frameworks like FAIR.
Improved Visualizations: Add more data visualizations for risk assessment and data insights.

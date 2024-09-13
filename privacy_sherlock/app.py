import streamlit as st
import pandas as pd
import plotly.express as px

# Importing custom modules
from detection.regex_pii_detection import detect_pii
from classification.classify_pii import classify_pii
from risk_assessment.risk_score import calculate_risk_score
from ingestion.mysql_ingestion import ingest_data_from_specific_database
from ingestion.s3_ingestion import ingest_data_from_s3
from ingestion.mongo_ingestion import ingest_data_from_mongodb
from detection.presidio_helpers import analyze, annotate
from annotated_text import annotated_text
from ai.groqai import getResponse

# Initialize session states
if 'main_data' not in st.session_state:
    st.session_state.update({
        'main_data': "",
        'pii_data': pd.DataFrame(),
        'show_docs': False,
        'ai_responses': []
    })

# Title and Header
st.title("PII Detection and Analysis")

# Documentation section
if st.button("Expand/Collapse Documentation"):
    st.session_state.show_docs = not st.session_state.show_docs

if st.session_state.show_docs:
    st.markdown("""
    ## Documentation for PII Detection and Analysis App
    ### Overview
    This app performs the following functions:
    1. **Data Ingestion**: Load data from MySQL, Amazon S3, or MongoDB.
    2. **PII Extraction**: Extract PII from the ingested data.
    3. **PII Classification**: Classify the extracted PII into categories.
    4. **Risk Assessment**: Calculate a risk score based on the classified PII.
    5. **Visualization**: Display a bar chart of the classification distribution.
    """)

# Data Ingestion Section
def load_data_from_mysql():
    try:
        db_config = {
            'host': mysql_host,
            'user': mysql_user,
            'password': mysql_password,
        }
        mysql_data = ingest_data_from_specific_database(db_config, mysql_database)
        st.session_state.main_data += str(mysql_data)
        st.success("Data loaded successfully from MySQL!")
    except Exception as e:
        st.error(f"Failed to load data from MySQL: {e}")

def load_data_from_s3():
    try:
        s3_data = ingest_data_from_s3(s3_bucket, aws_access_key, aws_secret_key)
        st.session_state.main_data += s3_data
        st.success("Data loaded successfully from Amazon S3!")
    except Exception as e:
        st.error(f"Failed to load data from Amazon S3: {e}")

def load_data_from_mongo():
    try:
        mongo_data = ingest_data_from_mongodb(mongo_uri, mongo_database)
        st.session_state.main_data += str(mongo_data)
        st.success("Data loaded successfully from MongoDB!")
    except Exception as e:
        st.error(f"Failed to load data from MongoDB: {e}")

with st.expander("MySQL Server Connection"):
    mysql_host = st.text_input("MySQL Host", "localhost")
    mysql_user = st.text_input("MySQL User", "root")
    mysql_password = st.text_input("MySQL Password", "", type="password")
    mysql_database = st.text_input("MySQL Database", "data")
    if st.button("Load MySQL Data"):
        load_data_from_mysql()

with st.expander("Amazon S3 Connection"):
    aws_access_key = st.text_input("AWS Access Key", "", type="password")
    aws_secret_key = st.text_input("AWS Secret Key", "", type="password")
    s3_bucket = st.text_input("S3 Bucket Name", "")
    if st.button("Load Amazon S3 Data"):
        load_data_from_s3()

with st.expander("MongoDB Connection"):
    mongo_uri = st.text_input("MongoDB URI", "", type="password")
    mongo_database = st.text_input("MongoDB Database", "data")
    if st.button("Load MongoDB Data"):
        load_data_from_mongo()

# PII Extraction Section
pii_method = st.selectbox("Choose PII Extraction Method", ['Regex', 'Presidio'])

def extract_pii_with_regex():
    st.session_state.pii_data = detect_pii(st.session_state.main_data)
    classified_pii = classify_pii(st.session_state.pii_data)
    classified_pii_df = pd.DataFrame([{'Category': cat, 'Count': len(vals)} for cat, vals in classified_pii.items()])
    
    # Display PII Classification and Visualization
    st.success("PII classified successfully!")
    risk_score = calculate_risk_score(classified_pii)
    st.write(f"The Risk Score is: {risk_score:.2f}")
    
    if not classified_pii_df.empty:
        st.write("Classification Distribution:", classified_pii_df)
        st.plotly_chart(px.bar(classified_pii_df, x='Category', y='Count', title="PII Classification Distribution"))

def extract_pii_with_presidio():
    analyzer_params = ('spaCy', 'en_core_web_lg', '', '')
    st_entities = ['PERSON', 'URL', 'EMAIL_ADDRESS', 'CREDIT_CARD', 'PHONE_NUMBER', 'IN_AADHAAR']
    st_analyze_results = analyze(*analyzer_params, text=st.session_state.main_data, entities=st_entities, language="en")
    annotated_tokens = annotate(text=st.session_state.main_data, analyze_results=st_analyze_results)
    st.success("PII extracted using Presidio!")
    annotated_text(*annotated_tokens)

if st.button("Extract PII"):
    if pii_method == 'Regex':
        extract_pii_with_regex()
    else:
        extract_pii_with_presidio()

# FAQs Section
with st.expander("FAQ's"):
    options = ['What is General Data Protection Regulation (GDPR)', 'What is California Consumer Privacy Act (CCPA)', 'What is HIPAA (Health Insurance Portability and Accountability Act)', 'What is Personally Identifiable Information (PII)', 'What is FAIR Risk Score']
    faq = st.selectbox("Choose an option", options)
    if faq == 'What is General Data Protection Regulation (GDPR)':
        st.markdown("""
        **GDPR** is a regulation in EU law on data protection and privacy in the European Union (EU) and the European Economic Area (EEA). It also addresses the transfer of personal data outside the EU and EEA areas. GDPR aims to give control to individuals over their personal data and to simplify the regulatory environment for international business.
        """)

    elif faq == 'What is California Consumer Privacy Act (CCPA)':
        st.markdown("""
        **CCPA** is a state statute intended to enhance privacy rights and consumer protection for residents of California, USA. It provides California residents with the right to know what personal data is being collected about them, to whom it is being sold, and the ability to request deletion of their personal data.
        """)

    elif faq == 'What is HIPAA (Health Insurance Portability and Accountability Act)':
        st.markdown("""
        **HIPAA** is a U.S. law designed to provide privacy standards to protect patients' medical records and other health information provided to health plans, doctors, hospitals, and other healthcare providers.
        """)

    elif faq == 'What is Personally Identifiable Information (PII)':
        st.markdown("""
        **PII** refers to any data that could potentially identify a specific individual. Examples include a person’s full name, social security number, driver's license number, bank account number, passport number, email address, and phone numbers.
        """)

    elif faq == 'What is FAIR Risk Score':
        st.markdown("""
        **FAIR Risk Score** is a method used to assess the risk of PII by applying the FAIR (Factor Analysis of Information Risk) framework. It helps organizations evaluate and quantify the potential risk associated with PII by assessing factors like threat, vulnerability, and impact to calculate a comprehensive risk score.
        """)

# Interactive AI Section for Queries
st.subheader("Ask with AI")

if "ai_responses" not in st.session_state:
    st.session_state.ai_responses = []  # To keep track of the conversation

query = st.text_input("Type your query here:")

if st.button("Ask AI"):
    if query.strip():
        with st.spinner('Waiting for AI response...'):
            try:
                # Assuming getResponse is a function that returns the AI's reply
                response = getResponse(query)
                # Store the query and response in session state to simulate a chat
                st.session_state.ai_responses.append((query, response))
                st.success("Response received!")
            except Exception as e:
                st.error(f"Problem with connecting with AI: {e}")
    else:
        st.warning("Please enter a query before asking AI.")

# Display conversation history
if st.session_state.ai_responses:
    st.write("### Conversation History:")
    for i, (user_query, ai_reply) in enumerate(st.session_state.ai_responses):
        st.write(f"**You**: {user_query}")
        st.write(f"**AI**: {ai_reply}")
        st.write("---")

# Add a button to clear conversation history
if st.button("Clear Conversation"):
    st.session_state.ai_responses = []  # Clear the conversation history
    st.success("Conversation history cleared!")

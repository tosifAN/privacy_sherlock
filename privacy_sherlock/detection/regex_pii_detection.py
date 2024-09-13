import re
import pandas as pd

# Regular Expressions for PII patterns (Indian context)
PII_PATTERNS = {
    'email': r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+[a-zA-Z]{2,}',
    'date': r'\b(0[1-9]|[12][0-9]|3[01])[-\/.](0[1-9]|1[0-2])[-\/.](19|20)\d{2}\b',
    'aadhaar': r'\d{4}\s?\d{4}\s?\d{4}',  # Aadhaar number (with or without spaces)
    'pan': r'[A-Z]{5}[0-9]{4}[A-Z]{1}',  # PAN number
    'ac_or_cre_number': r'\b(?:\d{4}[-\s]?){3}\d{4}|\b\d{13,19}\b|\b\d{9,18}\b',  # Credit Card number and bank account number
    'phone': r'(\+91[\-\s]?)?[6-9]\d{2}[\-\s]?\d{3}[\-\s]?\d{4}',  # Indian phone number
    'passport': r'[A-Z]{1}\d{7}',  # Indian passport number
    'voter_id': r'[A-Z]{3}\d{7}',  # Voter ID number
    'driving_license': r'[A-Z]{2}\d{2}\s?\d{11}',  # Driving License number
    'pin_code': r'\b\d{6}\b',  # Indian Postal Code (PIN)
    'ifsc_code': r'[A-Z]{4}0[A-Z0-9]{6}',  # IFSC Code
    'gstin': r'\d{2}[A-Z]{5}\d{4}[A-Z]{1}[A-Z\d]{1}[Z]{1}[A-Z\d]{1}',  # GSTIN
    'ip_address': r'\b((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b',  # IP Address
    'mac_address': r'([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})',  # MAC Address
    'public_social_media_profile' : r'https?://(?:www\.)?(?:facebook\.com|twitter\.com|instagram\.com|linkedin\.com|pinterest\.com|youtube\.com|reddit\.com)/[\w-]+', # Public Social Media Profile
    'epfo_number': r'[A-Z]{2}/\d{5}/\d{4}' # EPFO number  
}

def detect_pii(data, patterns=PII_PATTERNS):
    pii_found = {pii_type: [] for pii_type in patterns}
    
    # Apply PII detection for each pattern
    for pii_type, pattern in patterns.items():
        matches = re.findall(pattern, data)
        pii_found[pii_type].extend(matches)
    
    # Remove empty matches
    pii_found = {k: v for k, v in pii_found.items() if v}
    
    return pii_found

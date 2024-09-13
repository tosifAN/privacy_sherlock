# Updated PII Classification with 'financial' and 'personal'
PII_CLASSIFICATION = {
    'financial': ['pan', 'ac_or_cre_number','ifsc_code', 'gstin'],
    'personal': ['email', 'aadhaar', 'phone', 'date','pin_code'],
    'sensitive': ['mac_address', 'passport', 'ip_address', 'driving_license', 'voter_id','epfo_number'],
    'public': ['public_social_media_profile']
}

def classify_pii(pii_detected):
    classified_pii = {category: [] for category in PII_CLASSIFICATION.keys()}
    
    for pii_type, values in pii_detected.items():
        for category, types in PII_CLASSIFICATION.items():
            if pii_type in types:
                classified_pii[category].extend(values)
    
    return classified_pii



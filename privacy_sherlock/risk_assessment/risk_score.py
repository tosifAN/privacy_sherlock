def calculate_risk_score(classified_pii):
    # Risk weights for each category
    risk_weights = {
        'financial': 0.8,    # High risk for financial PII
        'personal': 0.5,     # Moderate risk for personal PII
        'sensitive': 0.9,    # Very high risk for sensitive PII
        'public': 0.2,       # Low risk for public PII
    }
    
    # Total PII count
    total_pii = sum(len(items) for items in classified_pii.values())
    
    # Risk score calculation
    risk_score = sum(len(classified_pii[category]) * risk_weights.get(category, 0) 
                     for category in classified_pii.keys())
    
    # Return normalized risk score
    return risk_score / total_pii if total_pii > 0 else 0

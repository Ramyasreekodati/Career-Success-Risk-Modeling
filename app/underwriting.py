import numpy as np

def calculate_underwriting_decision(risk_level, dti, percentile):
    """
    Recalibrated underwriting logic with stricter consistency.
    """
    decision = "Review Required"
    reason = "Initial profile analysis completed."
    suggested_amount_adj = 0 
    
    # Tiered Logic
    if risk_level == "Low":
        if dti < 0.35:
            decision = "Approved"
            reason = "Exceptional career outlook with optimal financial headroom."
            suggested_amount_adj = 15
        else:
            decision = "Conditional Approval"
            reason = "Strong employability, but high DTI requires lower loan amount or co-signer."
            suggested_amount_adj = -10
    elif risk_level == "Medium":
        if dti < 0.40:
            decision = "Conditional Approval"
            reason = "Profile shows promise; disbursement linked to internship verification."
        else:
            decision = "Manual Review"
            reason = "Moderate risk combined with high DTI. Over-leverage detected."
            suggested_amount_adj = -20
    else: # High Risk
        decision = "Rejected"
        reason = "Significant career-placement risk. Repayment sustainability cannot be verified."
        suggested_amount_adj = -40
        
    if percentile < 15 and decision != "Rejected":
        decision = "Fast-Track Approval"
        reason = "Applicant in the top 15% of career competency benchmark."
        
    return {
        "decision": decision,
        "reason": reason,
        "suggested_amount_adjustment": suggested_amount_adj
    }

def calculate_risk_based_pricing(base_rate, risk_level, dti):
    """
    Adjusts interest rates with transparent breakdown.
    """
    premium = 0.0
    if risk_level == "Medium": premium += 1.25
    elif risk_level == "High": premium += 3.50
    
    if dti > 0.4: premium += 0.75
    
    return {
        "base_rate": base_rate,
        "risk_premium": premium,
        "final_rate": round(base_rate + premium, 2)
    }

def generate_targeted_interventions(current_risk, current_data, predict_fn):
    """
    Calculates quantified impact of specific student actions.
    """
    if current_risk == "Low":
        return {"impact": "None", "text": "Profile is already optimized."}
        
    # Scenario: High Impact Actions
    # 1. Add Internship
    trial_intern = current_data.copy()
    trial_intern['internships'] += 1
    new_res_intern = predict_fn(trial_intern)
    
    # 2. Add Certifications
    trial_cert = current_data.copy()
    trial_cert['certifications'] += 2
    new_res_cert = predict_fn(trial_cert)
    
    impacts = []
    if new_res_intern['risk_level'] != current_risk:
        impacts.append(f"Gaining **1 additional internship** reduces risk to {new_res_intern['risk_level']}.")
    
    if new_res_cert['risk_level'] != current_risk:
        impacts.append(f"Adding **2 certifications** improves placement probability to {new_res_cert['risk_level']}.")
        
    if not impacts:
        return {"impact": "Marginal", "text": "Basic profile updates have marginal impact. Higher CGPA or Tier-up required."}
        
    return {"impact": "High", "text": " | ".join(impacts)}

def estimate_default_probability(risk_level, dti, behavioral_score=0.5):
    """
    Estimates PD with categorization.
    """
    # Defensive Clamping
    dti = max(0, min(1.0, dti))
    
    base_probs = {"Low": 0.02, "Medium": 0.08, "High": 0.22, "Manual Review": 0.25, "Rejected": 0.45}
    prob = base_probs.get(risk_level, 0.15)
    
    # Adjust for DTI (stricter penalty)
    if dti > 0.45: prob *= 1.8
    elif dti > 0.35: prob *= 1.3
    
    # Final clamping
    pd_val = round(max(0.01, min(0.99, prob)) * 100, 1)
    
    # Categorize
    category = "Low"
    if pd_val > 20: category = "High"
    elif pd_val > 10: category = "Moderate"
    
    return {
        "value": pd_val,
        "category": category,
        "label": f"{pd_val}% ({category} Default Risk)"
    }

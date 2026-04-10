import numpy as np

def calculate_underwriting_decision(risk_level, dti, percentile):
    """
    Programmatic underwriting with data-driven decisions.
    Rules aligned to the structured AI prompt spec.
    """
    decision = "Manual Review"
    reason = "Insufficient data to conclusively verify repayment capability."
    suggested_amount_adj = 0

    if risk_level == "Low":
        if dti < 0.35:
            decision = "Approved"
            reason = (
                f"Strong academic standing and optimal DTI of {dti*100:.1f}% "
                f"(well below the 35% threshold) verify repayment sustainability."
            )
            suggested_amount_adj = 15
        else:
            decision = "Conditional Approval"
            reason = (
                f"High employability outlook, but DTI of {dti*100:.1f}% "
                f"exceeds the 35% safe zone. A co-signer or loan reduction is required."
            )
            suggested_amount_adj = -10

    elif risk_level == "Medium":
        if dti < 0.40:
            decision = "Conditional Approval"
            reason = (
                f"Profile shows career promise, but placement is not guaranteed within 3 months. "
                f"DTI of {dti*100:.1f}% is acceptable. Disbursement linked to verified internship."
            )
        else:
            decision = "Manual Review"
            reason = (
                f"Moderate placement risk combined with DTI of {dti*100:.1f}% signals over-leverage. "
                f"Human underwriter review required."
            )
            suggested_amount_adj = -20

    else:  # High Risk
        decision = "Rejected"
        reason = (
            f"High career-placement risk with DTI of {dti*100:.1f}% cannot be verified for "
            f"repayment sustainability. Application does not meet minimum credit standards."
        )
        suggested_amount_adj = -40

    # Fast-Track override for top performers
    if percentile < 15 and decision != "Rejected":
        decision = "Fast-Track Approval"
        reason = (
            f"Applicant is in the top {percentile:.0f}% of career competency benchmarks. "
            f"Fast-track criteria met on all primary risk indicators."
        )

    return {
        "decision": decision,
        "reason": reason,
        "suggested_amount_adjustment": suggested_amount_adj
    }


def calculate_risk_based_pricing(base_rate, risk_level, dti):
    """
    Transparent risk-based pricing with structured bands:
    - Low risk → 8%–10%
    - Medium risk → 10%–14%
    - High risk → 14%–18%
    """
    premium = 0.0

    if risk_level == "Low":
        # Clamp to 8-10% band
        final_rate = max(8.0, min(10.0, base_rate))
    elif risk_level == "Medium":
        premium += 1.25
        if dti > 0.4: premium += 0.75
        final_rate = max(10.0, min(14.0, base_rate + premium))
    else:  # High
        premium += 3.50
        if dti > 0.4: premium += 1.0
        final_rate = max(14.0, min(18.0, base_rate + premium))

    return {
        "base_rate": base_rate,
        "risk_premium": round(final_rate - base_rate, 2),
        "final_rate": round(final_rate, 2),
        "rate_band": (
            "8%–10% (Low Risk)" if risk_level == "Low"
            else "10%–14% (Medium Risk)" if risk_level == "Medium"
            else "14%–18% (High Risk)"
        )
    }


def generate_ai_narrative(risk_level, dti, salary, timeline, cgpa, internships, tier):
    """
    Structured, data-driven narrative using the strict AI prompt template.
    Outputs specific numbers, not vague phrases.
    """
    salary_lpa = round(salary / 100000, 2)
    dti_pct = round(dti * 100, 1)

    # Decision
    if risk_level == "Low" and dti < 0.35:
        decision = "APPROVE"
        rate = "8%–10%"
    elif risk_level == "Medium" and dti < 0.40:
        decision = "CONDITIONAL APPROVAL"
        rate = "10%–14%"
    elif risk_level == "High":
        decision = "REJECT"
        rate = "14%–18%"
    else:
        decision = "CONDITIONAL APPROVAL"
        rate = "10%–14%"

    # Risk Factors
    risk_factors = []
    if dti > 0.35:
        risk_factors.append(f"DTI of {dti_pct}% exceeds the 35% safe threshold, increasing repayment pressure.")
    if internships < 2:
        risk_factors.append(f"Only {internships} internship(s) completed — limited industry exposure may reduce initial salary leverage.")
    if cgpa < 7.5:
        risk_factors.append(f"CGPA of {cgpa:.1f} is below the 7.5 benchmark for premium placements.")
    if tier != "Tier 1":
        risk_factors.append(f"Institute tier ({tier}) may limit access to high-paying campus recruiters.")
    if not risk_factors:
        risk_factors.append("All primary risk indicators are within acceptable ranges.")

    # Narrative
    narrative = (
        f"Candidate is projected to be placed {timeline} with an estimated salary of ₹{salary_lpa} LPA. "
        f"The DTI ratio of {dti_pct}% {'is within safe limits' if dti < 0.35 else 'poses moderate repayment strain'}. "
        f"Academic performance (CGPA {cgpa:.1f}) from a {tier} institution "
        f"{'supports a strong career trajectory' if cgpa >= 7.5 else 'needs improvement to compete for premium roles'}."
    )

    # Career Advice
    career_advice = []
    if internships < 3:
        career_advice.append(
            f"Complete {3 - internships} additional internship(s) in your domain before graduation "
            f"to improve salary negotiation leverage by an estimated 15–25%."
        )
    if cgpa < 8.0:
        career_advice.append(
            f"Improve CGPA from {cgpa:.1f} to 8.0+ by prioritizing core subject electives in the next 2 semesters."
        )
    career_advice.append(
        "Register on at least 3 job portals and aim for 5+ applications per week to increase placement probability."
    )

    return {
        "decision": decision,
        "interest_rate": rate,
        "reasoning": (
            f"Based on a predicted salary of ₹{salary_lpa} LPA, a DTI of {dti_pct}%, "
            f"a CGPA of {cgpa:.1f} at {tier}, and {internships} internship(s), "
            f"the risk profile is classified as '{risk_level}'."
        ),
        "risk_factors": risk_factors[:3],  # Top 3 most significant
        "narrative": narrative,
        "career_advice": career_advice
    }


def generate_targeted_interventions(current_risk, current_data, predict_fn):
    """
    Calculates quantified impact of specific student actions.
    """
    if current_risk == "Low":
        return {"impact": "None", "text": "Profile is already optimized. No corrective action required."}

    trial_intern = current_data.copy()
    trial_intern['internships'] = int(trial_intern.get('internships', 0)) + 1
    new_res_intern = predict_fn(trial_intern)

    trial_cert = current_data.copy()
    trial_cert['certifications'] = int(trial_cert.get('certifications', 0)) + 2
    new_res_cert = predict_fn(trial_cert)

    impacts = []
    if new_res_intern.get('risk_level') != current_risk:
        impacts.append(f"Gaining **1 more internship** reduces risk classification to {new_res_intern['risk_level']}.")
    if new_res_cert.get('risk_level') != current_risk:
        impacts.append(f"Adding **2 certifications** improves placement profile to {new_res_cert['risk_level']}.")

    if not impacts:
        return {"impact": "Marginal", "text": "Basic updates have marginal impact. A CGPA improvement or institute tier-up is required."}

    return {"impact": "High", "text": " | ".join(impacts)}


def estimate_default_probability(risk_level, dti, behavioral_score=0.5):
    """
    Estimates Probability of Default (PD) with category labels.
    """
    dti = max(0, min(1.0, dti))

    base_probs = {
        "Low": 0.02, "Medium": 0.08, "High": 0.22,
        "Manual Review": 0.25, "Rejected": 0.45
    }
    prob = base_probs.get(risk_level, 0.15)

    if dti > 0.45: prob *= 1.8
    elif dti > 0.35: prob *= 1.3

    pd_val = round(max(0.01, min(0.99, prob)) * 100, 1)

    category = "Low"
    if pd_val > 20: category = "High"
    elif pd_val > 10: category = "Moderate"

    return {
        "value": pd_val,
        "category": category,
        "label": f"{pd_val}% ({category} Default Risk)"
    }

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import numpy as np
import joblib
from src.explainability import get_risk_explanation
from app.underwriting import calculate_underwriting_decision, calculate_risk_based_pricing, generate_targeted_interventions, estimate_default_probability, generate_ai_narrative
from app.database import log_decision
import uvicorn

app = FastAPI(title="AI Underwriting & Risk Platform")

# Load models and artifacts
models = {}

def load_all_models():
    """Load models globally if they haven't been loaded yet."""
    if not models:
        try:
            # Resolve paths relative to the project root
            base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
            
            models['clf'] = joblib.load(os.path.join(base_path, 'models', 'clf_timeline.pkl'))
            models['reg'] = joblib.load(os.path.join(base_path, 'models', 'reg_salary.pkl'))
            models['scaler'] = joblib.load(os.path.join(base_path, 'models', 'scaler.pkl'))
            models['le'] = joblib.load(os.path.join(base_path, 'models', 'le_timeline.pkl'))
            models['features'] = joblib.load(os.path.join(base_path, 'models', 'feature_names.pkl'))
            print("INFO: All models loaded successfully into the core engine.")
        except Exception as e:
            print(f"CRITICAL ERROR: Failed to load models: {str(e)}")

@app.on_event("startup")
def startup_event():
    load_all_models()

class StudentData(BaseModel):
    course_type: str
    cgpa: float
    internships: int
    certifications: int
    academic_consistency: str
    institute_tier: str
    placement_cell_activity: str
    industry_demand_index: float
    regional_job_density: float
    job_portal_activity: float
    mock_interviews_cleared: int
    loan_amount: float = 1000000.0 
    interest_rate: float = 10.0
    tenure_years: int = 15

def internal_predict(d):
    # Helper for what-if simulations
    input_encoded = pd.get_dummies(pd.DataFrame([d]))
    final_input = pd.DataFrame(columns=models['features']).fillna(0)
    for col in models['features']:
        if col in input_encoded.columns:
            final_input[col] = input_encoded[col]
    
    scaled = models['scaler'].transform(final_input)
    t_idx = np.argmax(models['clf'].predict_proba(scaled)[0])
    label = models['le'].classes_[t_idx]
    return {"risk_level": "Low" if "3 months" in label else "Medium" if "6 months" in label else "High"}

def core_predict(model_data: dict):
    """
    Core prediction engine used by both single and batch pipelines.
    Enforces consistent preprocessing and debugging.
    """
    load_all_models()
    try:
        # Debugging: Log Input
        print(f"DEBUG: Processing record with keys: {list(model_data.keys())}")
        
        # Extract and validate loan fields (provide defaults if missing)
        loan_info = {
            "loan_amount": float(model_data.get("loan_amount", 1000000)),
            "interest_rate": float(model_data.get("interest_rate", 10.5)),
            "tenure_years": int(model_data.get("tenure_years", 15))
        }
        
        # Create a clean copy for ML features
        features_dict = {k: v for k, v in model_data.items() if k in StudentData.__fields__}
        
        # Preprocess
        input_encoded = pd.get_dummies(pd.DataFrame([features_dict]))
        final_input = pd.DataFrame(columns=models['features']).fillna(0)
        for col in models['features']:
            if col in input_encoded.columns:
                final_input[col] = input_encoded[col]
        
        # Verify shape
        scaled_input = models['scaler'].transform(final_input)
        
        # Base Predictions
        timeline_probs = models['clf'].predict_proba(scaled_input)[0]
        timeline_idx = np.argmax(timeline_probs)
        timeline_label = str(models['le'].classes_[timeline_idx])
        
        salary = float(models['reg'].predict(scaled_input)[0])
        salary = max(300000, min(2500000, salary))
        
        # Underwriting / Decision Logic
        stress = calculate_stress_test(salary, timeline_label, loan_info)
        current_risk = "Low" if "3 months" in timeline_label else "Medium" if "6 months" in timeline_label else "High"
        
        uw_decision = calculate_underwriting_decision(
            current_risk,
            stress['debt_to_income_ratio'],
            calculate_percentile(salary, float(model_data.get('cgpa', 7.0)))
        )
        
        pricing = calculate_risk_based_pricing(loan_info['interest_rate'], current_risk, stress['debt_to_income_ratio'])
        pd_info = estimate_default_probability(current_risk, stress['debt_to_income_ratio'])
        
        # 3. Targeted Interventions
        goal_res = generate_targeted_interventions(
            current_risk,
            features_dict,
            internal_predict
        )

        # 4. Structured AI Narrative (Data-Driven)
        ai_report = generate_ai_narrative(
            risk_level=current_risk,
            dti=stress['debt_to_income_ratio'],
            salary=salary,
            timeline=timeline_label,
            cgpa=float(features_dict.get('cgpa', 7.0)),
            internships=int(features_dict.get('internships', 0)),
            tier=str(features_dict.get('institute_tier', 'Tier 2'))
        )

        # Final result assembly
        return {
            "placement_timeline": timeline_label,
            "predicted_salary": round(salary, 2),
            "salary_lpa": f"{round(salary/100000, 2)} LPA",
            "underwriting_decision": uw_decision,
            "pricing_breakdown": pricing,
            "default_risk": pd_info,
            "intervention": goal_res,
            "risk_breakdown": calculate_risk_breakdown(
                features_dict,
                salary=salary,
                emi=stress.get('monthly_emi', 0),
                dti=stress.get('debt_to_income_ratio', 0)
            ),
            "ai_summary": ai_report["narrative"],
            "ai_report": ai_report,
            "stress_test": stress,
            "status": "success"
        }
    except Exception as e:
        print(f"ERROR in Core Predict: {str(e)}")
        return {"status": "error", "error_message": str(e)}

@app.post("/predict")
def predict_risk(data: StudentData):
    res = core_predict(data.dict())
    if res['status'] == 'error':
        raise HTTPException(status_code=500, detail=res['error_message'])
    
    # Recommendations (only for success)
    res['recommendations'] = get_recommendations(res['placement_timeline'], data)
    log_decision(data.dict(), res, res['underwriting_decision'])
    return res

def calculate_percentile(salary, cgpa):
    # Heuristic for demo purposes
    # Higher salary and CGPA leads to better percentile
    score = (salary / 1000000) * 0.7 + (cgpa / 10) * 0.3
    percentile = int(min(99, max(1, score * 100)))
    return 100 - percentile # "Top X%"

def calculate_risk_breakdown(data, salary=0, emi=0, dti=0):
    """
    AI Risk Scoring Engine — follows the strict prompt spec:
    Academic  = f(CGPA, Tier)
    Market    = f(DTI, EMI vs Salary)
    Professional = f(Internships, Predicted Salary)
    All scores vary deterministically with input.
    """
    cgpa        = float(data.get('cgpa', 7.0))
    tier        = str(data.get('institute_tier', 'Tier 2'))
    internships = int(data.get('internships', 0))

    # ── ACADEMIC RISK (CGPA + Tier) ───────────────────────────────────────
    # CGPA 10 → 0 risk | CGPA 4 → 60 risk  (scale: 0-60)
    cgpa_risk  = round((10 - cgpa) / 6 * 60, 1)
    tier_risk  = {'Tier 1': 0, 'Tier 2': 20, 'Tier 3': 40}.get(tier, 20)
    academic   = round(min(100, cgpa_risk + tier_risk), 1)

    # ── MARKET RISK (DTI + EMI burden) ───────────────────────────────────
    # Low income-to-debt → higher risk. High EMI vs salary → higher risk.
    dti_risk   = round(min(dti * 100, 70), 1)                            # 0-70
    # EMI burden: what % of monthly salary the EMI consumes
    monthly_sal = salary / 12 if salary > 0 else 1
    emi_burden  = round(min((emi / monthly_sal) * 30, 30), 1)            # 0-30
    market      = round(min(100, dti_risk + emi_burden), 1)

    # ── PROFESSIONAL RISK (Internship + Predicted Salary) ─────────────────
    # No internship → 50 risk, 1 → 30, 2+ → 15, 3+ → 0
    intern_risk = {0: 50, 1: 30, 2: 15}.get(min(internships, 2), 0)
    # Low salary → high risk  (salary 3L → 50 pts, 25L → 0 pts)
    sal_risk    = round(max(0, (1 - min(salary / 2500000, 1)) * 50), 1)
    professional = round(min(100, intern_risk + sal_risk), 1)

    return {
        "academic":     academic,
        "market":       market,
        "professional": professional
    }


def generate_polished_summary(label, data):
    strengths = []
    weaknesses = []
    
    if data['cgpa'] > 8.5: strengths.append("exceptional academic performance")
    elif data['cgpa'] > 7.5: strengths.append("strong academic background")
    
    if data['internships'] >= 2: strengths.append("significant internship exposure")
    elif data['internships'] == 0: weaknesses.append("limited internship exposure")
    
    if data['certifications'] >= 3: strengths.append("diverse professional certifications")
    
    if data['industry_demand_index'] < 0.4: weaknesses.append("weak field-wise job demand")
    
    summary = f"Forecast Outcome: {label}. "
    if strengths:
        summary += f"{str.capitalize(', '.join(strengths))} significantly improve placement chances, "
    if weaknesses:
        summary += f"however {', '.join(weaknesses)} increases the risk profile."
    else:
        summary += "indicating a highly competitive candidate profile."
        
    return summary

def calculate_stress_test(salary, timeline, loan_info):
    # EMI Calculation: P * r * (1+r)^n / ((1+r)^n - 1)
    p = loan_info['loan_amount']
    r = (loan_info['interest_rate'] / 100) / 12
    n = loan_info['tenure_years'] * 12
    
    emi = (p * r * (1 + r)**n) / ((1 + r)**n - 1)
    annual_repayment = emi * 12
    
    # Debt-to-Income (DTI)
    dti = annual_repayment / salary
    
    # Adjust for placement delay (lost income)
    delay_months = {'Within 3 months': 3, 'Within 6 months': 6, 'Within 12 months': 12, 'Delayed / High Risk': 18}.get(timeline, 6)
    estimated_repayment_stress = "Low"
    if dti > 0.4 or delay_months >= 12:
        estimated_repayment_stress = "High"
    elif dti > 0.25 or delay_months >= 6:
        estimated_repayment_stress = "Medium"
        
    return {
        "monthly_emi": round(emi, 2),
        "debt_to_income_ratio": round(dti, 4),
        "estimated_delay_months": delay_months,
        "stress_profile": estimated_repayment_stress
    }

class BatchRequest(BaseModel):
    data: list[dict]
    scenario: str

@app.post("/simulate-scenario")
def simulate_scenario(request: BatchRequest):
    data = request.data
    scenario = request.scenario
    
    # Adjust market conditions based on scenario
    adjustments = {
        "Recession": {"demand": -0.4, "density": -0.2},
        "Market Boom": {"demand": 0.3, "density": 0.2},
        "Standard": {"demand": 0, "density": 0}
    }
    adj = adjustments.get(scenario, adjustments["Standard"])
    
    simulated_results = []
    print(f"DEBUG: Starting batch simulation for {len(data)} records under {scenario} scenario.")
    
    for idx, s in enumerate(data):
        try:
            # Shift market signals
            s['industry_demand_index'] = max(0, min(1, float(s.get('industry_demand_index', 0.5)) + adj['demand']))
            s['regional_job_density'] = max(0, min(1, float(s.get('regional_job_density', 0.5)) + adj['density']))
            
            res = core_predict(s)
            if res['status'] == 'error':
                print(f"DEBUG: Record {idx} failed: {res['error_message']}")
            simulated_results.append(res)
        except Exception as e:
            print(f"DEBUG: Record {idx} crashed: {str(e)}")
            simulated_results.append({"status": "error", "error_message": str(e)})
            
    return simulated_results

@app.post("/predict-batch")
def predict_batch(students: list[dict]):
    results = []
    for s in students:
        results.append(core_predict(s))
    return results

def get_recommendations(label, data):
    recs = []
    
    # Priority 1: Placement Timeline Risk
    if label in ['Delayed / High Risk', 'Within 12 months']:
        if data.internships < 2:
            recs.append({
                "category": "Experience",
                "action": "Gap in Industry Exposure",
                "recommendation": "Secure at least one technical internship or 3-month industry project immediately."
            })
        if data.mock_interviews_cleared < 4:
            recs.append({
                "category": "Interpersonal",
                "action": "Soft Skills Training",
                "recommendation": "Enroll in high-frequency mock interview sessions to improve confidence and technical articulation."
            })
        if data.cgpa < 7.5:
            recs.append({
                "category": "Academic",
                "action": "Academic Focus",
                "recommendation": "Focus on high-growth elective subjects to improve recent semester consistency."
            })
        if data.certifications < 3:
            recs.append({
                "category": "Skillset",
                "action": "Skill Validation",
                "recommendation": "Earn 2+ industry-recognized certifications in your core field (e.g., AWS, CFA, or Nursing Specializations)."
            })
    
    # Priority 2: Market Readiness
    if data.job_portal_activity < 0.4:
         recs.append({
                "category": "Engagement",
                "action": "Low Portal Activity",
                "recommendation": "Increase presence on LinkedIn and industry-specific portals. Aim for 5+ applications per week."
            })

    # Priority 3: General Best Practices
    if not recs:
        recs.append({
            "category": "Growth",
            "action": "Network Expansion",
            "recommendation": "Engage with alumni from Tier-1 institutes in your field to uncover hidden job markets."
        })
        
    return recs

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

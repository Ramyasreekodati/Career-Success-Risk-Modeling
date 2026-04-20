# ⚖️ AI Education Loan Underwriter & Decision Intelligence

### *Quantifying Student Potential. Minimizing Financial Risk.*

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_svg)](https://career-success-risk-modeling.streamlit.app/)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📌 Project Vision
Traditional education lending relies on **backward-looking metrics** (family income, past credit). This platform shifts the paradigm to **forward-looking intelligence** by predicting a student's **Career Success Path**. 

By analyzing academic trajectory, institutional strength, and real-time labor market signals, we provide lenders with a programmatic "Risk Score" that determines loan eligibility and risk-based pricing.

## 🚀 Key Features
- **🎯 Precision Underwriting:** Automated "Approve/Manual Review/Reject" decisions based on Career-Adjusted DTI (Debt-to-Income) ratios.
- **💰 Salary Forecasting:** Machine Learning engine trained on thousands of placement outcomes to predict starting LPA.
- **🕵️ SHAP Explainability:** Transparent "Risk Factor" breakdown—know exactly *why* a profile is flagged (e.g., "Weak internship exposure").
- **📈 Scenario Simulations:** Stress-test portfolios against **Recessions** or **Market Booms** in real-time.
- **🚀 Growth Roadmap:** Targeted interventions (e.g., "Complete 2 certifications to reduce risk by 15%").
- **📄 Executive Reporting:** Download professional underwriting reports for formal loan documentation.

## 🛠️ Tech Stack
- **Frontend:** Streamlit (Custom Glassmorphism UI)
- **Backend:** FastAPI (Core Risk Engine)
- **Machine Learning:** XGBoost (Classification) & Random Forest (Regression)
- **Explainability:** SHAP (SHapley Additive exPlanations)
- **Database:** SQLite (Decision Audit Logging)

## 📊 How It Works (The Logic)
The system calculates risk through three primary vectors:
1.  **Academic Risk:** CGPA consistency + Institute Placement Strength.
2.  **Market Risk:** Industry Demand Index + Regional Job Density.
3.  **Professional Risk:** Internship performance + Certification depth.

These vectors are combined with **Stress Testing** (EMI vs. Predicted Salary) to generate a final **Decision Intelligence** output.

## 📂 Repository Structure
```
├── app/                # Core Application (FastAPI & Streamlit)
├── src/                # ML Pipeline & Explainability Logic
├── models/             # Pre-trained XGBoost & RF Artifacts
├── data/               # Synthetic Training & Market Datasets
├── notebooks/          # Research & Model Validation
└── PROJECT_REPORT.md   # Detailed Technical Analysis
```

## 🏁 Getting Started
1. Clone the repo
2. Install dependencies: `pip install -r requirements.txt`
3. Launch the app: `streamlit run app/view.py`

---
*Developed for AI-Driven Financial Services & Career Intelligence.*

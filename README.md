# ⚖️ AI Career Success & Risk Modeling Platform

![Hero Banner](career_risk_hero_banner.png)

### *Bridging the Gap Between Education Potential and Financial Stability*

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_svg)](https://career-success-risk-modeling.streamlit.app/)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📌 Project Overview
Traditional education lending is flawed—it relies on historical family income rather than a student's future potential. This platform introduces **Predictive Career Underwriting**, a forward-looking intelligence system that forecasts a student's employability and starting salary to determine loan eligibility and risk-based pricing.

By analyzing academic trajectory, institutional strength, and real-time labor market signals, we provide lenders with a programmatic "Risk Score" that powers automated decision-making.

---

## 🚀 Key Features

### 🎯 1. Precision Underwriting
Automated "Approve / Manual Review / Reject" decisions based on **Debt-to-Income (DTI)** ratios and **Placement Probability**.

### 💰 2. Salary Forecasting Engine
A high-performance regression model trained on thousands of placement outcomes to predict starting LPA (Lakhs Per Annum) with an MAE of ~₹45,000.

### 🕵️ 3. Explainable AI (SHAP)
Transparent risk factor breakdown. Know exactly *why* a profile is flagged (e.g., "Weak internship exposure" or "Market saturation in the chosen field").

### 📈 4. Scenario Simulations
Stress-test portfolios against economic shifts. Simulate **Recessions** (dropping industry demand by 40%) or **Market Booms** in real-time to see how portfolio risk fluctuates.

### 🛡️ 5. Targeted Interventions
The engine suggests actionable steps for students to reduce their risk profile, such as "Complete 2 specific certifications to reduce financial risk by 15%."

---

## 🛠️ Technical Architecture

### **The Brain: Multi-Vector Risk Engine**
The system calculates risk through three primary vectors:
1.  **Academic Risk Index:** CGPA consistency + Institute Tier weighting.
2.  **Market & Financial Risk:** Industry Demand Index + Regional Job Density + DTI Ratio.
3.  **Professional Readiness:** Internship depth + Certification impact + Mock interview performance.

### **Tech Stack**
- **Frontend:** Streamlit (Custom Glassmorphism UI)
- **Backend:** FastAPI (Core ML Inference Engine)
- **ML Engine:** XGBoost, Random Forest, & Ridge Regression
- **Explainability:** SHAP (SHapley Additive exPlanations)
- **Visualization:** Plotly & CSS3 dynamic charts
- **Deployment:** Docker & PowerShell automation

---

## 📊 Performance Metrics
| Metric | Value |
| :--- | :--- |
| **Timeline Prediction Accuracy** | ~92% |
| **Salary Prediction MAE** | ₹45,000 |
| **System Latency** | < 200ms per inference |
| **Risk Sensitivity** | High (optimized to minimize Type II errors) |

---

## 📂 Repository Structure
```
├── app/                # Streamlit UI & Glassmorphism Components
├── src/                # Core ML Pipeline & Explainability Logic
├── models/             # Pre-trained XGBoost & RF Artifacts
├── data/               # Synthetic Training & Market Datasets
├── notebooks/          # Research, EDA & Model Validation
├── tests/              # Unit tests for risk logic
├── Dockerfile          # Containerization for production
└── FINAL_PROJECT_REPORT.md # Comprehensive Technical Documentation
```

---

## 🏁 Getting Started

### Prerequisites
- Python 3.9+
- Docker (Optional)

### Installation
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Ramyasreekodati/Career-Success-Risk-Modeling.git
   cd Career-Success-Risk-Modeling
   ```

2. **Setup Environment:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch the Application:**
   ```bash
   streamlit run app/view.py
   ```

### Docker Deployment
```bash
docker build -t career-risk-model .
docker run -p 8501:8501 career-risk-model
```

---

## 📄 License
Distributed under the MIT License. See `LICENSE` for more information.

---
*Developed for AI-Driven Financial Services & Career Intelligence.*

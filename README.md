# ⚖️ AI-Powered Loan Underwriting & Decision Intelligence Platform

An enterprise-grade platform for education loan lenders that transforms career success predictions into programmatic financial decisions. This system evaluates student employability, estimates default probability, and automates high-fidelity underwriting workflows.

## ✨ Core Pillars

- **Decision Intelligence**: Programmatic logic for automated loan approval/rejection with transparent reasoning.
- **Risk-Based Pricing (RBP)**: Dynamic interest rate optimization based on predicted placement risk and DTI (Debt-to-Income) ratios.
- **Predictive Engine**: Dual-model architecture forecasting placement timelines (3/6/12 months) and salary trajectories (LPA).
- **Default Risk Modeling**: Dedicated probabilistic layer for estimating loan default risk (PD).
- **Goal-Oriented Interventions**: Actionable "What-If" planning to guide students toward lower risk tiers (e.g., gain +1 internship).
- **Audit & Continuous Learning**: Comprehensive logging pipeline for regulatory auditing and autonomous model refinement.

## 🛠️ Tech Stack

- **Backend**: Python, FastAPI, Uvicorn
- **Machine Learning**: Scikit-Learn, XGBoost, LightGBM, SHAP
- **Frontend**: Streamlit, Plotly (Dynamic Viz)
- **Infrastructure**: Docker for containerized deployment

## 🚀 Quick Start

### Option 1: Standard Execution (Local)
1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Launch the Application**:
   ```powershell
   .\start_project.ps1
   ```

### Option 2: Docker Execution
```bash
docker build -t placement-risk-app .
docker run -p 8000:8000 -p 8501:8501 placement-risk-app
```

## 📁 Project Structure

- `app/`: FastAPI backend and Streamlit UI.
- `src/`: Core logic for synthetic data, preprocessing, and training.
- `data/`: Student datasets and processed artifacts.
- `models/`: Serialized ML models and encoders.
- `tests/`: Automated unit testing for risk calculation logic.

## 📊 Business Impact
Designed to reduce loan delinquency by providing early visibility into employability gaps, allowing lenders to implement targeted student-support programs (e.g., resume coaching, certifications) early in the student's lifecycle.

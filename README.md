# ⚖️ AI Education Loan Underwriter & Decision Intelligence Platform

### *Bridging the gap between Student Potential and Financial Risk.*

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/Ramyasreekodati/Career-Success-Risk-Modeling)

![Platform Banner](https://images.unsplash.com/photo-1551288049-bbbda536339a?auto=format&fit=crop&q=80&w=2070)

## 📌 What is this? (The "Human" Explanation)
Today, most banks look at a student's **past** (credit score, family income) to decide if they deserve a loan. But for a student, their most valuable asset is their **future**.

This platform is a "Smart Underwriter." It uses AI to predict a student's **Career Success Path**. By analyzing academics, internships, and the live job market, it answers two critical questions for lenders:
1. **Will this student get a job?** (Placement Probability)
2. **Can they afford to pay back the loan?** (Repayment Sustainability)

We transform complex predictive modeling into clear, actionable financial decisions like **Loan Approval**, **Risk-Based Pricing**, and **Default Probability**.

---

## 🚀 Key Value Pillars

### 🤖 1. Automated Underwriting
No more manual guesswork. The system analyzes the student's profile and immediately provides a verdict: **Approved**, **Conditional**, or **Rejected**, backed by a transparent reasoning engine.

### 📈 2. Career & Salary Forecasting
Predict exactly when a student is likely to be placed (within 3 months, 6 months, etc.) and what their estimated starting salary will be in **Lakhs Per Annum (LPA)**.

### 💳 3. Financial Stress Testing
The system runs a "flight simulator" on the student's finances. It calculates the **EMI (Monthly Installment)** and **Income-to-Debt Ratio** to ensure the student won't be overburdened after graduation.

### 🛡️ 4. Risk-Based Pricing (RBP)
Fairer lending. Students with lower career risk get rewarded with lower interest rates, while high-risk profiles include a transparent "Risk Premium" to protect the lender.

---

## 🛠️ How it Works: The 4-Step Workflow

### **Step 1: Intake**
Enter the student's data—Field of study, CGPA, Internships, and College Quality. Input the loan requirements.
> ![Intake Screenshot](https://raw.githubusercontent.com/Ramyasreekodati/Career-Success-Risk-Modeling/main/screenshots/intake_preview.png)

### **Step 2: Career Outlook**
The AI models (XGBoost & LightGBM) process the data to forecast the student's placement timeline and potential salary. 
> *“Top 5% of candidates in the engineering sector.”*

### **Step 3: Financial Feasibility**
We calculate the repayment stress. If the predicted salary is ₹10 LPA and the EMI is ₹20k, the system calculates the **DTI (Debt-to-Income)** ratio to ensure sustainability.

### **Step 4: The Final Verdict**
The Underwriting Engine generates a high-impact verdict banner.
> **Verdict: Approved**  
> *Reasoning: Exceptional career outlook and optimal financial headroom.*

---

## 📊 Portfolio Batch Tools (For Institutional Lenders)
Institutional users can upload a **CSV dataset of 1,000+ applicants**. The system will:
*   Perform **Batch Underwriting** in seconds.
*   Visualize **Portfolio Yield** (how many are approved vs rejected).
*   Export the results to a structured decision ledger.

---

## 🕵️ Transparency & Audit (The "Safety" Layer)
Every single decision is logged in our **Audit Trail**. This ensures:
*   **Regulatory Compliance**: Know why every loan was approved or denied.
*   **Continuous Learning**: Use the logged data to retrain and improve the AI over time.
*   **Drift Monitoring**: Track how student profiles are changing in the real world.

---

## 💻 Tech Stack
*   **Frontend**: Streamlit (Reactive Professional Dashboard)
*   **Backend**: FastAPI (High-performance API)
*   **Machine Learning**: XGBoost, LightGBM, Scikit-Learn
*   **Explainability**: SHAP (Shapley Additive Explanations)
*   **Data Ops**: Pandas, Numpy, Joblib

---

## 🏃 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/Ramyasreekodati/Career-Success-Risk-Modeling.git
cd Career-Success-Risk-Modeling
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch the Platform
Run the automated startup script:
```powershell
.\start_project.ps1
```
*   **Dashboard**: http://localhost:8501
*   **API**: http://localhost:8000

---

## 📜 Ethical AI Disclaimer
This system is designed as a **Decision Support Tool**. While the AI provides high-fidelity predictions, final financial disbursements should involve human oversight to ensure compliance with local lending regulations.

---
**Created by Ramyasreekodati** – *Transforming Education Financing through AI.*

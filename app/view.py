import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import os
from io import BytesIO

st.set_page_config(page_title="AI Education Loan Underwriter", layout="wide")

# Custom CSS for Premium Look
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    div[data-testid="stMetricValue"] > div { font-size: 2.2rem !important; font-weight: 700; color: #ffffff; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: #1e2130; border-radius: 8px; color: #ffffff; padding: 10px 20px; }
    .stTabs [aria-selected="true"] { background-color: #3b82f6 !important; border-bottom: none !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚖️ AI Education Loan Underwriting System")
st.markdown("Automated Career Verification & Credit Intelligence Platform")

# --- TOP HORIZONTAL NAVIGATION ---
# Moving from sidebar to a prominent top-level tab structure
tab_single, tab_batch, tab_history = st.tabs([
    "📂 Individual Loan Assessment", 
    "📊 Portfolio Batch Underwriting", 
    "🕵️ System Summary & History"
])

# Helper for stats
from app.database import get_learning_stats

# --- INDIVIDUAL ASSESSMENT ---
with tab_single:
    st.sidebar.title("👤 Applicant Profile")
    st.sidebar.divider()
    
    def user_input_features():
        course_type = st.sidebar.selectbox("Field of Study", ["Engineering", "MBA", "Nursing", "Data Science", "Finance", "Arts"])
        cgpa = st.sidebar.slider("Current CGPA", 4.0, 10.0, 8.5)
        internships = st.sidebar.number_input("Internships", 0, 5, 1)
        certifications = st.sidebar.number_input("Certifications", 0, 10, 2)
        institute_tier = st.sidebar.selectbox("College Quality", ["Tier 1 (High)", "Tier 2 (Mid)", "Tier 3 (Standard)"])
        demand = st.sidebar.slider("Job Market Demand", 0.0, 1.0, 0.7)
        mock = st.sidebar.number_input("Mock Interviews Cleared", 0, 10, 3)
        amount = st.sidebar.number_input("Requested Loan (₹)", 100000, 5000000, 1000000)
        rate = st.sidebar.slider("Standard Rate (%)", 5.0, 15.0, 10.5)
        tenure = st.sidebar.slider("Term (Years)", 1, 25, 15)

        tier_map = {"Tier 1 (High)": "Tier 1", "Tier 2 (Mid)": "Tier 2", "Tier 3 (Standard)": "Tier 3"}
        return {
            "course_type": course_type, "cgpa": cgpa, "internships": internships, "certifications": certifications,
            "academic_consistency": "High", "institute_tier": tier_map[institute_tier], 
            "placement_cell_activity": "High", "industry_demand_index": demand,
            "regional_job_density": 0.6, "job_portal_activity": 0.5,
            "mock_interviews_cleared": mock, "loan_amount": amount,
            "interest_rate": rate, "tenure_years": tenure
        }

    input_data = user_input_features()

    if st.sidebar.button("👉 Run Comprehensive Underwriting"):
        with st.spinner("Executing Risk Models..."):
            try:
                response = requests.post("http://localhost:8000/predict", json=input_data)
                if response.status_code == 200:
                    res = response.json()
                    st.subheader("🎓 Personal Assessment Result")
                    
                    m1, m2, m3, m4 = st.columns(4)
                    m1.metric("Predicted Salary", f"₹{res['salary_lpa']}")
                    m2.metric("Monthly EMI", f"₹{res['stress_test']['monthly_emi']:,}")
                    m3.metric("Income-to-Debt", f"{res['stress_test']['debt_to_income_ratio']*100:.1f}%")
                    m4.metric("Risk Category", res['default_risk']['category'])

                    uw = res['underwriting_decision']
                    colors = {"Approved": "#28a745", "Conditional Approval": "#ffc107", "Manual Review": "#17a2b8", "Rejected": "#dc3545", "Fast-Track Approval": "#155724"}
                    color = colors.get(uw['decision'], "#007bff")
                    st.markdown(f"""
                        <div style="background-color:{color}22; padding:25px; border-radius:15px; border-left: 10px solid {color}; margin-bottom:20px;">
                            <h1 style="color:{color}; margin:0; font-size:2.2rem">Verdict: {uw['decision']}</h1>
                            <p style="font-size:1.2rem; margin-top:10px;"><b>Reasoning:</b> {uw['reason']}</p>
                            <p style="font-size:1.1rem"><b>Recommended Loan Rate:</b> {res['pricing_breakdown']['final_rate']}%</p>
                        </div>
                    """, unsafe_allow_html=True)

                    with st.expander("🔍 Detailed Analytical Breakdown", expanded=True):
                        st.subheader("Career Growth Path")
                        if 'intervention' in res: st.info(res['intervention']['text'])
                        col_a, col_b = st.columns(2)
                        with col_a:
                            st.subheader("AI Narrative Summary")
                            st.write(res['ai_summary'])
                        with col_b:
                            st.subheader("Risk Variances")
                            st.plotly_chart(px.bar(x=['Academic', 'Market', 'Professional'], 
                                               y=[res['risk_breakdown']['academic'], res['risk_breakdown']['market'], res['risk_breakdown']['professional']], 
                                               color=['Academic', 'Market', 'Professional'],
                                               title="Risk Contributing Factors"), use_container_width=True)
                else:
                    st.error("Engine failed to generate result.")
            except Exception as e:
                st.error(f"Connection Error: {str(e)}")
    else:
        st.info("Input profile details in the left sidebar and click 'Run' to see results.")

# --- BATCH UNDERWRITING ---
with tab_batch:
    st.subheader("📊 Portfolio Bulk Assessment Dashboard")
    st.write("Process bulk applications and visualize portfolio risk and yield.")
    
    uploaded = st.file_uploader("Upload Applicant CSV", type="csv")
    if uploaded:
        df = pd.read_csv(uploaded)
        st.info(f"📂 **{uploaded.name}** loaded with {len(df)} records.")
        scenario = st.selectbox("Simulated Market Environment", ["Standard", "Recession", "Market Boom"])
        
        if st.button("🚀 Start Batch Underwriting Process"):
            with st.spinner("Processing Large-Scale Inferences..."):
                mapping = {"course_type":["degree","major"], "cgpa":["gpa","grades"], "internships":["intern"], "certifications":["certs"], "mock_interviews_cleared":["mock"], "institute_tier":["tier"]}
                for target, aliases in mapping.items():
                    for alias in aliases:
                        if alias in df.columns and target not in df.columns: df.rename(columns={alias: target}, inplace=True)
                
                payload = df.to_dict(orient='records')
                response = requests.post("http://localhost:8000/simulate-scenario", json={"data": payload, "scenario": scenario})
                
                if response.status_code == 200:
                    results = response.json()
                    processed = [ {
                        "Decision": r['underwriting_decision']['decision'],
                        "Salary Forecast": r['salary_lpa'],
                        "Risk Category": r['default_risk']['category'],
                        "DTI Ratio": r['stress_test']['debt_to_income_ratio'],
                        "Verdict Reason": r['underwriting_decision']['reason']
                    } for r in results if r['status'] == 'success']
                    
                    res_df = pd.DataFrame(processed)
                    if not res_df.empty:
                        st.divider()
                        st.subheader("🏢 Portfolio Health Summary")
                        c1, c2, c3, c4, c5 = st.columns(5)
                        c1.metric("Batch Size", len(res_df))
                        c2.metric("Approved", len(res_df[res_df['Decision'].str.contains('Approve')]))
                        c3.metric("Conditional", len(res_df[res_df['Decision'].str.contains('Conditional')]))
                        c4.metric("Rejected", len(res_df[res_df['Decision'] == 'Rejected']))
                        avg_sal = res_df['Salary Forecast'].str.replace(' LPA', '').astype(float).mean()
                        c5.metric("Avg Salary", f"₹{avg_sal:.2f} LPA")

                        st.divider()
                        st.subheader("📊 Portfolio Yield & Risk Visualization")
                        fig_pie = px.pie(res_df, names='Decision', hole=.4, 
                                       color_discrete_sequence=px.colors.qualitative.Pastel)
                        st.plotly_chart(fig_pie, use_container_width=True)
                        
                        st.subheader("📋 Complete Decision Ledger")
                        st.dataframe(res_df, use_container_width=True)
                        csv_data = res_df.to_csv(index=False).encode('utf-8')
                        st.download_button(label="📥 Export Decision Ledger (CSV)", data=csv_data, file_name="underwriting_batch_results.csv", mime="text/csv")
                    else:
                        st.warning("Data quality issues detected. No records processed.")

# --- SYSTEM HISTORY ---
with tab_history:
    st.subheader("🕵️ Platform Historical Performance")
    stats = get_learning_stats()
    col1, col2, col3 = st.columns(3)
    col1.metric("Lifetime Decisions Audited", stats['total_inferences'])
    yield_val = (stats['approvals'] / stats['total_inferences'] * 100) if stats['total_inferences'] > 0 else 0
    col2.metric("Lifetime Approval Yield", f"{yield_val:.1f}%")
    col3.metric("Drift Status", "Stable (Standard)")
    
    st.divider()
    st.write("📂 **Recent Audit Trail (Latest 100 Records)**")
    if os.path.exists("data/audit_logs.jsonl"):
        audit_df = pd.read_json("data/audit_logs.jsonl", lines=True)
        log_view = pd.json_normalize(audit_df.to_dict(orient='records'))
        st.dataframe(log_view.tail(100), use_container_width=True)
    else:
        st.info("No audit logs available.")

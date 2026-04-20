import streamlit as st
import pandas as pd
import plotly.express as px
import os
import sys
import datetime

# Path setup for cloud
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import core engine and database
from app.main import core_predict
from app.database import get_learning_stats, log_decision

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Career Success AI Underwriter",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- SESSION STATE INITIALIZATION (TRUE STATE MANAGEMENT) ---
if 'prediction_result' not in st.session_state:
    st.session_state.prediction_result = None
if 'session_history' not in st.session_state:
    st.session_state.session_history = []  # Single source of truth for current sessions
if 'last_input' not in st.session_state:
    st.session_state.last_input = None

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    div[data-testid="stMetricValue"] { font-size: 1.8rem !important; font-weight: 700; color: #3b82f6; }
    div[data-testid="stMetricLabel"] { font-size: 0.9rem !important; color: #aaa; }
    .stTabs [data-baseweb="tab"] { 
        background-color: #1e2130; 
        border-radius: 8px; 
        color: #fff; 
        padding: 10px 20px; 
        margin-right: 5px;
    }
    .stTabs [aria-selected="true"] { background-color: #3b82f6 !important; }
    .decision-banner {
        padding: 25px;
        border-radius: 15px;
        margin: 16px 0;
        border-left: 10px solid;
    }
    .empty-state {
        text-align: center;
        padding: 50px;
        background: #1e2130;
        border-radius: 15px;
        color: #aaa;
        border: 2px dashed #343a40;
    }
    </style>
""", unsafe_allow_html=True)

# --- UTILITY FUNCTIONS ---

def preprocess_input(sidebar_data):
    """Clean and map sidebar inputs to model format."""
    tier_map = {"Tier 1 (High)": "Tier 1", "Tier 2 (Mid)": "Tier 2", "Tier 3 (Standard)": "Tier 3"}
    return {
        "course_type": sidebar_data['course_type'],
        "cgpa": sidebar_data['cgpa'],
        "internships": sidebar_data['internships'],
        "certifications": sidebar_data['certifications'],
        "academic_consistency": "High",
        "institute_tier": tier_map[sidebar_data['institute_tier']],
        "placement_cell_activity": "High",
        "industry_demand_index": sidebar_data['demand'],
        "regional_job_density": sidebar_data['density'],
        "job_portal_activity": sidebar_data['portal'],
        "mock_interviews_cleared": sidebar_data['mock'],
        "loan_amount": sidebar_data['amount'],
        "interest_rate": sidebar_data['rate'],
        "tenure_years": sidebar_data['tenure']
    }

def run_prediction(input_data):
    """Execute model prediction and log results to session state and database."""
    try:
        with st.spinner("AI Underwriter Analyzing Profile..."):
            res = core_predict(input_data)
            if res and res.get('status') == 'success':
                st.session_state.prediction_result = res
                st.session_state.last_input = input_data
                
                # Update Session History (TRUE STATE)
                history_entry = {
                    "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "decision": res['underwriting_decision']['decision'],
                    "salary": res['salary_lpa'],
                    "risk": res['default_risk']['category'],
                    "dti": f"{res['stress_test']['debt_to_income_ratio']*100:.1f}%"
                }
                st.session_state.session_history.append(history_entry)
                
                # LOG TO PERMANENT DATABASE (Optional but kept for global stats)
                log_decision(input_data, res, res['underwriting_decision'])
                return res
            else:
                st.error(f"Engine Error: {res.get('error_message', 'Unknown error')}")
                return None
    except Exception as e:
        st.error(f"Runtime Exception: {str(e)}")
        return None

def plot_risk_variance(risk_breakdown):
    """Generate dynamic Plotly chart for risk factors."""
    a_score = risk_breakdown.get('academic', 0)
    m_score = risk_breakdown.get('market', 0)
    p_score = risk_breakdown.get('professional', 0)

    fig = px.bar(
        x=["Academic Risk", "Market Risk", "Professional Risk"],
        y=[a_score, m_score, p_score],
        color=["Academic Risk", "Market Risk", "Professional Risk"],
        color_discrete_map={
            "Academic Risk":     "#3b82f6",
            "Market Risk":       "#f59e0b",
            "Professional Risk": "#ef4444"
        },
        text=[f"{a_score}%", f"{m_score}%", f"{p_score}%"],
        labels={"y": "Risk Score (%)", "x": "Factor"}
    )
    fig.update_traces(textposition='outside')
    fig.update_layout(
        showlegend=False, 
        yaxis_range=[0, 110],
        margin=dict(l=20, r=20, t=20, b=20),
        height=350,
        template="plotly_dark"
    )
    return fig

# --- MAIN UI ---

st.title("⚖️ AI Education Loan Underwriting System")
st.markdown("Automated Career Verification & Credit Intelligence Platform")

tab_single, tab_batch, tab_history, tab_report = st.tabs([
    "📂 Individual Assessment",
    "📊 Portfolio Batch",
    "🕵️ Session History & Stats",
    "📖 Project Report"
])

# --- SIDEBAR INPUTS ---
st.sidebar.title("👤 Applicant Profile")
st.sidebar.divider()

sb_data = {}
sb_data['course_type'] = st.sidebar.selectbox("Field of Study", ["Engineering", "MBA", "Nursing", "Data Science", "Finance", "Arts"])
sb_data['cgpa'] = st.sidebar.slider("Current CGPA", 4.0, 10.0, 8.5)
sb_data['internships'] = st.sidebar.number_input("Internships Completed", 0, 5, 1)
sb_data['certifications'] = st.sidebar.number_input("Certifications Earned", 0, 10, 2)
sb_data['institute_tier'] = st.sidebar.selectbox("College Quality", ["Tier 1 (High)", "Tier 2 (Mid)", "Tier 3 (Standard)"])

st.sidebar.subheader("📊 Market Signals")
sb_data['demand'] = st.sidebar.slider("Industry Demand (0–1)", 0.0, 1.0, 0.7)
sb_data['density'] = st.sidebar.slider("Regional Job Density (0–1)", 0.0, 1.0, 0.6)
sb_data['portal'] = st.sidebar.slider("Job Portal Activity (0–1)", 0.0, 1.0, 0.5)
sb_data['mock'] = st.sidebar.number_input("Mock Interviews Cleared", 0, 10, 3)

st.sidebar.subheader("💰 Loan Terms")
sb_data['amount'] = st.sidebar.number_input("Requested Loan (₹)", 100000, 5000000, 1000000)
sb_data['rate'] = st.sidebar.slider("Base Interest Rate (%)", 5.0, 15.0, 10.5)
sb_data['tenure'] = st.sidebar.slider("Repayment Term (Years)", 1, 25, 15)

if st.sidebar.button("👉 Run Full Underwriting", use_container_width=True):
    processed_input = preprocess_input(sb_data)
    run_prediction(processed_input)

# --- TAB 1: INDIVIDUAL ASSESSMENT ---
with tab_single:
    if st.session_state.prediction_result:
        res = st.session_state.prediction_result
        
        # 0. Download Report Button
        report_text = f"""
# ⚖️ CAREER UNDERWRITING ASSESSMENT REPORT
Generated on: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## 1. EXECUTIVE SUMMARY
- **Decision:** {res['underwriting_decision']['decision']}
- **Predicted Salary:** {res['salary_lpa']}
- **Risk Category:** {res['default_risk']['category']}
- **Interest Rate:** {res['pricing_breakdown']['final_rate']}%

## 2. UNDERWRITING REASONING
{res['underwriting_decision']['reason']}

## 3. RISK BREAKDOWN
- **Academic Risk:** {res['risk_breakdown']['academic']}%
- **Market Risk:** {res['risk_breakdown']['market']}%
- **Professional Risk:** {res['risk_breakdown']['professional']}%

## 4. AI NARRATIVE
{res['ai_summary']}

## 5. RECOMMENDED ACTIONS
{chr(10).join([f'- {r["recommendation"]}' for r in res.get('recommendations', [])])}

---
*This report is generated by the AI Education Loan Underwriting System.*
"""
        st.download_button(
            label="📄 Download Professional Underwriting Report",
            data=report_text,
            file_name=f"Assessment_Report_{datetime.datetime.now().strftime('%Y%m%d')}.md",
            mime="text/markdown",
            use_container_width=True
        )

        # 1. Metrics Row
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Predicted Salary", f"₹{res.get('salary_lpa', 'N/A')}")
        m2.metric("Monthly EMI", f"₹{res.get('stress_test', {}).get('monthly_emi', 0):,.0f}")
        m3.metric("DTI Ratio", f"{res.get('stress_test', {}).get('debt_to_income_ratio', 0)*100:.1f}%")
        m4.metric("Risk Category", res.get('default_risk', {}).get('category', 'N/A'))

        # 2. Verdict Banner
        uw = res.get('underwriting_decision', {})
        decision = uw.get('decision', 'Manual Review')
        colors = {
            "Approved": "#28a745", "Fast-Track Approval": "#155724",
            "Conditional Approval": "#ffc107", "Manual Review": "#17a2b8",
            "Rejected": "#dc3545"
        }
        color = colors.get(decision, "#007bff")
        
        st.markdown(f"""
            <div class="decision-banner" style="background:{color}22; border-color:{color};">
                <h1 style="color:{color}; margin:0;">Verdict: {decision}</h1>
                <p style="font-size:1.1rem; margin-top:10px;"><b>Reasoning:</b> {uw.get('reason', '')}</p>
                <p style="font-size:1rem;"><b>Final Interest Rate:</b> {res.get('pricing_breakdown', {}).get('final_rate', 'N/A')}%</p>
            </div>
        """, unsafe_allow_html=True)

        # 3. Details and Visualization
        col_left, col_right = st.columns([1.2, 0.8])
        
        with col_left:
            st.subheader("🔍 AI Model Insights")
            ai = res.get('ai_report', {})
            st.write(ai.get('narrative', 'No narrative available.'))
            
            st.divider()
            c1, c2 = st.columns(2)
            with c1:
                st.write("**⚠️ Risk Factors**")
                for rf in ai.get('risk_factors', []):
                    st.caption(f"• {rf}")
            with c2:
                st.write("**📈 Career Advice**")
                for advice in ai.get('career_advice', []):
                    st.caption(f"• {advice}")

        with col_right:
            st.subheader("📊 Risk Profile Variance")
            st.plotly_chart(plot_risk_variance(res.get('risk_breakdown', {})), use_container_width=True)
            
            if res.get('intervention', {}).get('text'):
                st.info(f"**💡 Scenario Insight:** {res['intervention']['text']}")
            
            # --- WHAT-IF SIMULATOR CARD ---
            st.markdown("""
                <div style="background:#1e293b; padding:20px; border-radius:12px; border-left:5px solid #3b82f6; margin-top:20px;">
                    <h4 style="margin:0; color:#3b82f6;">🚀 Future Potential (What-If?)</h4>
                    <p style="font-size:0.9rem; color:#aaa; margin-top:5px;">How can you improve your profile?</p>
                </div>
            """, unsafe_allow_html=True)
            
            with st.expander("📈 Simulate Career Growth"):
                st.write("See how small changes can impact your risk profile:")
                c1, c2 = st.columns(2)
                with c1:
                    extra_intern = st.checkbox("Add 1 Internship")
                with c2:
                    extra_cert = st.checkbox("Add 2 Certifications")
                
                if extra_intern or extra_cert:
                    # Run a mini simulation
                    sim_input = st.session_state.last_input.copy()
                    if extra_intern: sim_input['internships'] += 1
                    if extra_cert: sim_input['certifications'] += 2
                    
                    with st.spinner("Calculating impact..."):
                        sim_res = core_predict(sim_input)
                        if sim_res['status'] == 'success':
                            st.write(f"**New Risk Level:** {sim_res['default_risk']['category']}")
                            st.write(f"**New Salary:** {sim_res['salary_lpa']}")
                            if sim_res['default_risk']['category'] != res['default_risk']['category']:
                                st.success("🎉 This change improves your overall risk category!")
                            else:
                                st.info("This improves your stats but keeps you in the same risk category.")
    else:
        st.markdown("""
            <div class="empty-state">
                <h2 style="margin:0;">No Active Assessment</h2>
                <p>Configure the profile in the sidebar and click <b>'Run Full Underwriting'</b> to see results here.</p>
            </div>
        """, unsafe_allow_html=True)

# --- TAB 2: BATCH PORTFOLIO ---
with tab_batch:
    st.subheader("📊 Portfolio Bulk Assessment")
    uploaded = st.file_uploader("Upload Applicant CSV", type="csv")
    
    if uploaded:
        df = pd.read_csv(uploaded)
        st.success(f"Loaded {len(df)} records from {uploaded.name}")
        scenario = st.selectbox("Market Scenario Simulation", ["Standard", "Recession", "Market Boom"])
        
        if st.button("🚀 Process Batch"):
            # Minimal mapping for demo
            mapping = {"course_type": ["degree"], "cgpa": ["gpa"], "internships": ["intern"]}
            for target, aliases in mapping.items():
                for a in aliases:
                    if a in df.columns and target not in df.columns:
                        df.rename(columns={a: target}, inplace=True)
            
            results = []
            progress = st.progress(0)
            for i, row in df.iterrows():
                r = core_predict(row.to_dict())
                if r['status'] == 'success':
                    results.append({
                        "Applicant": row.get('name', f"ID_{i}"),
                        "Decision": r['underwriting_decision']['decision'],
                        "Salary": r['salary_lpa'],
                        "Risk": r['default_risk']['category'],
                        "DTI": f"{r['stress_test']['debt_to_income_ratio']*100:.1f}%"
                    })
                progress.progress((i + 1) / len(df))
            
            if results:
                res_df = pd.DataFrame(results)
                st.dataframe(res_df, use_container_width=True)
                st.plotly_chart(px.pie(res_df, names="Decision", title="Portfolio Decision Distribution"))
            else:
                st.error("Could not process any records. Ensure CSV matches expected features.")
    else:
        st.markdown("""
            <div class="empty-state">
                <h2 style="margin:0;">No CSV Uploaded</h2>
                <p>Upload a list of applicants to perform bulk underwriting and scenario simulations.</p>
            </div>
        """, unsafe_allow_html=True)

# --- TAB 3: SESSION HISTORY & STATS ---
with tab_history:
    st.subheader("🕵️ Your Session Intelligence")
    
    if st.session_state.session_history:
        # Dynamic calculation from REAL session data
        history_df = pd.DataFrame(st.session_state.session_history)
        total = len(history_df)
        approvals = len(history_df[history_df['decision'].str.contains('Approve')])
        yield_val = f"{(approvals / total * 100):.1f}%"
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Your Decisions", total)
        c2.metric("Your Approval Rate", yield_val)
        c3.metric("System Status", "Live Monitoring")
        
        st.divider()
        st.subheader("📋 Session Audit Log")
        st.dataframe(history_df.iloc[::-1], use_container_width=True) # Reverse for latest first
        
        if st.button("🗑️ Clear My Session History"):
            st.session_state.session_history = []
            st.rerun()
    else:
        st.markdown("""
            <div class="empty-state">
                <h2 style="margin:0;">No Personal History Yet</h2>
                <p>Run your first assessment to see dynamic metrics and audit logs here.</p>
            </div>
        """, unsafe_allow_html=True)

# --- TAB 4: PROJECT REPORT ---
with tab_report:
    report_path = os.path.join(os.path.dirname(__file__), '..', 'PROJECT_REPORT.md')
    if os.path.exists(report_path):
        with open(report_path, 'r', encoding='utf-8') as f:
            st.markdown(f.read())
    else:
        st.error("Project Report file not found.")

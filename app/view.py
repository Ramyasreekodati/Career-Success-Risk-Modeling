import streamlit as st
import pandas as pd
import plotly.express as px
import os
import sys

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

# --- SESSION STATE INITIALIZATION ---
if 'prediction_result' not in st.session_state:
    st.session_state.prediction_result = None
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
    """Execute model prediction and log results."""
    try:
        with st.spinner("AI Underwriter Analyzing Profile..."):
            res = core_predict(input_data)
            if res and res.get('status') == 'success':
                st.session_state.prediction_result = res
                st.session_state.last_input = input_data
                # LOG TO DATABASE
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
        height=350
    )
    return fig

# --- MAIN UI ---

st.title("⚖️ AI Education Loan Underwriting System")
st.markdown("Automated Career Verification & Credit Intelligence Platform")

tab_single, tab_batch, tab_history = st.tabs([
    "📂 Individual Loan Assessment",
    "📊 Portfolio Batch Underwriting",
    "🕵️ System Summary & History"
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
                st.info(f"**💡 Insight:** {res['intervention']['text']}")
    else:
        st.info("👋 Welcome! Fill in the applicant profile on the left and click **'Run Full Underwriting'** to start.")

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

# --- TAB 3: SYSTEM SUMMARY ---
with tab_history:
    st.subheader("🕵️ Platform Historical Analytics")
    
    stats = get_learning_stats()
    total = stats.get('total_inferences', 0)
    approvals = stats.get('approvals', 0)
    yield_val = f"{(approvals / total * 100):.1f}%" if total > 0 else "0.0%"
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Decisions", total)
    c2.metric("Approval Rate", yield_val)
    c3.metric("System Health", "Active" if total > 0 else "Idle")
    
    st.divider()
    
    # Load recent logs
    from app.database import LOG_FILE
    if os.path.exists(LOG_FILE):
        try:
            audit_df = pd.read_json(LOG_FILE, lines=True)
            st.subheader("📋 Recent Audit Logs")
            # Flatten some fields for better display
            display_df = audit_df.copy()
            display_df['Decision'] = display_df['underwriting'].apply(lambda x: x.get('decision') if isinstance(x, dict) else x)
            display_df['Salary Forecast'] = display_df['prediction'].apply(lambda x: x.get('salary_lpa') if isinstance(x, dict) else 'N/A')
            
            st.dataframe(
                display_df[['timestamp', 'Decision', 'Salary Forecast']].tail(20).iloc[::-1],
                use_container_width=True
            )
        except Exception as e:
            st.warning("Logs found but could not be parsed yet.")
    else:
        st.info("No historical data available. Run some assessments to populate this dashboard.")

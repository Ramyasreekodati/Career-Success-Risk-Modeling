import streamlit as st
import pandas as pd
import plotly.express as px
import os
import sys

st.set_page_config(page_title="AI Education Loan Underwriter", layout="wide")

# Path setup for cloud
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import core engine directly (no HTTP needed on cloud)
from app.main import core_predict
from app.database import get_learning_stats

# Custom CSS
st.markdown("""
    <style>
    div[data-testid="stMetricValue"] { font-size: 1.8rem !important; font-weight: 700; }
    div[data-testid="stMetricLabel"] { font-size: 0.9rem !important; color: #aaa; }
    .stTabs [data-baseweb="tab"] { background-color: #1e2130; border-radius: 8px; color: #fff; padding: 10px 20px; }
    .stTabs [aria-selected="true"] { background-color: #3b82f6 !important; }
    </style>
""", unsafe_allow_html=True)

st.title("⚖️ AI Education Loan Underwriting System")
st.markdown("Automated Career Verification & Credit Intelligence Platform")

tab_single, tab_batch, tab_history = st.tabs([
    "📂 Individual Loan Assessment",
    "📊 Portfolio Batch Underwriting",
    "🕵️ System Summary & History"
])

# ─── TAB 1: Individual Assessment ───────────────────────────────────────────
with tab_single:
    st.sidebar.title("👤 Applicant Profile")
    st.sidebar.divider()

    course_type    = st.sidebar.selectbox("Field of Study", ["Engineering", "MBA", "Nursing", "Data Science", "Finance", "Arts"])
    cgpa           = st.sidebar.slider("Current CGPA", 4.0, 10.0, 8.5)
    internships    = st.sidebar.number_input("Internships Completed", 0, 5, 1)
    certifications = st.sidebar.number_input("Certifications Earned", 0, 10, 2)
    institute_tier = st.sidebar.selectbox("College Quality", ["Tier 1 (High)", "Tier 2 (Mid)", "Tier 3 (Standard)"])

    st.sidebar.subheader("📊 Market Signals")
    demand         = st.sidebar.slider("Industry Demand (0–1)", 0.0, 1.0, 0.7, help="Higher = more jobs available in your field")
    density        = st.sidebar.slider("Regional Job Density (0–1)", 0.0, 1.0, 0.6, help="Higher = more employers in your region")
    portal         = st.sidebar.slider("Job Portal Activity (0–1)", 0.0, 1.0, 0.5, help="How actively the applicant is applying online")
    mock           = st.sidebar.number_input("Mock Interviews Cleared", 0, 10, 3)

    st.sidebar.subheader("💰 Loan Terms")
    amount         = st.sidebar.number_input("Requested Loan (₹)", 100000, 5000000, 1000000)
    rate           = st.sidebar.slider("Base Interest Rate (%)", 5.0, 15.0, 10.5)
    tenure         = st.sidebar.slider("Repayment Term (Years)", 1, 25, 15)

    tier_map = {"Tier 1 (High)": "Tier 1", "Tier 2 (Mid)": "Tier 2", "Tier 3 (Standard)": "Tier 3"}
    input_data = {
        "course_type": course_type, "cgpa": cgpa,
        "internships": internships, "certifications": certifications,
        "academic_consistency": "High",
        "institute_tier": tier_map[institute_tier],
        "placement_cell_activity": "High",
        "industry_demand_index": demand,
        "regional_job_density": density,
        "job_portal_activity": portal,
        "mock_interviews_cleared": mock,
        "loan_amount": amount,
        "interest_rate": rate,
        "tenure_years": tenure
    }

    if st.sidebar.button("👉 Run Full Underwriting"):
        with st.spinner("Running AI Underwriting Engine..."):
            try:
                res = core_predict(input_data)

                if res and res.get('status') == 'success':
                    st.subheader("🎓 Personal Assessment Result")

                    # ── Metric cards with safe defaults ──
                    salary_display  = res.get('salary_lpa', 'N/A')
                    emi_display     = res.get('stress_test', {}).get('monthly_emi', 0)
                    dti_display     = res.get('stress_test', {}).get('debt_to_income_ratio', 0)
                    risk_display    = res.get('default_risk', {}).get('category', 'N/A')

                    m1, m2, m3, m4 = st.columns(4)
                    m1.metric("Predicted Salary", f"₹{salary_display}")
                    m2.metric("Monthly EMI", f"₹{emi_display:,.0f}")
                    m3.metric("Income-to-Debt Ratio", f"{dti_display*100:.1f}%")
                    m4.metric("Risk Category", risk_display)

                    # ── Verdict Banner ──
                    uw = res.get('underwriting_decision', {})
                    decision_text   = uw.get('decision', 'N/A')
                    reason_text     = uw.get('reason', '')
                    final_rate      = res.get('pricing_breakdown', {}).get('final_rate', 'N/A')
                    rate_band       = res.get('pricing_breakdown', {}).get('rate_band', '')

                    colors = {
                        "Approved": "#28a745", "Fast-Track Approval": "#155724",
                        "Conditional Approval": "#ffc107", "Manual Review": "#17a2b8",
                        "Rejected": "#dc3545"
                    }
                    color = colors.get(decision_text, "#007bff")

                    st.markdown(f"""
                        <div style="background:{color}22; padding:25px; border-radius:15px; border-left:10px solid {color}; margin:16px 0">
                            <h1 style="color:{color}; margin:0; font-size:2rem">Verdict: {decision_text}</h1>
                            <p style="font-size:1.1rem; margin-top:10px"><b>Reasoning:</b> {reason_text}</p>
                            <p style="font-size:1rem"><b>Recommended Rate:</b> {final_rate}% &nbsp;|&nbsp; <em>{rate_band}</em></p>
                        </div>
                    """, unsafe_allow_html=True)

                    # ── Analytical Breakdown ──
                    with st.expander("🔍 Detailed Analytical Breakdown", expanded=True):
                        ai = res.get('ai_report', {})

                        st.markdown(f"**📋 Structured Reasoning:** {ai.get('reasoning', reason_text)}")
                        st.divider()

                        col_a, col_b = st.columns(2)
                        with col_a:
                            st.subheader("⚠️ Key Risk Factors")
                            for rf in ai.get('risk_factors', []):
                                st.markdown(f"- {rf}")
                        with col_b:
                            st.subheader("📈 Career Growth Advice")
                            for advice in ai.get('career_advice', []):
                                st.markdown(f"- {advice}")

                        st.divider()
                        st.subheader("🗺️ Career Outlook")
                        st.info(ai.get('narrative', res.get('ai_summary', '')))

                        if res.get('intervention', {}).get('text'):
                            st.subheader("💡 What-If Simulation")
                            st.success(res['intervention']['text'])

                        # Risk scores computed from REAL model output (salary, EMI, DTI)
                        rb = res.get('risk_breakdown', {})
                        a_score = rb.get('academic', 0)
                        m_score = rb.get('market', 0)
                        p_score = rb.get('professional', 0)

                        st.subheader("📊 Risk Factor Variance")
                        st.caption("Academic = CGPA + Tier | Market = DTI + EMI burden | Professional = Internships + Predicted Salary")
                        risk_fig = px.bar(
                            x=["Academic Risk", "Market Risk", "Professional Risk"],
                            y=[a_score, m_score, p_score],
                            color=["Academic Risk", "Market Risk", "Professional Risk"],
                            color_discrete_map={
                                "Academic Risk":     "#3b82f6",
                                "Market Risk":       "#f59e0b",
                                "Professional Risk": "#ef4444"
                            },
                            text=[f"{a_score}%", f"{m_score}%", f"{p_score}%"],
                            labels={"y": "Risk Score (0–100, lower is better)"}
                        )
                        risk_fig.update_traces(textposition='outside')
                        risk_fig.update_layout(showlegend=False, yaxis_range=[0, 110])
                        st.plotly_chart(risk_fig, use_container_width=True)
                else:
                    st.error(f"⚠️ Engine Error: {res.get('error_message', 'Unknown error')}")
            except Exception as e:
                st.error(f"Runtime Error: {str(e)}")
    else:
        st.info("Fill in the applicant profile on the left sidebar, then click 'Run Underwriting'.")

# ─── TAB 2: Batch Portfolio ──────────────────────────────────────────────────
with tab_batch:
    st.subheader("📊 Portfolio Bulk Assessment Dashboard")

    uploaded = st.file_uploader("Upload Applicant CSV", type="csv")
    if uploaded:
        df = pd.read_csv(uploaded)
        st.info(f"📂 **{uploaded.name}** loaded with **{len(df)}** records.")
        scenario = st.selectbox("Market Scenario", ["Standard", "Recession", "Market Boom"])

        if st.button("🚀 Start Batch Underwriting"):
            with st.spinner("Processing batch…"):
                # Column alias mapping
                alias_map = {
                    "course_type": ["degree", "major"],
                    "cgpa": ["gpa", "grades"],
                    "internships": ["intern"],
                    "certifications": ["certs"],
                    "mock_interviews_cleared": ["mock"],
                    "institute_tier": ["tier"]
                }
                for target, aliases in alias_map.items():
                    for a in aliases:
                        if a in df.columns and target not in df.columns:
                            df.rename(columns={a: target}, inplace=True)

                adjustments = {
                    "Recession":    {"demand": -0.4, "density": -0.2},
                    "Market Boom":  {"demand":  0.3, "density":  0.2},
                    "Standard":     {"demand":  0.0, "density":  0.0}
                }
                adj = adjustments[scenario]

                records, processed = df.to_dict(orient='records'), []
                for s in records:
                    s['industry_demand_index'] = max(0, min(1, float(s.get('industry_demand_index', 0.5)) + adj['demand']))
                    s['regional_job_density']  = max(0, min(1, float(s.get('regional_job_density',  0.5)) + adj['density']))
                    r = core_predict(s)
                    if r and r.get('status') == 'success':
                        processed.append({
                            "Decision":        r['underwriting_decision']['decision'],
                            "Salary Forecast": r['salary_lpa'],
                            "Risk Category":   r['default_risk']['category'],
                            "DTI %":           f"{r['stress_test']['debt_to_income_ratio']*100:.1f}%",
                            "Rate Band":       r['pricing_breakdown'].get('rate_band', ''),
                            "Reason":          r['underwriting_decision']['reason']
                        })

                if processed:
                    res_df = pd.DataFrame(processed)

                    st.divider()
                    st.subheader("🏢 Portfolio Health Summary")
                    c1, c2, c3, c4, c5 = st.columns(5)
                    n_approved    = len(res_df[res_df['Decision'].str.contains('Approve', na=False)])
                    n_conditional = len(res_df[res_df['Decision'].str.contains('Conditional', na=False)])
                    n_rejected    = len(res_df[res_df['Decision'] == 'Rejected'])
                    avg_sal = (
                        res_df['Salary Forecast'].str.replace(' LPA', '', regex=False)
                        .astype(float).mean()
                    )
                    c1.metric("Batch Size",    str(len(res_df)))
                    c2.metric("Approved",      str(n_approved))
                    c3.metric("Conditional",   str(n_conditional))
                    c4.metric("Rejected",      str(n_rejected))
                    c5.metric("Avg Salary",    f"₹{avg_sal:.2f} LPA")

                    st.divider()
                    st.subheader("📊 Portfolio Yield Visualization")
                    st.plotly_chart(
                        px.pie(res_df, names='Decision', hole=.4,
                               color_discrete_sequence=px.colors.qualitative.Pastel),
                        use_container_width=True
                    )

                    st.subheader("📋 Decision Ledger")
                    st.dataframe(res_df, use_container_width=True)

                    csv_bytes = res_df.to_csv(index=False).encode('utf-8')
                    st.download_button("📥 Export CSV", data=csv_bytes,
                                       file_name="underwriting_results.csv", mime="text/csv")
                else:
                    st.warning("No records were successfully processed. Check CSV column names.")

# ─── TAB 3: System History ───────────────────────────────────────────────────
with tab_history:
    st.subheader("🕵️ Platform Historical Performance")

    stats = get_learning_stats()
    total  = stats.get('total_inferences', 0)
    approvals = stats.get('approvals', 0)
    yield_val = f"{(approvals / total * 100):.1f}%" if total > 0 else "N/A"

    col1, col2, col3 = st.columns(3)
    col1.metric("Lifetime Decisions", str(total) if total > 0 else "N/A")
    col2.metric("Lifetime Approval Yield", yield_val)
    col3.metric("Drift Status", "N/A (logs required)")

    st.divider()
    log_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'audit_logs.jsonl')
    if os.path.exists(log_path):
        audit_df = pd.read_json(log_path, lines=True)
        st.write(f"📂 **Showing latest {min(100, len(audit_df))} records**")
        st.dataframe(audit_df.tail(100), use_container_width=True)
    else:
        st.info("No audit logs available yet. Run individual underwriting sessions to populate this view.")

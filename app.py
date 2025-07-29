# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io

# Page config
st.set_page_config(page_title="Resume vs Reality", layout="wide")
st.markdown("""
<style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    h1, h2, h3 {
        color: #2e2e2e;
    }
    .stTabs [role="tab"] {
        background-color: #f1f3f6;
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        margin-right: 0.5rem;
        font-weight: bold;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #60a5fa, #3b82f6);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

st.title("📄 Resume vs Reality")
st.caption("Think of this like your older sister giving you the real talk — honest, loving, and full of solid advice.")

# Load dataset
@st.cache_data

def load_data():
    return pd.read_csv("genz_resume_market_data.csv")

df = load_data()

# Tabs
tabs = st.tabs(["👤 Profile Snapshot", "📈 Market Comparison", "📊 Match Score", "💡 Suggestions", "📥 Download Report"])

# --- Tab 0: Profile Snapshot ---
with tabs[0]:
    st.subheader("👤 Profile Snapshot")
    resume_ids = df["ResumeID"].unique()
    selected_resume = st.selectbox("🎯 Select a Resume ID to Explore", resume_ids)
    resume_data = df[df["ResumeID"] == selected_resume].iloc[0]

    st.markdown("### 💼 Quick Glance")
    st.write("Let’s break this down like your favorite sibling explaining what matters — quick, honest, and always with your best interest in mind.")

    col1, col2, col3 = st.columns([1,1,1])
    with col1:
        st.metric("🎓 Education Level", resume_data['EducationLevel'])
        st.metric("🧠 Gen Z Traits", resume_data['GenZ_Trait_Tags'])
    with col2:
        st.metric("📌 Applied Role", resume_data['JobAppliedFor'])
        st.metric("📑 Resume Style", resume_data['ResumeStyle'])
    with col3:
        st.metric("🎯 AI Match Score", f"{resume_data['AI_MatchScore']}/100")
        st.metric("🎟 Certifications", resume_data['Certifications'])

    st.markdown("---")
    st.markdown("### 🧬 Field of Study")
    st.info(f"You’re coming from a background in **{resume_data['FieldOfStudy']}**, which is a solid start for someone aiming to become a {resume_data['JobAppliedFor']}. Let's see if your skills align.")

    st.markdown("### 🧰 Skill Comparison")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**✅ Skills You Listed**")
        st.code("\n".join(resume_data["SkillsListed"].split(", ")))
    with col2:
        st.markdown("**📌 Skills the Role Wants**")
        st.code("\n".join(resume_data["JobPostingSkillsRequired"].split(", ")))

    listed = len(resume_data['SkillsListed'].split(', '))
    required = len(resume_data['JobPostingSkillsRequired'].split(', '))
    gap = required - listed

    st.markdown("### 💡 Insight + Big Sis Advice")
    if gap > 0:
        st.warning(f"You listed **{listed}** skills, but this role expects around **{required}**. That's a gap of {gap} important ones. Don’t panic — now we know what to fix. This is your growth checklist!")
        st.info("💬 Tip: Try adding **one skill per project** you've done — be specific. Recruiters love context, not just buzzwords.")
    elif gap == 0:
        st.success("You're right on target with skill count! Now make sure they're **quality, not just quantity**. Would an employer *feel* your experience from those words?")
    else:
        st.success("You've got more skills listed than required — great! But double-check: Are they relevant to **this** job? Sometimes trimming down is powerful.")

    st.markdown("---")
    st.markdown("👀 Let’s dive deeper into market trends next. If you were a product, how in-demand would you be?")

# --- Tab 4: Download Report ---
with tabs[4]:
    st.subheader("📥 Export Your Report")

    report_text = f'''
    📄 Resume ID: {resume_data["ResumeID"]}
    🧠 Match Score: {resume_data["AI_MatchScore"]}/100
    ❌ Skill Gap: {gap}
    🎨 Style: {resume_data["ResumeStyle"]}
    ✨ Advice:
    - Close skill gap by learning {gap} if applicable.
    - Optimize resume structure based on ATS-friendliness.
    - Use action-driven language and match job keywords.
    '''
    st.download_button(
        label="Download as TXT",
        data=report_text.encode('utf-8'),
        file_name="resume_vs_reality_report.txt",
        mime="text/plain"
    )

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
    .welcome-container {
        background: linear-gradient(to right, #e0f7fa, #e8f5e9);
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
        margin-bottom: 2rem;
    }
    .quote-box {
        background-color: #fff8e1;
        padding: 1rem;
        border-left: 5px solid #ffd54f;
        border-radius: 8px;
        font-style: italic;
        margin-top: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Load dataset
@st.cache_data

def load_data():
    return pd.read_csv("genz_resume_market_data.csv")

df = load_data()

# --- Welcome Tab ---
st.markdown("""
<div class="welcome-container">
<h1>💼 Welcome to <span style='color:#3b82f6'>Resume vs Reality</span></h1>
<h3>Your sassy, smart career wingwoman. 💁‍♀️</h3>
<p>
Ever stared at your resume wondering, "Will this get me hired or ghosted?" <br>
You're not alone — and you're not going in blind anymore.
</p>
<p>
This app compares your resume to real job market data and gives you blunt-but-loving advice (like a slightly judgy older sister who just wants to see you win).
</p>
</div>
""", unsafe_allow_html=True)

with st.expander("🔍 What is This App Really About?"):
    st.markdown("""
- 💥 **Mirror meets mentor**: Know what your resume says *and* what it’s missing.
- 🔍 **Resume vs Job Data**: We pull trends across domains — what gets people hired, what you’re lacking, what you need to add.
- 💬 **Witty, real-world advice**: Because the job hunt doesn’t need to be a soul-sucking scroll.
""")

with st.expander("🛠️ How to Use This App"):
    st.markdown("""
1. **👤 Profile Snapshot** – Upload or select a sample resume. Get the overview.
2. **📈 Market Comparison** – How does your resume stand in your chosen field?
3. **📊 Match Score** – Visual breakdown of how close you are to ideal profiles.
4. **💡 Suggestions** – Helpful, no-BS advice to close skill and keyword gaps.
5. **📥 Download Report** – Save your growth map as a TXT report.
""")

with st.expander("🎁 What You'll Walk Away With"):
    st.markdown("""
- 🔎 **Insights that matter** — no more guessing what to fix.
- 🧠 **Understanding your job-readiness** like a hiring manager would.
- 📌 **Skill roadmaps** based on what others got hired for.
- 💪 **Confidence** that comes from clarity.
""")

st.markdown("""
<div class="quote-box">
“Resumes don’t just speak for you — they whisper to recruiters. Let’s make sure yours is saying the right things.”
</div>

🚀 **Ready? Let’s build a resume that doesn’t just talk — it lands you offers.**
""", unsafe_allow_html=True)

# Tabs
tabs = st.tabs(["👤 Profile Snapshot", "📈 Market Comparison", "📊 Match Score", "💡 Suggestions", "📥 Download Report"])

# Tab 1: Profile Snapshot
with tabs[0]:
    st.header("👤 Profile Snapshot")
    resume_ids = df['ResumeID'].unique()
    selected_id = st.selectbox("Select a Resume ID", resume_ids)
    resume_data = df[df['ResumeID'] == selected_id].iloc[0]

    st.subheader("Resume Summary")
    st.write(f"**Age:** {resume_data['Age']}")
    st.write(f"**Education:** {resume_data['EducationLevel']} in {resume_data['FieldOfStudy']}")
    st.write(f"**Applied For:** {resume_data['JobAppliedFor']}")
    st.write(f"**Resume Style:** {resume_data['ResumeStyle']}")
    st.write(f"**Certifications:** {resume_data['Certifications']}")

    st.markdown("---")
    st.subheader("🎯 Resume Score")
    ai_score = resume_data['AI_MatchScore']
    st.metric("AI Match Score", f"{ai_score}/100")
    st.progress(ai_score / 100)

    if ai_score >= 85:
        st.success("🔥 This resume is job-ready. Very strong match with market expectations!")
    elif ai_score >= 60:
        st.warning("⚠️ Decent resume, but needs tweaks to be more aligned with current hiring trends.")
    else:
        st.error("🚨 Your resume is likely being overlooked. Let’s upgrade it together.")

# Tab 2: Market Comparison
with tabs[1]:
    st.header("📈 Market Comparison")
    domain_scores = df.groupby("Domain")["AI_MatchScore"].mean().sort_values()
    st.subheader("🔍 Average AI Match Score by Domain")
    fig = px.bar(domain_scores, orientation='h', color=domain_scores, color_continuous_scale='Blues')
    st.plotly_chart(fig)

    st.subheader("📌 Most Common Top Skill Gaps")
    gap_counts = df["TopSkillGap"].value_counts().head(10)
    st.bar_chart(gap_counts)

# Tab 3: Match Score
with tabs[2]:
    st.header("📊 Match Score Breakdown")
    skills_present = len(resume_data["SkillsListed"].split(", "))
    skills_required = len(resume_data["JobPostingSkillsRequired"].split(", "))

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=[skills_present, skills_required, ai_score / 10],
        theta=['Skills Listed', 'Skills Required', 'AI Match Score'],
        fill='toself',
        name='Resume Match'
    ))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True)), showlegend=False)
    st.plotly_chart(fig)

# Tab 4: Suggestions
with tabs[3]:
    st.header("💡 Suggestions from Your Career Sister")
    gap = resume_data['TopSkillGap']
    if gap != 'None':
        st.warning(f"📌 You’re missing: **{gap}**. Try Coursera, LinkedIn Learning, or YouTube tutorials.")
    else:
        st.success("🌟 No major skill gaps! Keep up the great work.")

    style = resume_data["ResumeStyle"]
    if style == "Minimalist":
        st.info("✅ Your resume is clean. Consider adding personal branding elements.")
    elif style == "Infographic":
        st.warning("⚠️ Infographics can be ATS-unfriendly. Save it for creative roles.")

# Tab 5: Download Report
with tabs[4]:
    st.header("📥 Download Report")
    result_text = f"""
Resume ID: {resume_data['ResumeID']}
Match Score: {ai_score}/100
Skill Gap: {gap}
Style: {style}
Suggested Improvement: Learn {gap} and improve formatting for ATS if needed.
"""
   st.download_button(
    label="Download TXT Report",
    data=result_text,
    file_name="resume_vs_reality_report.txt",
    mime="text/plain"
)


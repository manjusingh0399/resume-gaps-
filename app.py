# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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
<h3>Your sassy, smart career wingwoman. 💅‍♂️</h3>
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
3. **📈 Match Score** – Visual breakdown of how close you are to ideal profiles.
4. **💡 Suggestions** – Helpful, no-BS advice to close skill and keyword gaps.
5. **🗕️ Download Report** – Save your growth map as a TXT report.
""")

with st.expander("🏡 What You'll Walk Away With"):
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
tabs = st.tabs(["Profile Snapshot", "Market Comparison", "Match Score", "Suggestions", "Trends & Insights", "Download Report"])

# Reuse same resume logic
def get_resume_data():
    resume_ids = df['ResumeID'].unique()
    selected_id = st.selectbox("Select a Resume ID", resume_ids, key="resume_selector")
    resume_data = df[df['ResumeID'] == selected_id].iloc[0]
    return resume_data

# Tab 1
with tabs[0]:
    st.header("Profile Snapshot")
    resume_data = get_resume_data()
    st.subheader("Resume Summary")
    st.write(f"**Age:** {resume_data['Age']}")
    st.write(f"**Education:** {resume_data['EducationLevel']} in {resume_data['FieldOfStudy']}")
    st.write(f"**Applied For:** {resume_data['JobAppliedFor']}")
    st.write(f"**Resume Style:** {resume_data['ResumeStyle']}")
    st.write(f"**Certifications:** {resume_data['Certifications']}")
    st.metric("AI Match Score", f"{resume_data['AI_MatchScore']}/100")

# Tab 2
with tabs[1]:
    st.header("Market Comparison")
    st.plotly_chart(px.box(df, x="Domain", y="AI_MatchScore", color="Domain"))
    gap_counts = df['TopSkillGap'].value_counts().head(10)
    st.plotly_chart(px.bar(gap_counts, title="Top Skill Gaps"))

# Tab 3
with tabs[2]:
    st.header("Match Score")
    listed = set(resume_data["SkillsListed"].split(", "))
    required = set(resume_data["JobPostingSkillsRequired"].split(", "))
    overlap = listed & required
    missing = required - listed
    st.metric("Skill Match", f"{len(overlap)} / {len(required)}")
    st.plotly_chart(px.pie(values=[len(overlap), len(missing)], names=["Matched", "Missing"]))

# Tab 4
with tabs[3]:
    st.header("Suggestions")
    gap = resume_data['TopSkillGap']
    st.markdown("### Personalized Advice")
    st.markdown("""
- Learn **{}** on LinkedIn Learning or Coursera.
- Rewrite bullets with measurable impact.
- Add a profile summary that aligns with job goals.
- Try building a portfolio using Notion or GitHub Pages.
- Tailor your resume for each job description.
""".format(gap))

# Tab 5: Extra graphs
with tabs[4]:
    st.header("Trends & Insights")
    avg_score_by_edu = df.groupby("EducationLevel")["AI_MatchScore"].mean().sort_values()
    st.subheader("Average Match Score by Education Level")
    st.plotly_chart(px.bar(avg_score_by_edu, orientation='h'))

    field_score = df.groupby("FieldOfStudy")["AI_MatchScore"].mean().sort_values(ascending=False).head(10)
    st.subheader("Top Performing Fields")
    st.plotly_chart(px.bar(field_score, title="Fields with Strongest Resume Match"))

    cert_counts = df['Certifications'].dropna().str.split(', ').explode().value_counts().head(10)
    st.subheader("Popular Certifications")
    st.plotly_chart(px.bar(cert_counts, title="Top Certifications"))

# Tab 6
with tabs[5]:
    st.header("Download Report")
    text = f"Resume ID: {resume_data['ResumeID']}\nScore: {resume_data['AI_MatchScore']}\nGap: {resume_data['TopSkillGap']}\nAdvice: Improve your skill in {resume_data['TopSkillGap']} and update resume formatting."
    st.download_button("Download as TXT", data=text, file_name="resume_vs_reality.txt")

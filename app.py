# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page config
st.set_page_config(page_title="Job Snob", layout="wide")

# Therapeutic Aesthetic Theme - Pastel Yellow & Ombre UI
st.markdown("""
    <style>
        body {
            background-color: #fffdf6;
            color: #333333;
            font-family: 'DM Sans', sans-serif;
        }
        .stApp {
            background-color: #fffdf6;
        }
        .stTabs [role="tab"] {
            background-color: #ffedd5;
            border-radius: 12px;
            padding: 0.75rem 1.25rem;
            margin-right: 0.5rem;
            font-weight: bold;
            color: #4e342e;
            transition: all 0.3s ease-in-out;
        }
        .stTabs [aria-selected="true"] {
            background: linear-gradient(90deg, #ffe0b2, #ffcc80);
            color: black;
            box-shadow: 0px 0px 10px rgba(255, 183, 77, 0.8);
        }
        .stProgress > div > div > div > div {
            background-color: #fbc687 !important;
        }
        .glow {
            color: #ff9100;
            text-shadow: 0 0 10px #ffd54f, 0 0 20px #ffca28;
        }
        .glass-card {
            background: rgba(255, 255, 255, 0.45);
            border-radius: 20px;
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            padding: 2rem;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
            margin-bottom: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

# Welcome Header & Intro Section
st.markdown("""
<div class='glass-card'>
    <h1 style='text-align:center;' class='glow'>🎯 Job Snob</h1>
    <p style='text-align:center; font-size: 1.2rem;'><em>Where Resumes Meet Reality</em></p>
    <p style='text-align:center;'>Navigating today’s job market can feel overwhelming, especially when you're unsure whether your skills are actually what employers want.</p>
    <p style='text-align:center;'>That’s where <strong>Job Snob</strong> steps in — a smart, stylish career companion built to decode the truth behind what gets you hired.</p>
    <p style='text-align:center;'>With real-time insights, role-matching analytics, and resume diagnostics, this app helps you bridge the gap between what you have and what you need.</p>
    <p style='text-align:center;'>Whether you're reworking your resume, exploring trending roles, or discovering hidden strengths, Job Snob empowers you to confidently take control of your career story — with clarity, elegance, and just the right amount of attitude. 💁‍♀️</p>
</div>
""", unsafe_allow_html=True)

# Instructions
with st.expander("📘 How to Use Job Snob"):
    st.markdown("""
    - Select a resume ID to view detailed breakdowns.
    - Navigate through each tab to explore how your resume compares to market standards.
    - Use the feedback and suggestions to improve your profile and job readiness.
    """)

# Why This App (User's Insight)
st.markdown("""
> "I created this app because I’ve been where you are — tweaking resumes at midnight, unsure if any of it even matters. **Job Snob** is my way of turning confusion into clarity, helping others feel empowered and informed instead of judged or lost."
""")

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv("genz_resume_market_data.csv")

df = load_data()

# Tabs
tabs = st.tabs([
    "👤 Profile Snapshot", 
    "📈 Market Comparison", 
    "📈 Match Score", 
    "💡 Suggestions", 
    "📚 Trends & Insights", 
    "📅 Download Report"])

# Resume selection logic
def get_resume_data():
    resume_ids = df['ResumeID'].unique()
    selected_id = st.selectbox("Select a Resume ID", resume_ids, key="resume_selector")
    resume_data = df[df['ResumeID'] == selected_id].iloc[0]
    return resume_data

# Tab 1: Profile Snapshot
with tabs[0]:
    st.header("👤 Profile Snapshot")
    st.caption("Your personalized profile card. Get a quick sense of who you are on paper.")
    resume_data = get_resume_data()
    st.subheader("Resume Summary")
    st.write(f"**Age:** {resume_data['Age']}")
    st.write(f"**Education:** {resume_data['EducationLevel']} in {resume_data['FieldOfStudy']}")
    st.write(f"**Applied For:** {resume_data['JobAppliedFor']}")
    st.write(f"**Resume Style:** {resume_data['ResumeStyle']}")
    st.write(f"**Certifications:** {resume_data['Certifications']}")
    st.metric("AI Match Score", f"{resume_data['AI_MatchScore']}/100")
    st.progress(resume_data['AI_MatchScore'] / 100)
    st.markdown("✅ *This score reflects how well your resume aligns with AI-based applicant screening systems.*")
    st.markdown("💡 *Think of this as your first impression checkpoint. If it's low, it's your cue to fine-tune.*")

# Tab 2: Market Comparison
with tabs[1]:
    st.header("📈 Market Comparison")
    st.caption("How do you stack up against others in your field?")

    st.subheader("AI Match Score by Domain")
    st.plotly_chart(px.box(df, x="Domain", y="AI_MatchScore", color="Domain"))
    st.caption("🎯 This shows how competitive different domains are. Higher scores in fields like Data and Marketing reflect greater skill alignment.")

    gap_counts = df['TopSkillGap'].value_counts().head(10)
    st.subheader("Top Skill Gaps Across Resumes")
    st.plotly_chart(px.bar(gap_counts, title="Top Skill Gaps"))
    st.caption("📉 These are the most lacking skills across resumes submitted. Use this insight to prioritize what to learn next.")
    st.markdown("✅ *These insights help you align better with hiring expectations in your domain.*")

# Tab 3: Match Score
with tabs[2]:
    st.header("📈 Match Score")
    st.caption("We break down your resume's skill overlap with the job posting.")
    listed = set(resume_data["SkillsListed"].split(", "))
    required = set(resume_data["JobPostingSkillsRequired"].split(", "))
    overlap = listed & required
    missing = required - listed
    st.metric("Skill Match", f"{len(overlap)} / {len(required)}")
    st.plotly_chart(px.pie(values=[len(overlap), len(missing)], names=["Matched", "Missing"]))
    st.caption("🍰 This pie chart reveals how many job-required skills are reflected in your resume.")
    st.markdown("✅ *Fewer missing skills = higher likelihood of getting shortlisted.*")
    st.markdown("💡 *Use this space to plan how to strategically improve your profile.*")

# Tab 4: Suggestions
with tabs[3]:
    st.header("💡 Suggestions")
    st.caption("Smart advice that makes a difference.")
    gap = resume_data['TopSkillGap']
    st.markdown(f"""
**Your Top Missing Skill:** `{gap}`

Try this:
- 📚 Learn **{gap}** through Coursera, YouTube, or LinkedIn Learning.
- ✍️ Update your resume bullets using STAR (Situation, Task, Action, Result).
- 🔍 Add keywords like "{gap}" in your summary or experience section.
- 🧪 Add a portfolio or project link that showcases that skill.
""")
    st.markdown("✅ *Even a single improvement here can push you ahead of 70% of applicants.*")
    st.markdown("💡 *This tab is your low-hanging fruit. Start here for fast impact.*")

# Tab 5: Trends & Insights
with tabs[4]:
    st.header("📚 Trends & Insights")
    st.caption("What’s hot in the hiring world?")

    avg_score_by_edu = df.groupby("EducationLevel")["AI_MatchScore"].mean().sort_values()
    st.subheader("Average Match Score by Education Level")
    st.plotly_chart(px.bar(avg_score_by_edu, orientation='h'))
    st.caption("🎓 How different educational levels perform under resume scanning systems.")

    field_score = df.groupby("FieldOfStudy")["AI_MatchScore"].mean().sort_values(ascending=False).head(10)
    st.subheader("Top Performing Fields")
    st.plotly_chart(px.bar(field_score, title="Fields with Strongest Resume Match"))
    st.caption("📘 These fields have high resume-job alignment. Consider pivoting or upskilling accordingly.")

    cert_counts = df['Certifications'].dropna().str.split(', ').explode().value_counts().head(10)
    st.subheader("Popular Certifications")
    st.plotly_chart(px.bar(cert_counts, title="Top Certifications"))
    st.caption("🎖️ Certifications most recognized and rewarded by employers today.")
    st.markdown("✅ *Trends help you plan your next steps with clarity and data.*")
    st.markdown("💡 *Explore this tab for long-term upskilling and strategy.*")

# Tab 6: Download Report
with tabs[5]:
    st.header("📅 Download Report")
    st.caption("Save your progress and recommendations for future reference.")
    text = f"Resume ID: {resume_data['ResumeID']}\nScore: {resume_data['AI_MatchScore']}\nGap: {resume_data['TopSkillGap']}\nAdvice: Improve your skill in {resume_data['TopSkillGap']} and update resume formatting."
    st.download_button("Download as TXT", data=text, file_name="resume_vs_reality.txt")
    st.markdown("✅ *A mini career blueprint to keep on hand.*")
    st.markdown("💡 *Keep iterating — success is in the follow-through.*")

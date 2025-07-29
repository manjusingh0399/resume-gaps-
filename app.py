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

st.markdown("""
    <div style="
        background: rgba(255, 255, 255, 0.25);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 15px;
        padding: 2rem 2.5rem;
        margin-top: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.18);
        color: #1e1e1e;
        font-family: 'DM Sans', sans-serif;
        font-size: 1.15rem;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.08);
    ">
        <h1 style="color:#6A0DAD; font-size: 2.2rem; margin-bottom: 0.5rem;">✨ Welcome to <em>Resume vs Reality</em></h1>

        <p><strong>We all build resumes hoping they reflect our potential.</strong> But behind every hiring decision lies a pattern. This project is a search for those patterns — an exploration of the gap between what we write and what employers value.</p>

        <p>I'm <strong>Manju Singh</strong>, an MBA student and a job seeker like you. I’ve been through the anxious nights of tweaking resumes, unsure if my skills are enough. This app is my way of turning that uncertainty into clarity — a light in the dark for all of us navigating today’s job market.</p>

        <p>With real data, interactive visuals, and a touch of empathy, <em>Resume vs Reality</em> is your personal career mentor. It doesn’t just show you the gap — it helps you bridge it. Let’s turn guesswork into guidance, and doubt into direction. 🌱</p>
    </div>
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
- 📊 **Visual data & coaching**: Get instant charts, skill scores, and action items.
- 🧱 **Built for Gen Z**: Think: aesthetics + analytics + honest feedback.
""")

with st.expander("🛠️ How to Use This App"):
    st.markdown("""
1. **👤 Profile Snapshot** – Upload or select a sample resume. Get the overview.
2. **📈 Market Comparison** – How does your resume stand in your chosen field?
3. **📈 Match Score** – Visual breakdown of how close you are to ideal profiles.
4. **💡 Suggestions** – Helpful, no-BS advice to close skill and keyword gaps.
5. **📅 Download Report** – Save your growth map as a TXT report.
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
tabs = st.tabs([
    "👤 Profile Snapshot", 
    "📈 Market Comparison", 
    "📈 Match Score", 
    "💡 Suggestions", 
    "📚 Trends & Insights", 
    "📅 Download Report"])

# Reuse same resume logic
def get_resume_data():
    resume_ids = df['ResumeID'].unique()
    selected_id = st.selectbox("Select a Resume ID", resume_ids, key="resume_selector")
    resume_data = df[df['ResumeID'] == selected_id].iloc[0]
    return resume_data

# Tab 1
with tabs[0]:
    st.header("👤 Profile Snapshot")
    st.caption("\nThis section shows a detailed view of the resume you selected. It helps you assess the basic profile details, resume style, and overall score before diving deeper.")
    resume_data = get_resume_data()
    st.subheader("Resume Summary")
    st.write(f"**Age:** {resume_data['Age']}")
    st.write(f"**Education:** {resume_data['EducationLevel']} in {resume_data['FieldOfStudy']}")
    st.write(f"**Applied For:** {resume_data['JobAppliedFor']}")
    st.write(f"**Resume Style:** {resume_data['ResumeStyle']}")
    st.write(f"**Certifications:** {resume_data['Certifications']}")
    st.metric("AI Match Score", f"{resume_data['AI_MatchScore']}/100")
    st.markdown("---")
    st.markdown("✅ *This gives a bird's eye view of your resume profile. Your score indicates how likely your resume is to get shortlisted in the AI-filtered hiring process.*")

# Tab 2
with tabs[1]:
    st.header("📈 Market Comparison")
    st.caption("\nCompare your score and skills with what the market expects in your field.")
    st.subheader("AI Match Score by Domain")
    st.plotly_chart(px.box(df, x="Domain", y="AI_MatchScore", color="Domain"))
    st.caption("\n🔍 This graph helps you compare how resumes perform across industries. Domains like Data and Marketing tend to have higher match scores.")

    gap_counts = df['TopSkillGap'].value_counts().head(10)
    st.subheader("Top Skill Gaps Across Resumes")
    st.plotly_chart(px.bar(gap_counts, title="Top Skill Gaps"))
    st.caption("\n📉 These are the most common skills missing across applicants. If yours appears here, you're not alone — but it's fixable!")

    st.markdown("---")
    st.markdown("✅ *This tab helps you understand how competitive your resume is within your target domain. Take note of the common gaps to address them proactively.*")

# Tab 3
with tabs[2]:
    st.header("📈 Match Score")
    st.caption("\nFind out how well your skills align with what employers want.")
    listed = set(resume_data["SkillsListed"].split(", "))
    required = set(resume_data["JobPostingSkillsRequired"].split(", "))
    overlap = listed & required
    missing = required - listed
    st.metric("Skill Match", f"{len(overlap)} / {len(required)}")
    st.plotly_chart(px.pie(values=[len(overlap), len(missing)], names=["Matched", "Missing"]))
    st.caption("\n📊 This pie chart shows how many skills you already have vs what's expected for the job. Fill the gap, boost your chances!")
    st.markdown("---")
    st.markdown("✅ *The more overlap you achieve here, the higher your job-fit and recruiter match potential becomes.*")

# Tab 4
with tabs[3]:
    st.header("💡 Suggestions")
    st.caption("\nHere’s your career coach moment. Let’s make things better.")
    gap = resume_data['TopSkillGap']
    st.markdown("### Personalized Advice")
    st.markdown(f"""
- 🎯 Learn **{gap}** on LinkedIn Learning, Coursera, or YouTube.
- ✍️ Rewrite resume bullets using STAR format (Situation, Task, Action, Result).
- 💬 Add keywords like "{gap}" naturally in your profile summary.
- 💼 Use real project links in portfolio if applying for tech/marketing roles.
- 🎨 Avoid overly creative resume styles if applying to traditional fields like Finance/HR.
""")
    st.markdown("---")
    st.markdown("✅ *These are practical next steps you can take immediately. Don’t wait — recruiters won’t.*")

# Tab 5: Extra graphs
with tabs[4]:
    st.header("📚 Trends & Insights")
    st.caption("\nDiscover macro trends in education, field, and certification performance.")
    avg_score_by_edu = df.groupby("EducationLevel")["AI_MatchScore"].mean().sort_values()
    st.subheader("Average Match Score by Education Level")
    st.plotly_chart(px.bar(avg_score_by_edu, orientation='h'))
    st.caption("🎓 See how your education compares in terms of AI-readiness.")

    field_score = df.groupby("FieldOfStudy")["AI_MatchScore"].mean().sort_values(ascending=False).head(10)
    st.subheader("Top Performing Fields")
    st.plotly_chart(px.bar(field_score, title="Fields with Strongest Resume Match"))
    st.caption("📘 These fields have the best resume-to-job alignment.")

    cert_counts = df['Certifications'].dropna().str.split(', ').explode().value_counts().head(10)
    st.subheader("Popular Certifications")
    st.plotly_chart(px.bar(cert_counts, title="Top Certifications"))
    st.caption("✅ Want to upgrade your resume fast? These are the top certifications recruiters recognize.")
    st.markdown("---")
    st.markdown("✅ *This data gives you an edge on how to align your background with real market performance.*")

# Tab 6
with tabs[5]:
    st.header("📅 Download Report")
    st.caption("\nSave your personalized advice and resume insight summary.")
    text = f"Resume ID: {resume_data['ResumeID']}\nScore: {resume_data['AI_MatchScore']}\nGap: {resume_data['TopSkillGap']}\nAdvice: Improve your skill in {resume_data['TopSkillGap']} and update resume formatting."
    st.download_button("Download as TXT", data=text, file_name="resume_vs_reality.txt")
    st.markdown("---")
    st.markdown("✅ *Take this report with you as a reminder of what to fix and where to grow.*")

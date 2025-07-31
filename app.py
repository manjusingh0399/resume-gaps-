import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(page_title="Job Snob", layout="wide")

# Sunset Gradient Themed CSS
st.markdown("""
<style>
    body {
        background: linear-gradient(120deg, #ffe082, #f48fb1, #ff8a65);
        background-attachment: fixed;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        background-color: rgba(255, 255, 255, 0.8);
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    h1, h2, h3 {
        color: #4e342e;
        font-family: 'DM Sans', sans-serif;
    }
    .sidebar .sidebar-content {
        background: rgba(255, 245, 235, 0.9);
        border-radius: 20px;
        padding: 1rem;
    }
    .welcome-container {
        background: linear-gradient(to right, #fffde7, #ffe0b2);
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 4px 8px rgba(0,0,0,0.08);
        margin-bottom: 2rem;
        text-align: center;
    }
    .quote-box {
        background-color: #fff8e1;
        padding: 1rem;
        border-left: 5px solid #ffd54f;
        border-radius: 8px;
        font-style: italic;
        margin-top: 1.5rem;
        font-size: 1.05rem;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3064/3064197.png", width=80)
st.sidebar.title("✨ Job Snob Navigation")
page = st.sidebar.radio("Go to:", [
    "👤 Profile Snapshot", 
    "📈 Market Comparison", 
    "📈 Match Score", 
    "💡 Suggestions", 
    "📚 Trends & Insights", 
    "📅 Download Report"
])

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("genz_resume_market_data.csv")

df = load_data()

# Welcome message
if page == "👤 Profile Snapshot":
    st.markdown("""
    <div class="welcome-container">
        <h1 style="color:#d84315;">💼 Welcome to <em>Job Snob</em></h1>
        <p><strong>Only the best skills make the cut. No basic resumes allowed.</strong></p>
        <p>Ever stared at your resume wondering, "Will this get me hired or ghosted?" You're not alone, and you're not going in blind anymore.</p>
        <p><strong>We all build resumes hoping they reflect our potential.</strong> But behind every hiring decision lies a pattern.</p>
        <p>I’m <strong>Manju Singh</strong>, an MBA student and job seeker. This app is your personal clarity engine — using real data and empathy to guide your career growth.</p>
        <p><em>Resume vs Reality</em> shows you the gap, and then helps you bridge it. Let’s turn guesswork into guidance. 🌱</p>
        <ul style="text-align:left; max-width:800px; margin:auto;">
            <li>💥 <strong>Mirror meets mentor:</strong> Know what your resume says <em>and</em> what it’s missing.</li>
            <li>🎯 <strong>Target your goals:</strong> Understand what job listings actually prioritize.</li>
            <li>🧠 <strong>Get real feedback:</strong> Actionable advice based on real market data.</li>
            <li>🌈 <strong>Grow with guidance:</strong> Personalized suggestions to help you level up fast.</li>
        </ul>
        <div class="quote-box">
        “Resumes don’t just speak for you — they whisper to recruiters. Let’s make sure yours is saying the right things.”
        </div>
    </div>
    """, unsafe_allow_html=True)

# Shared resume data fetch
def get_resume_data():
    resume_ids = df['ResumeID'].unique()
    selected_id = st.selectbox("Select a Resume ID", resume_ids, key="resume_selector")
    resume_data = df[df['ResumeID'] == selected_id].iloc[0]
    return resume_data

resume_data = get_resume_data()

# Page Routing
if page == "👤 Profile Snapshot":
    st.header("👤 Profile Snapshot")
    st.subheader("Resume Summary")
    st.write(f"Age: {resume_data['Age']}")
    st.write(f"Education: {resume_data['EducationLevel']} in {resume_data['FieldOfStudy']}")
    st.write(f"Applied For: {resume_data['JobAppliedFor']}")
    st.write(f"Resume Style: {resume_data['ResumeStyle']}")
    st.write(f"Certifications: {resume_data['Certifications']}")
    st.metric("AI Match Score", f"{resume_data['AI_MatchScore']}/100")

elif page == "📈 Market Comparison":
    st.header("📈 Market Comparison")
    st.subheader("AI Match Score by Domain")
    st.plotly_chart(px.box(df, x="Domain", y="AI_MatchScore", color="Domain"))
    gap_counts = df['TopSkillGap'].value_counts().head(10)
    st.subheader("Top Skill Gaps Across Resumes")
    st.plotly_chart(px.bar(gap_counts, title="Top Skill Gaps"))

elif page == "📈 Match Score":
    st.header("📈 Match Score")
    listed = set(resume_data["SkillsListed"].split(", "))
    required = set(resume_data["JobPostingSkillsRequired"].split(", "))
    overlap = listed & required
    missing = required - listed
    st.metric("Skill Match", f"{len(overlap)} / {len(required)}")
    st.plotly_chart(px.pie(values=[len(overlap), len(missing)], names=["Matched", "Missing"]))

elif page == "💡 Suggestions":
    st.header("💡 Suggestions")
    gap = resume_data['TopSkillGap']
    st.markdown(f"""
- 🎯 Learn **{gap}** on Coursera or YouTube.
- ✍ Rewrite your resume bullets using **STAR** format.
- 💬 Add keywords like **{gap}** to your summary.
- 💼 Include project links or GitHub if relevant.
""")

elif page == "📚 Trends & Insights":
    st.header("📚 Trends & Insights")
    avg_score_by_edu = df.groupby("EducationLevel")["AI_MatchScore"].mean().sort_values()
    st.subheader("Avg Match Score by Education Level")
    st.plotly_chart(px.bar(avg_score_by_edu, orientation='h'))

    field_score = df.groupby("FieldOfStudy")["AI_MatchScore"].mean().sort_values(ascending=False).head(10)
    st.subheader("Top Performing Fields")
    st.plotly_chart(px.bar(field_score))

    cert_counts = df['Certifications'].dropna().str.split(', ').explode().value_counts().head(10)
    st.subheader("Popular Certifications")
    st.plotly_chart(px.bar(cert_counts))

elif page == "📅 Download Report":
    st.header("📅 Download Report")
    text = f"Resume ID: {resume_data['ResumeID']}\nScore: {resume_data['AI_MatchScore']}\nGap: {resume_data['TopSkillGap']}\nAdvice: Improve your skill in {resume_data['TopSkillGap']} and update resume formatting."
    st.download_button("📄 Download TXT", data=text, file_name="resume_vs_reality.txt")


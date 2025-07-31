import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(page_title="Job Snob", layout="wide")

# Sunset Theme + Tab-style Buttons
st.markdown("""
<style>
body {
    background: linear-gradient(120deg, #ffe082, #f48fb1, #ff8a65);
    background-attachment: fixed;
}
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    background-color: rgba(255, 255, 255, 0.95);
    border-radius: 20px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}
h1, h2, h3 {
    color: #4e342e;
    font-family: 'DM Sans', sans-serif;
}
.stTabs [role="tab"] {
    background-color: #fff3e0;
    border-radius: 15px 15px 0 0;
    padding: 0.75rem 1.5rem;
    margin-right: 0.5rem;
    font-weight: bold;
    color: #6d4c41;
    border: 2px solid transparent;
    cursor: pointer;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(90deg, #ffe082, #f48fb1);
    color: white;
    border: 2px solid #ffb74d;
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
.instruction-box {
    background-color: #fffde7;
    border: 1px solid #ffe082;
    border-radius: 10px;
    padding: 1.5rem;
    margin-top: 2rem;
    font-size: 1.05rem;
    color: #4e342e;
}
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("genz_resume_market_data.csv")

df = load_data()

# Resume logic
def get_resume_data():
    resume_ids = df['ResumeID'].unique()
    selected_id = st.selectbox("Select a Resume ID", resume_ids)
    return df[df['ResumeID'] == selected_id].iloc[0]

resume_data = get_resume_data()

# Tabs
tabs = st.tabs([
    "🏡 Welcome", 
    "👤 Profile Snapshot", 
    "📈 Market Comparison", 
    "📈 Match Score", 
    "💡 Suggestions", 
    "📚 Trends & Insights", 
    "📅 Download Report"])

# Welcome Page
with tabs[0]:
    st.markdown("""
<div class="welcome-container">
    <h1 style="color:#d84315;"> Welcome to <em>Job Snob</em></h1>
    <p><strong>Only the best skills make the cut. No basic resumes allowed.</strong></p>
    <p>Ever stared at your resume wondering, \"Will this get me hired or ghosted?\" You're not alone, and you're not going in blind anymore.</p>
    <p><strong>We all build resumes hoping they reflect our potential.</strong> But behind every hiring decision lies a pattern.</p>
    <p>I’m <strong>Manju Singh</strong>, an MBA student and job seeker. This app is your personal clarity engine — using real data and empathy to guide your career growth.</p>
    <p><em>Resume vs Reality</em> shows you the gap, and then helps you bridge it. Let’s turn guesswork into guidance. 🌱</p>
    <ul style="text-align:left; max-width:800px; margin:auto;">
        <li> <strong>Mirror meets mentor:</strong> Know what your resume says <em>and</em> what it’s missing.</li>
        <li> <strong>Target your goals:</strong> Understand what job listings actually prioritize.</li>
        <li> <strong>Get real feedback:</strong> Actionable advice based on real market data.</li>
        <li> <strong>Grow with guidance:</strong> Personalized suggestions to help you level up fast.</li>
    </ul>
    <div class="quote-box">
    “Resumes don’t just speak for you — they whisper to recruiters. Let’s make sure yours is saying the right things.”
    </div>
</div>
<div class="instruction-box">
    <h3>🛠 How to Use This App:</h3>
    <ol>
        <li> <strong>Profile Snapshot</strong> — Select your resume ID and get an overview of your profile.</li>
        <li> <strong>Market Comparison</strong> — See how your resume stacks up in the market.</li>
        <li <strong>Match Score</strong> — Compare your skills with job requirements.</li>
        <li> <strong>Suggestions</strong> — Get tailored advice based on your resume’s gaps.</li>
        <li> <strong>Trends</strong> — Discover which education, skills, and certs work best.</li>
        <li> <strong>Download</strong> — Export a neat summary of your performance & advice.</li>
    </ol>
    <p>✨ Click on the tab headers at the top to explore each section. No more guessing — just growth.</p>
</div>
""", unsafe_allow_html=True)

# Page 1: Profile Snapshot
with tabs[1]:
    st.header("👤 Profile Snapshot")
    st.markdown("This is your resume's reflection. Think of it like a first impression on the recruiter.")
    st.subheader("Resume Summary")
    st.write(f"Age: {resume_data['Age']}")
    st.write(f"Education: {resume_data['EducationLevel']} in {resume_data['FieldOfStudy']}")
    st.write(f"Applied For: {resume_data['JobAppliedFor']}")
    st.write(f"Resume Style: {resume_data['ResumeStyle']}")
    st.write(f"Certifications: {resume_data['Certifications']}")
    st.metric("AI Match Score", f"{resume_data['AI_MatchScore']}/100")
    st.markdown("""<div class="quote-box">✅ Use this snapshot to assess how you're presenting yourself before diving into what the market wants.</div>""", unsafe_allow_html=True)

# Page 2: Market Comparison
with tabs[2]:
    st.header("📈 Market Comparison")
    st.markdown("Understanding the competition helps you stand out. Here's how you compare with the crowd.")
    st.subheader("AI Match Score by Domain")
    st.plotly_chart(px.box(df, x="Domain", y="AI_MatchScore", color="Domain"))
    gap_counts = df['TopSkillGap'].value_counts().head(10)
    st.subheader("Top Skill Gaps Across Resumes")
    st.plotly_chart(px.bar(gap_counts))
    st.markdown("""<div class="quote-box">✅ Know your playing field. Understanding where you stand lets you compete smarter — not harder.</div>""", unsafe_allow_html=True)

# Page 3: Match Score
with tabs[3]:
    st.header("📈 Match Score")
    st.markdown("How aligned are your skills with job requirements? Here's the breakdown.")
    listed = set(resume_data["SkillsListed"].split(", "))
    required = set(resume_data["JobPostingSkillsRequired"].split(", "))
    overlap = listed & required
    missing = required - listed
    st.metric("Skill Match", f"{len(overlap)} / {len(required)}")
    st.plotly_chart(px.pie(values=[len(overlap), len(missing)], names=["Matched", "Missing"]))
    st.markdown("""<div class="quote-box">✅ Every matched skill improves your odds. The missing ones? They’re just opportunities in disguise.</div>""", unsafe_allow_html=True)

# Page 4: Suggestions
with tabs[4]:
    st.header("💡 Suggestions")
    st.markdown("Based on your profile and detected gaps, here are some highly actionable tips.")
    gap = resume_data['TopSkillGap']
    st.markdown(f"""
    -  Learn **{gap}** through a project-based course.
    -  Rewrite your resume bullets using **STAR** format.
    -  Add keywords like **{gap}** to your summary.
    -  Include links to live projects or portfolios.
    -  Format your resume cleanly — recruiters scan in seconds.
    """)
    st.markdown("""<div class="quote-box">✅ Small actions compound into big results. Believe in progress, not perfection.</div>""", unsafe_allow_html=True)

# Page 5: Trends
with tabs[5]:
    st.header("📚 Trends & Insights")
    st.markdown("Zoom out to see what's working for others — then personalize it for yourself.")
    avg_score_by_edu = df.groupby("EducationLevel")["AI_MatchScore"].mean().sort_values()
    st.subheader("Avg Match Score by Education Level")
    st.plotly_chart(px.bar(avg_score_by_edu, orientation='h'))
    field_score = df.groupby("FieldOfStudy")["AI_MatchScore"].mean().sort_values(ascending=False).head(10)
    st.subheader("Top Performing Fields")
    st.plotly_chart(px.bar(field_score))
    cert_counts = df['Certifications'].dropna().str.split(', ').explode().value_counts().head(10)
    st.subheader("Popular Certifications")
    st.plotly_chart(px.bar(cert_counts))
    st.markdown("""<div class="quote-box">✅ Be aware of patterns, but build your own story. These trends are here to guide — not define — you.</div>""", unsafe_allow_html=True)

# Page 6: Download Report
with tabs[6]:
    st.header(" Download Report")
    st.markdown("Here’s your personalized career clarity digest. Save it and revisit as you grow.")
    text = f"""
    📄 Resume Summary Report

    Resume ID: {resume_data['ResumeID']}
    Name: {resume_data.get('Name', 'Anonymous')}
    Applied For: {resume_data['JobAppliedFor']}
    Education: {resume_data['EducationLevel']} in {resume_data['FieldOfStudy']}
    Certifications: {resume_data['Certifications']}
    Resume Style: {resume_data['ResumeStyle']}

    AI Match Score: {resume_data['AI_MatchScore']}/100
    Skill Match: {len(overlap)} / {len(required)}
    Top Skill Gap: {resume_data['TopSkillGap']}

    Suggestions:
    - Strengthen skill in {resume_data['TopSkillGap']}
    - Add missing skills to resume strategically
    - Use STAR method in your experience descriptions
    - Highlight real projects or portfolio links
    - Keep resume style clean and ATS-friendly

    Encouragement:
    You're closer than you think. Keep learning, keep iterating, and remember — every step you take brings you one closer to your dream role. 🚀
    """
    st.download_button("📄 Download Full Report", data=text, file_name="resume_vs_reality_detailed_report.txt")
    st.markdown("""<div class="quote-box">✅ Save your progress and use it as a roadmap. You’ve got this!</div>""", unsafe_allow_html=True)

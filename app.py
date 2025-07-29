# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page config
st.set_page_config(page_title="Job Snob", layout="wide")

# Therapeutic Aesthetic Theme - Soft Yellow & Pastel Ombre
st.markdown("""
    <style>
        body {
            background-color: #fffdf6;
            color: #333333;
            font-family: 'Georgia', serif;
        }
        .stApp {
            background-color: #fffdf6;
        }
        .css-1d391kg, .css-1q8dd3e {
            background-color: #ffffff;
            color: #333333;
        }
        .st-bw, .st-bv, .st-c2 {
            color: #333333;
        }
        .stProgress > div > div > div > div {
            background-color: #fbc687 !important;
        }
    </style>
""", unsafe_allow_html=True)

# Welcome Page
st.markdown("""
<div style='background: linear-gradient(to right, #fffde7, #ffe0b2); padding: 2rem; border-radius: 15px; box-shadow: 0 2px 12px rgba(0,0,0,0.04);'>
    <h1 style='text-align:center; color: #5d4037;'>🎯 Welcome to <em>Job Snob</em> — Where Resumes Meet Reality</h1>
    <p style='text-align:center; font-size: 1.15rem;'>Navigating today’s job market can feel overwhelming, especially when you're unsure whether your skills are actually what employers want.</p>
    <p style='text-align:center;'>That’s where <strong>Job Snob</strong> steps in — a smart, stylish career companion built to decode the truth behind what gets you hired.</p>
    <p style='text-align:center;'>With real-time insights, role-matching analytics, and resume diagnostics, this app helps you bridge the gap between what you have and what you need.</p>
    <p style='text-align:center;'>Whether you're reworking your resume, exploring trending roles, or discovering hidden strengths, Job Snob empowers you to confidently take control of your career story — with clarity, elegance, and just the right amount of attitude. 💁‍♀️</p>
</div>
""", unsafe_allow_html=True)

# Resume Upload (Future expansion)
uploaded_file = st.sidebar.file_uploader("📤 Upload Your Resume (PDF/DOCX)", type=["pdf", "docx"])
if uploaded_file:
    st.sidebar.success("Resume uploaded. Parsing will be added in next version.")

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

# Resume Selection Logic
def get_resume_data():
    resume_ids = df['ResumeID'].unique()
    selected_id = st.selectbox("Select a Resume ID", resume_ids, key="resume_selector")
    resume_data = df[df['ResumeID'] == selected_id].iloc[0]
    return resume_data

resume_data = get_resume_data()
tabs = st.tabs([
    "👤 Profile Snapshot", "📈 Market Comparison", "📊 Match Score",
    "💡 Suggestions", "📚 Trends & Insights", "📅 Download Report"])

with tabs[0]:
    st.header("👤 Profile Snapshot")
    st.markdown("""
    <p>This section captures a snapshot of your background, education, and application focus — setting the stage for your career reflection journey.</p>
    """, unsafe_allow_html=True)
    st.write(f"**Age:** {resume_data['Age']}")
    st.write(f"**Education:** {resume_data['EducationLevel']} in {resume_data['FieldOfStudy']}")
    st.write(f"**Applied For:** {resume_data['JobAppliedFor']}")
    st.write(f"**Resume Style:** {resume_data['ResumeStyle']}")
    st.write(f"**Certifications:** {resume_data['Certifications']}")
    st.metric("AI Match Score", f"{resume_data['AI_MatchScore']} / 100")
    st.progress(resume_data['AI_MatchScore'] / 100)
    st.markdown(f"""
    <div class='feedback-box'>
    Insight: Resume formatting and relevant certifications are subtle but crucial signals.<br>
    Advice: Highlight recent achievements and role-focused skills to improve first impressions.
    </div>
    <p><em>Keep this profile fresh and aligned with the job roles you aspire for.</em></p>
    """, unsafe_allow_html=True)

with tabs[1]:
    st.header("📈 Market Comparison")
    st.markdown("""
    <p>This section allows you to benchmark yourself against industry peers — a must for understanding how you stack up competitively.</p>
    """, unsafe_allow_html=True)
    st.plotly_chart(px.box(df, x="FieldOfStudy", y="AI_MatchScore", template="seaborn"), use_container_width=True)
    st.markdown(f"""
    <div class='feedback-box'>
    Insight: Fields with tech-focused education have better match scores on average.<br>
    Advice: Consider certifications in trending areas to stay competitive.
    </div>
    <p><em>Use these comparisons to make informed upskilling decisions.</em></p>
    """, unsafe_allow_html=True)

with tabs[2]:
    st.header("📊 Match Score")
    st.markdown("""
    <p>This section dissects your skill match and reveals gaps between your profile and what job listings demand.</p>
    """, unsafe_allow_html=True)
    listed = set(resume_data["SkillsListed"].split(", "))
    required = set(resume_data["JobPostingSkillsRequired"].split(", "))
    overlap = listed & required
    missing = required - listed
    st.metric("Skill Match", f"{len(overlap)} / {len(required)}")
    st.plotly_chart(px.pie(values=[len(overlap), len(missing)], names=["Matched", "Missing"], template="seaborn"), use_container_width=True)
    st.markdown(f"""
    <div class='feedback-box'>
    Insight: Skills like {', '.join(missing)} are commonly expected but missing.<br>
    Advice: Learning and showcasing these will boost your hiring score.
    </div>
    <p><em>Your match score improves with each resume revision and real skill gain.</em></p>
    """, unsafe_allow_html=True)

with tabs[3]:
    st.header("💡 Suggestions")
    st.markdown("""
    <p>Targeted advice tailored to your profile gaps — here’s how to get better, faster.</p>
    """, unsafe_allow_html=True)
    st.markdown(f"""
- 📘 Learn **{resume_data['TopSkillGap']}** through project-based courses.
- ✍️ Use STAR format to rewrite bullet points.
- 🧠 Reflect missing skills in summary & keywords.
- 🖼 Adapt your resume layout based on the job type.
- 🤝 Get peer reviews or use resume checkers.
    """)
    st.markdown("""
    <div class='feedback-box'>
    Feedback: Small resume tweaks + consistent learning = big leaps.
    </div>
    <p><em>Come back to this tab often — adapt as you grow.</em></p>
    """, unsafe_allow_html=True)

with tabs[4]:
    st.header("📚 Trends & Insights")
    st.markdown("""
    <p>Observe market trends, popular education paths, and in-demand certifications to stay ahead.</p>
    """, unsafe_allow_html=True)
    avg_edu = df.groupby("EducationLevel")["AI_MatchScore"].mean()
    st.bar_chart(avg_edu)
    st.markdown("""
    <div class='feedback-box'>
    Insight: Bachelor's and up with industry certifications outperform in data roles.
    </div>
    <p><em>Let industry trends guide your skill priorities.</em></p>
    """, unsafe_allow_html=True)

with tabs[5]:
    st.header("📅 Download Report")
    st.markdown("""
    <p>Download a customized summary of your profile, insights, and next steps.</p>
    """, unsafe_allow_html=True)
    report = f"""
Job Snob Report\n================\nResume ID: {resume_data['ResumeID']}\nJob Applied For: {resume_data['JobAppliedFor']}\nEducation: {resume_data['EducationLevel']} in {resume_data['FieldOfStudy']}\nMatch Score: {resume_data['AI_MatchScore']}\nMissing Skills: {', '.join(missing)}\nRecommendations: Focus on {resume_data['TopSkillGap']}\n"""
    st.download_button("📥 Download Report", data=report, file_name="job_snob_report.txt")
    st.markdown("""
    <div class='feedback-box'>
    Reminder: Use this report monthly to realign your growth.
    </div>
    <p><em>This report is your portable career blueprint.</em></p>
    """, unsafe_allow_html=True)

# Conclusion
st.markdown("""
<div class='feedback-box'>
🌟 <strong>Final Insight:</strong> Your career is a marathon, not a sprint. Keep evolving with purpose, stay updated, and let each small action lead you toward your dream role.
</div>

<div style='text-align:center; padding-top:2rem; font-size:0.9rem;'>
© 2025 Job Snob | Built with ❤️ using Streamlit
</div>
""", unsafe_allow_html=True)

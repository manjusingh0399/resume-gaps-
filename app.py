import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(page_title="Job Snob", layout="wide")

# Sunset Theme + Styled Sidebar Tabs
st.markdown("""
<style>
body {
    background: linear-gradient(120deg, #ffe082, #f48fb1, #ff8a65);
    background-attachment: fixed;
}
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    background-color: rgba(255, 255, 255, 0.9);
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
.sidebar-title {
    font-size: 1.4rem;
    font-weight: 600;
    margin-bottom: 1rem;
    background: linear-gradient(to right, #ffcc80, #f48fb1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
div[data-testid="stSidebar"] div[role="radiogroup"] > label {
    background: #fffaf0;
    padding: 0.75rem 1rem;
    margin: 0.25rem 0;
    border-radius: 15px;
    border: 1px solid #ffe0b2;
    transition: all 0.2s ease-in-out;
}
div[data-testid="stSidebar"] div[role="radiogroup"] > label:hover {
    background: #fff3e0;
    transform: translateX(2px);
    box-shadow: 0 0 6px rgba(255, 204, 128, 0.3);
}
div[data-testid="stSidebar"] div[role="radiogroup"] > label[data-selected="true"] {
    background: linear-gradient(to right, #ffe082, #f48fb1, #ff8a65);
    color: white !important;
    font-weight: bold;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    transform: scale(1.02);
}
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown('<div class="sidebar-title">✨ Job Snob</div>', unsafe_allow_html=True)
page = st.sidebar.radio("Choose a section:", [
    "👤 Profile Snapshot", 
    "📈 Market Comparison", 
    "📈 Match Score", 
    "💡 Suggestions", 
    "📚 Trends & Insights", 
    "📅 Download Report"])

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("genz_resume_market_data.csv")

df = load_data()

# Shared resume logic
def get_resume_data():
    resume_ids = df['ResumeID'].unique()
    selected_id = st.selectbox("Select a Resume ID", resume_ids)
    return df[df['ResumeID'] == selected_id].iloc[0]

resume_data = get_resume_data()

# Pages
if page == "👤 Profile Snapshot":
    st.header("👤 Profile Snapshot")
    st.markdown("""
    This section breaks down the essentials — your education, age, resume style, and how your skills reflect on paper.
    Think of it as your resume’s first impression.
    """)
    st.subheader("Resume Summary")
    st.write(f"Age: {resume_data['Age']}")
    st.write(f"Education: {resume_data['EducationLevel']} in {resume_data['FieldOfStudy']}")
    st.write(f"Applied For: {resume_data['JobAppliedFor']}")
    st.write(f"Resume Style: {resume_data['ResumeStyle']}")
    st.write(f"Certifications: {resume_data['Certifications']}")
    st.metric("AI Match Score", f"{resume_data['AI_MatchScore']}/100")
    st.markdown("""
    <div class="quote-box">
    ✅ Use this snapshot to assess how you're presenting yourself before diving into what the market wants.
    </div>
    """, unsafe_allow_html=True)

elif page == "📈 Market Comparison":
    st.header("📈 Market Comparison")
    st.markdown("""
    Compare your resume to others in the same domain. See where you stand and what's commonly missing.
    """)
    st.subheader("AI Match Score by Domain")
    st.plotly_chart(px.box(df, x="Domain", y="AI_MatchScore", color="Domain"))
    gap_counts = df['TopSkillGap'].value_counts().head(10)
    st.subheader("Top Skill Gaps Across Resumes")
    st.plotly_chart(px.bar(gap_counts))
    st.markdown("""
    <div class="quote-box">
    ✅ Know your playing field. Understanding where you stand lets you compete smarter — not harder.
    </div>
    """, unsafe_allow_html=True)

elif page == "📈 Match Score":
    st.header("📈 Match Score")
    st.markdown("""
    How aligned are your skills with job requirements? Here's the breakdown.
    """)
    listed = set(resume_data["SkillsListed"].split(", "))
    required = set(resume_data["JobPostingSkillsRequired"].split(", "))
    overlap = listed & required
    missing = required - listed
    st.metric("Skill Match", f"{len(overlap)} / {len(required)}")
    st.plotly_chart(px.pie(values=[len(overlap), len(missing)], names=["Matched", "Missing"]))
    st.markdown("""
    <div class="quote-box">
    ✅ Every matched skill improves your odds. The missing ones? They’re just opportunities in disguise.
    </div>
    """, unsafe_allow_html=True)

elif page == "💡 Suggestions":
    st.header("💡 Suggestions")
    st.markdown("""
    Based on your top gap, here are targeted, real-world tips to level up.
    """)
    gap = resume_data['TopSkillGap']
    st.markdown(f"""
    - 🎯 Learn **{gap}** on Coursera or YouTube.
    - ✍ Rewrite your resume bullets using **STAR** format.
    - 💬 Add keywords like **{gap}** to your summary.
    - 💼 Include project links or GitHub if relevant.
    - 🧹 Clean up formatting — clarity wins over creativity.
    """)
    st.markdown("""
    <div class="quote-box">
    ✅ Small steps, big results. Just start.
    </div>
    """, unsafe_allow_html=True)

elif page == "📚 Trends & Insights":
    st.header("📚 Trends & Insights")
    st.markdown("""
    Zooming out. See which degrees, fields, and certs actually perform.
    """)
    avg_score_by_edu = df.groupby("EducationLevel")["AI_MatchScore"].mean().sort_values()
    st.subheader("Avg Match Score by Education Level")
    st.plotly_chart(px.bar(avg_score_by_edu, orientation='h'))

    field_score = df.groupby("FieldOfStudy")["AI_MatchScore"].mean().sort_values(ascending=False).head(10)
    st.subheader("Top Performing Fields")
    st.plotly_chart(px.bar(field_score))

    cert_counts = df['Certifications'].dropna().str.split(', ').explode().value_counts().head(10)
    st.subheader("Popular Certifications")
    st.plotly_chart(px.bar(cert_counts))
    st.markdown("""
    <div class="quote-box">
    ✅ Learn from the best — then make it your own.
    </div>
    """, unsafe_allow_html=True)

elif page == "📅 Download Report":
    st.header("📅 Download Report")
    st.markdown("""
    Wrap it up and take it with you. Here's your personal growth report.
    """)
    text = f"Resume ID: {resume_data['ResumeID']}\nScore: {resume_data['AI_MatchScore']}\nGap: {resume_data['TopSkillGap']}\nAdvice: Improve your skill in {resume_data['TopSkillGap']} and update resume formatting."
    st.download_button("📄 Download TXT", data=text, file_name="resume_vs_reality.txt")
    st.markdown("""
    <div class="quote-box">
    ✅ Save it. Share it. Reflect on it. See you on the shortlist soon.
    </div>
    """, unsafe_allow_html=True)

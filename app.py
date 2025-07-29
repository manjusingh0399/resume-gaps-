# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page config
st.set_page_config(page_title="Resume vs Reality", layout="wide")

# Resume Upload (Future expansion)
uploaded_file = st.sidebar.file_uploader("\U0001F4E4 Upload Your Resume (PDF/DOCX)", type=["pdf", "docx"])
if uploaded_file:
    st.sidebar.success("Resume uploaded. Parsing will be added in next version.")

# Custom CSS styles
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
        font-family: 'DM Sans', sans-serif;
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

# Welcome Message
with st.container():
    st.markdown("""
        <div class="welcome-container">
            <h1 style="color:#6A0DAD; font-size: 2.2rem; margin-bottom: 0.5rem;">\U0001F4BC Welcome to <em>Resume vs Reality</em></h1>
            <p><strong>Your sassy, smart career wingwoman. \U0001F91D‍♂️</strong></p>
            <p>Ever stared at your resume wondering, \"Will this get me hired or ghosted?\" You're not alone — and you're not going in blind anymore.</p>
            <p><strong>We all build resumes hoping they reflect our potential.</strong> But behind every hiring decision lies a pattern. This project is a search for those patterns — an exploration of the gap between what we write and what employers value.</p>
            <p>I'm <strong>Manju Singh</strong>, an MBA student and a job seeker like you. I’ve been through the anxious nights of tweaking resumes, unsure if my skills are enough. This app is my way of turning that uncertainty into clarity — a light in the dark for all of us navigating today’s job market.</p>
            <p>With real data, interactive visuals, and a touch of empathy, <em>Resume vs Reality</em> is your personal career mentor. It doesn’t just show you the gap — it helps you bridge it. Let’s turn guesswork into guidance, and doubt into direction. 🌱</p>
            <p><strong>Here’s what you’ll discover:</strong></p>
            <ul style="text-align: left; max-width: 800px; margin: auto;">
                <li>💥 <strong>Mirror meets mentor:</strong> Know what your resume says <em>and</em> what it’s missing.</li>
                <li>🎯 <strong>Target your goals:</strong> Understand what job listings actually prioritize.</li>
                <li>🧠 <strong>Get real feedback:</strong> Actionable advice based on <em>real</em> market data.</li>
                <li>🌈 <strong>Grow with guidance:</strong> Personalized suggestions to help you level up fast.</li>
            </ul>
            <div class="quote-box">
                “Resumes don’t just speak for you — they whisper to recruiters. Let’s make sure yours is saying the right things.”
            </div>
        </div>
    """, unsafe_allow_html=True)

@st.cache_data

def load_data():
    return pd.read_csv("genz_resume_market_data.csv")

df = load_data()

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

# Tabs
tabs = st.tabs([
    "👤 Profile Snapshot", 
    "📈 Market Comparison", 
    "🎯 Match Score", 
    "💡 Suggestions", 
    "📚 Trends & Insights", 
    "🗕️ Download Report"])

def get_resume_data():
    resume_ids = df['ResumeID'].unique()
    selected_id = st.selectbox("Select a Resume ID", resume_ids, key="resume_selector")
    resume_data = df[df['ResumeID'] == selected_id].iloc[0]
    return resume_data

# Tab 1
with tabs[0]:
    st.header("👤 Profile Snapshot")
    st.caption("This section shows a detailed view of the resume you selected.")
    resume_data = get_resume_data()
    st.subheader("Resume Summary")
    st.write(f"**Age:** {resume_data['Age']}")
    st.write(f"**Education:** {resume_data['EducationLevel']} in {resume_data['FieldOfStudy']}")
    st.write(f"**Applied For:** {resume_data['JobAppliedFor']}")
    st.write(f"**Resume Style:** {resume_data['ResumeStyle']}")
    st.write(f"**Certifications:** {resume_data['Certifications']}")
    st.metric("AI Match Score", f"{resume_data['AI_MatchScore']}/100")
    st.progress(resume_data['AI_MatchScore'] / 100)

    role_mapping = {
        'Data Science': ['Data Analyst', 'ML Engineer'],
        'Computer Science': ['Software Developer', 'Backend Engineer'],
        'Marketing': ['Digital Marketer', 'SEO Analyst'],
        'Finance': ['Financial Analyst', 'Investment Banker'],
        'Business': ['Business Analyst', 'Ops Manager'],
        'Economics': ['Policy Analyst', 'Risk Analyst']
    }
    field = resume_data['FieldOfStudy']
    st.subheader("\U0001F3AF Suggested Roles")
    st.success(", ".join(role_mapping.get(field, ['General Analyst', 'Trainee Associate'])))

# Tab 2
with tabs[1]:
    st.header("📈 Market Comparison")
    st.subheader("AI Match Score by Domain")
    st.plotly_chart(px.box(df, x="Domain", y="AI_MatchScore", color="Domain"))
    st.subheader("Top Skill Gaps Across Resumes")
    gap_counts = df['TopSkillGap'].value_counts().head(10)
    st.plotly_chart(px.bar(gap_counts, title="Top Skill Gaps"))

# Tab 3
with tabs[2]:
    st.header("\U0001F3AF Match Score")
    listed = set(resume_data["SkillsListed"].split(", "))
    required = set(resume_data["JobPostingSkillsRequired"].split(", "))
    overlap = listed & required
    missing = required - listed
    st.metric("Skill Match", f"{len(overlap)} / {len(required)}")
    st.plotly_chart(px.pie(values=[len(overlap), len(missing)], names=["Matched", "Missing"]))

# Tab 4
with tabs[3]:
    st.header("\U0001F4A1 Suggestions")
    gap = resume_data['TopSkillGap']
    st.markdown(f"""
- Learn **{gap}** online (LinkedIn, Coursera).
- Use STAR format in your resume.
- Mention **{gap}** in summary or bullets.
- Add project links or portfolios.
- Avoid overly creative designs for traditional roles.
""")

# Tab 5
with tabs[4]:
    st.header("\U0001F4DA Trends & Insights")
    avg_score_by_edu = df.groupby("EducationLevel")["AI_MatchScore"].mean().sort_values()
    st.subheader("Avg Score by Education")
    st.plotly_chart(px.bar(avg_score_by_edu, orientation='h'))
    field_score = df.groupby("FieldOfStudy")["AI_MatchScore"].mean().sort_values(ascending=False).head(10)
    st.subheader("Top Performing Fields")
    st.plotly_chart(px.bar(field_score))
    cert_counts = df['Certifications'].dropna().str.split(', ').explode().value_counts().head(10)
    st.subheader("Top Certifications")
    st.plotly_chart(px.bar(cert_counts))

# Tab 6
with tabs[5]:
    st.header("\U0001F5D5\ufe0f Download Report")
    text = f"Resume ID: {resume_data['ResumeID']}\nScore: {resume_data['AI_MatchScore']}\nGap: {resume_data['TopSkillGap']}\nAdvice: Improve your skill in {resume_data['TopSkillGap']} and update resume formatting."
    st.download_button("Download as TXT", data=text, file_name="resume_vs_reality.txt")

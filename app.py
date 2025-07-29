import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(page_title="The Resume Reflection Room", layout="wide")

# Soft Pastel Theme
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
        .stProgress > div > div > div > div {
            background-color: #fbc687 !important;
        }
    </style>
""", unsafe_allow_html=True)

# Welcome Message
with st.container():
    st.markdown("""
        <div class="welcome-container">
            <h1 style="color:#6A0DAD; font-size: 2.2rem;">💼 Welcome to <em>Resume vs Reality</em></h1>
            <p><strong>Your sassy, smart career wingwoman. 💅‍♂</strong></p>
            <p>Ever stared at your resume wondering, "Will this get me hired or ghosted?" You're not alone — and you're not going in blind anymore.</p>
            <p><strong>We all build resumes hoping they reflect our potential.</strong> But behind every hiring decision lies a pattern. This project is a search for those patterns — an exploration of the gap between what we write and what employers value.</p>
            <p>I'm <strong>Manju Singh</strong>, an MBA student and a job seeker like you. I’ve been through the anxious nights of tweaking resumes, unsure if my skills are enough. This app is my way of turning that uncertainty into clarity — a light in the dark for all of us navigating today’s job market.</p>
            <p>With real data, interactive visuals, and a touch of empathy, <em>Resume vs Reality</em> is your personal career mentor.</p>
            <ul>
                <li>💥 <strong>Mirror meets mentor:</strong> Know what your resume says <em>and</em> what it’s missing.</li>
                <li>🎯 <strong>Target your goals:</strong> Understand what job listings actually prioritize.</li>
                <li>🧠 <strong>Get real feedback:</strong> Actionable advice based on <em>real</em> market data.</li>
                <li>🌈 <strong>Grow with guidance:</strong> Personalized suggestions to help you level up fast.</li>
            </ul>
            <blockquote>“Resumes don’t just speak for you — they whisper to recruiters. Let’s make sure yours is saying the right things.”</blockquote>
        </div>
    """, unsafe_allow_html=True)

# Data loader
@st.cache_data(persist=True)
def load_data():
    return pd.read_csv("genz_resume_market_data.csv")

df = load_data()

# Expanders for guidance
with st.expander("🛠 How to Use This App"):
    st.markdown("""
1. *👤 Profile Snapshot* – Select a sample resume.
2. *📈 Market Comparison* – See how your resume stacks up.
3. *📈 Match Score* – Measure your fit against job listings.
4. *💡 Suggestions* – Close skill/keyword gaps smartly.
5. *📅 Download Report* – Take home your career roadmap.
""")

with st.expander("🏡 What You'll Walk Away With"):
    st.markdown("""
- 🔎 *Clarity* on your resume’s strengths and weaknesses.
- 🧠 *Insight* into hiring trends and domain gaps.
- 📌 *Skill maps* tailored to your field.
- 💪 *Confidence* from data-backed suggestions.
""")

st.markdown("""
<blockquote>“Resumes don’t just speak for you — they whisper to recruiters. Let’s make sure yours is saying the right things.”</blockquote>
🚀 *Ready? Let’s build a resume that doesn’t just talk — it lands you offers.*
""", unsafe_allow_html=True)

# Tabs
tabs = st.tabs([
    "👤 Profile Snapshot", 
    "📈 Market Comparison", 
    "📈 Match Score", 
    "💡 Suggestions", 
    "📚 Trends & Insights", 
    "📅 Download Report"
])

# Resume Selector
def get_resume_data():
    resume_ids = df['ResumeID'].unique()
    selected_id = st.selectbox("Select a Resume ID", resume_ids, key="resume_selector")
    resume_data = df[df['ResumeID'] == selected_id].iloc[0]
    return resume_data

# Tab 1 - Profile Snapshot
with tabs[0]:
    st.header("👤 Profile Snapshot")
    resume_data = get_resume_data()
    st.subheader("Resume Summary")
    st.write(f"**Age:** {resume_data['Age']}")
    st.write(f"**Education:** {resume_data['EducationLevel']} in {resume_data['FieldOfStudy']}")
    st.write(f"**Applied For:** {resume_data['JobAppliedFor']}")
    st.write(f"**Resume Style:** {resume_data['ResumeStyle']}")
    st.write(f"**Certifications:** {resume_data['Certifications'] if pd.notna(resume_data['Certifications']) else 'None'}")
    st.metric("AI Match Score", f"{resume_data['AI_MatchScore']}/100")
    st.progress(resume_data["AI_MatchScore"] / 100)

    role_mapping = {
        'Data Science': ['Data Analyst', 'ML Engineer'],
        'Marketing': ['Brand Associate', 'Content Strategist'],
        'Finance': ['Credit Analyst', 'Business Analyst']
    }
    field = resume_data['FieldOfStudy']
    suggested_roles = ', '.join(role_mapping.get(field, ['General Analyst', 'Executive Trainee']))
    st.markdown(f"👀 Suggested Roles: {suggested_roles}")
    st.markdown("---")

# Tab 2 - Market Comparison
with tabs[1]:
    st.header("📈 Market Comparison")
    st.subheader("AI Match Score by Domain")
    st.plotly_chart(px.box(df, x="Domain", y="AI_MatchScore", color="Domain"))

    gap_counts = df['TopSkillGap'].value_counts().head(10)
    st.subheader("Top Skill Gaps Across Resumes")
    st.plotly_chart(px.bar(gap_counts, title="Top Skill Gaps"))

# Tab 3 - Match Score
with tabs[2]:
    st.header("📈 Match Score")
    listed = set(resume_data.get("SkillsListed", "").split(", "))
    required = set(resume_data.get("JobPostingSkillsRequired", "").split(", "))
    overlap = listed & required
    missing = required - listed
    st.metric("Skill Match", f"{len(overlap)} / {len(required)}")
    st.plotly_chart(px.pie(values=[len(overlap), len(missing)], names=["Matched", "Missing"]))

# Tab 4 - Suggestions
with tabs[3]:
    st.header("💡 Suggestions")
    gap = resume_data.get("TopSkillGap", "relevant skills")
    st.markdown(f"""
- 🎯 Learn **{gap}** on LinkedIn, Coursera, or YouTube.
- ✍️ Rewrite resume bullets using STAR format.
- 💬 Mention **{gap}** in your profile.
- 💼 Add real projects for validation.
- 🎨 Avoid overly creative styles in conservative industries.
""")

# Tab 5 - Trends & Insights
with tabs[4]:
    st.header("📚 Trends & Insights")
    avg_score_by_edu = df.groupby("EducationLevel")["AI_MatchScore"].mean().sort_values()
    st.subheader("Average Match Score by Education Level")
    st.plotly_chart(px.bar(avg_score_by_edu, orientation='h'))

    field_score = df.groupby("FieldOfStudy")["AI_MatchScore"].mean().sort_values(ascending=False).head(10)
    st.subheader("Top Performing Fields")
    st.plotly_chart(px.bar(field_score))

    certs = df['Certifications'].dropna().str.split(', ').explode().value_counts().head(10)
    st.subheader("Popular Certifications")
    st.plotly_chart(px.bar(certs, title="Top Certifications"))

# Tab 6 - Download Report
with tabs[5]:
    st.header("📅 Download Report")
    text = f"""
Resume ID: {resume_data['ResumeID']}
Score: {resume_data['AI_MatchScore']}
Gap: {resume_data.get('TopSkillGap', 'N/A')}
Advice: Improve your skill in {resume_data.get('TopSkillGap', 'the missing area')} and update resume formatting.
"""
    st.download_button("📄 Download as TXT", data=text, file_name="resume_vs_reality.txt")


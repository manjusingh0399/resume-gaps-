import streamlit as st
import pandas as pd
import plotly.express as px

# Page Config
st.set_page_config(page_title="Resume vs Reality", layout="wide")

# 🌼 Custom Pastel Styling
st.markdown("""
    <style>
        html, body {
            background-color: #fdfcf7;
            font-family: 'Segoe UI', 'Helvetica Neue', sans-serif;
            color: #333333;
        }
        .stApp {
            background: linear-gradient(to bottom, #fffdf6 0%, #fef8e7 100%);
            padding: 1rem;
        }
        h1, h2, h3 {
            font-family: 'Georgia', serif;
            color: #6A0DAD;
        }
        .card {
            background-color: #ffffff;
            padding: 1.5rem;
            border-radius: 1rem;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
            margin-bottom: 1.5rem;
        }
        .streamlit-expanderHeader {
            font-weight: bold;
            color: #6A0DAD;
        }
        button[kind="primary"] {
            background-color: #ff8ba7 !important;
            color: white !important;
            border-radius: 10px;
            font-weight: bold;
        }
        .stDownloadButton > button {
            background-color: #ffb347 !important;
            color: white;
            border-radius: 10px;
            padding: 0.5rem 1rem;
            font-size: 16px;
            font-weight: 600;
        }
        .stProgress > div > div > div > div {
            background-color: #fbc687 !important;
        }
        .quote-box {
            font-style: italic;
            color: #444;
            background: #fff5d7;
            padding: 1rem;
            border-left: 5px solid #ffa500;
            border-radius: 10px;
            margin-top: 1.5rem;
        }
        .stTabs [data-baseweb="tab-list"] {
            margin-bottom: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

# Load Data
@st.cache_data(persist=True)
def load_data():
    return pd.read_csv("genz_resume_market_data.csv")

df = load_data()

# 💬 Welcome Section
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("""
        <h1>💼 Welcome to <em>Resume vs Reality</em></h1>
        <p><strong>Your sassy, smart career wingwoman. 💅</strong></p>
        <p>Ever stared at your resume wondering, "Will this get me hired or ghosted?" You're not alone. This app helps decode what recruiters truly want.</p>
        <ul>
            <li>💥 <strong>Mirror meets mentor:</strong> Know what your resume says <em>and</em> what it’s missing.</li>
            <li>🎯 <strong>Target your goals:</strong> Understand what job listings actually prioritize.</li>
            <li>🧠 <strong>Real feedback:</strong> Actionable advice based on real hiring data.</li>
            <li>🌈 <strong>Grow smart:</strong> Personalized suggestions to level-up fast.</li>
        </ul>
        <div class="quote-box">
            “Resumes don’t just speak for you — they whisper to recruiters. Let’s make sure yours is saying the right things.”
        </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Expanders
with st.expander("🛠 How to Use This App"):
    st.markdown("""
1. 👤 Select a Resume  
2. 📈 Compare to Market  
3. 📊 View Skill Match  
4. 💡 Get Suggestions  
5. 📅 Download a custom report
""")

with st.expander("🏡 What You'll Walk Away With"):
    st.markdown("""
- 🔍 Clarity on your resume  
- 🧠 Realistic hiring expectations  
- 🛠 Personalized growth roadmap  
- 💪 Confidence, backed by data
""")

# Resume Selector Logic
def get_resume_data():
    resume_ids = df['ResumeID'].unique()
    selected_id = st.selectbox("Select a Resume ID", resume_ids, key="resume_selector")
    resume_data = df[df['ResumeID'] == selected_id].iloc[0]
    return resume_data

# Tabs Setup
tabs = st.tabs([
    "👤 Profile Snapshot", 
    "📈 Market Comparison", 
    "📊 Match Score", 
    "💡 Suggestions", 
    "📚 Trends & Insights", 
    "📅 Download Report"
])

# Tab 1 - Profile Snapshot
with tabs[0]:
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.header("👤 Profile Snapshot")
        resume_data = get_resume_data()
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
        roles = role_mapping.get(field, ['General Analyst', 'Executive Trainee'])
        st.markdown(f"👀 Suggested Roles: {', '.join(roles)}")
        st.markdown('</div>', unsafe_allow_html=True)

# Tab 2 - Market Comparison
with tabs[1]:
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.header("📈 Market Comparison")
        st.subheader("AI Match Score by Domain")
        st.plotly_chart(px.box(df, x="Domain", y="AI_MatchScore", color="Domain", template="ggplot2"))
        st.subheader("Top Skill Gaps Across Resumes")
        gap_counts = df['TopSkillGap'].value_counts().head(10)
        st.plotly_chart(px.bar(gap_counts, title="Top Skill Gaps", template="ggplot2"))
        st.markdown('</div>', unsafe_allow_html=True)

# Tab 3 - Match Score
with tabs[2]:
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.header("📊 Match Score")
        listed = set(resume_data.get("SkillsListed", "").split(", "))
        required = set(resume_data.get("JobPostingSkillsRequired", "").split(", "))
        overlap = listed & required
        missing = required - listed
        st.metric("Skill Match", f"{len(overlap)} / {len(required)}")
        st.plotly_chart(px.pie(values=[len(overlap), len(missing)], names=["Matched", "Missing"], template="ggplot2"))
        st.markdown('</div>', unsafe_allow_html=True)

# Tab 4 - Suggestions
with tabs[3]:
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.header("💡 Suggestions")
        gap = resume_data.get("TopSkillGap", "relevant skills")
        st.markdown(f"""
- 📚 Learn **{gap}** via Coursera, LinkedIn Learning or YouTube  
- ✍️ Update bullets using STAR format (Situation, Task, Action, Result)  
- 🪞 Mention **{gap}** naturally in your summary  
- 💼 Add project links or GitHub if applying for tech/marketing  
- 🎨 Stick to minimal resumes for Finance/HR roles
""")
        st.markdown('</div>', unsafe_allow_html=True)

# Tab 5 - Trends & Insights
with tabs[4]:
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.header("📚 Trends & Insights")
        avg_score_by_edu = df.groupby("EducationLevel")["AI_MatchScore"].mean().sort_values()
        st.subheader("Avg. Match Score by Education")
        st.plotly_chart(px.bar(avg_score_by_edu, orientation='h', template="seaborn"))

        top_fields = df.groupby("FieldOfStudy")["AI_MatchScore"].mean().sort_values(ascending=False).head(10)
        st.subheader("Top Performing Fields")
        st.plotly_chart(px.bar(top_fields, title="Best Fields by Resume Match", template="seaborn"))

        certs = df['Certifications'].dropna().str.split(', ').explode().value_counts().head(10)
        st.subheader("Popular Certifications")
        st.plotly_chart(px.bar(certs, template="seaborn"))
        st.markdown('</div>', unsafe_allow_html=True)

# Tab 6 - Download Report
with tabs[5]:
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.header("📅 Download Report")
        text = f"""
Resume ID: {resume_data['ResumeID']}
Score: {resume_data['AI_MatchScore']}
Gap: {resume_data.get('TopSkillGap', 'N/A')}
Advice: Improve your skill in {resume_data.get('TopSkillGap', 'a key area')} and enhance formatting.
"""
        st.download_button("📄 Download as TXT", data=text, file_name="resume_vs_reality.txt")
        st.markdown('</div>', unsafe_allow_html=True)

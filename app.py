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
        .feedback-box {
            background-color: #ffeff5;
            border-left: 5px solid #ff8ba7;
            padding: 1rem;
            border-radius: 10px;
            margin-top: 1rem;
            color: #6A0DAD;
            font-style: italic;
        }
    </style>
""", unsafe_allow_html=True)

# === TITLE & TAGLINE ===
with st.container():
    st.markdown('<div class="card" style="text-align:center;">', unsafe_allow_html=True)
    st.markdown("""
        <h1 style="font-family: Georgia, serif; color:#6A0DAD; margin-bottom:0;">Job Snob</h1>
        <p style="font-size:1.2rem; font-style: italic; color:#ff8ba7; margin-top:0;">
            “Only the best skills make the cut. No basic resumes allowed.”
        </p>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Load Data
@st.cache_data(persist=True)
def load_data():
    return pd.read_csv("genz_resume_market_data.csv")

df = load_data()

# --- Sample Static Insights ---
match_score = 72
top_missing_skills = ['SQL', 'Tableau', 'Cloud Computing']
skill_insights = {
    'SQL': "Structured Query Language is essential for handling and analyzing data in databases.",
    'Tableau': "A leading tool for data visualization and business intelligence dashboards.",
    'Cloud Computing': "Increasingly vital for scalable and secure infrastructure (AWS, Azure, GCP)."
}
tailored_suggestions = [
    {'title': 'Data Analyst Path', 'why': 'You already know Excel and Python.', 'tip': 'Boost it with Tableau + SQL.'},
    {'title': 'Support Engineer', 'why': 'Strong communication skills.', 'tip': 'Pair it with CRM/Jira tools.'},
]

def get_resume_data():
    resume_ids = df['ResumeID'].unique()
    selected_id = st.selectbox("Select a Resume ID", resume_ids, key="resume_selector")
    return df[df['ResumeID'] == selected_id].iloc[0]

# --- Welcome + Match Score ---
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.title("📄 Resume vs Reality: Are You Job-Ready?")
    st.subheader("Compare your resume skills with real hiring data and get personalized advice.")
    st.markdown("</div>", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("📊 Resume Match Score")
    st.markdown("Here you see an overall match percentage showing how well your skills align with current hiring trends.")
    st.metric("🔍 Match Score", f"{match_score}%", delta="Based on hiring trends")
    if match_score > 85:
        st.success("🌟 Excellent Match!")
        st.markdown("""
        **Insight:** You’re highly aligned with the industry.  
        **Advice:** Keep updating your portfolio and prepare for behavioral interviews.  
        > “Success usually comes to those who are too busy to be looking for it.” – Thoreau
        """)
    elif match_score > 60:
        st.warning("🟡 Moderate Match")
        st.markdown("""
        **Insight:** You're close to market expectations, with a few skill gaps.  
        **Advice:** Focus on acquiring the top 2 missing skills below.  
        > “Don’t watch the clock; do what it does. Keep going.” – Sam Levenson
        """)
    else:
        st.error("🔴 Low Match")
        st.markdown("""
        **Insight:** Your resume doesn’t align with most current job needs.  
        **Advice:** Start small—learn one tool at a time.  
        > “The future depends on what you do today.” – Mahatma Gandhi
        """)
    st.markdown("</div>", unsafe_allow_html=True)

# --- Missing Skills & Career Advice ---
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("📉 Top Missing Skills & Why They Matter")
    st.markdown("This section highlights the skills most commonly missing from resumes like yours, but highly sought after by employers.")
    for skill in top_missing_skills:
        st.markdown(f"""
        ✅ **{skill}**  
        - _Why it matters:_ {skill_insights[skill]}  
        - _Where to learn:_ [LinkedIn Learning](#) · [Coursera](#) · [YouTube](#)  
        > “Every expert was once a beginner.”
        """)
    st.markdown('<div class="feedback-box">💡 <strong>Tip:</strong> Start by focusing on one missing skill. Small consistent steps win the race.</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("🚀 Career Suggestions Tailored to You")
    st.markdown("Based on your current skills, here are some curated career paths you could consider along with actionable next steps.")
    for suggestion in tailored_suggestions:
        st.markdown(f"""
        💼 **{suggestion['title']}**  
        - _Why this fits:_ {suggestion['why']}  
        - _Your next step:_ {suggestion['tip']}  
        > “Opportunities don’t happen, you create them.” – Chris Grosser
        """)
    st.markdown('<div class="feedback-box">💬 Remember, your career is a journey. Keep exploring and growing every day!</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- Motivational Reminder ---
with st.container():
    st.markdown('<div class="quote-box">', unsafe_allow_html=True)
    st.markdown("""
    💬 **Reminder:** Your resume is a snapshot, not a verdict.  
    _“Believe you can and you're halfway there.” – Theodore Roosevelt_
    """)
    st.markdown("</div>", unsafe_allow_html=True)

# --- Intro Expander Section ---
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("""
        <h1>💼 Welcome to <em>Resume vs Reality</em></h1>
        <p><strong>Your sassy, smart career wingwoman. 💅</strong></p>
        <p>This app decodes what recruiters really want.</p>
        <ul>
            <li>💥 <strong>Mirror meets mentor:</strong> Know what your resume says and what it’s missing.</li>
            <li>🎯 <strong>Target your goals:</strong> See what employers actually look for.</li>
            <li>🧠 <strong>Real feedback:</strong> Actionable advice from hiring data.</li>
            <li>🌈 <strong>Grow smart:</strong> Personal tips to level-up faster.</li>
        </ul>
        <div class="quote-box">
            “Resumes don’t just speak for you — they whisper to recruiters. Let’s make sure yours is saying the right things.”
        </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

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

# --- Interactive Tabs ---
tabs = st.tabs([
    "👤 Profile Snapshot", 
    "📈 Market Comparison", 
    "📊 Match Score", 
    "💡 Suggestions", 
    "📚 Trends & Insights", 
    "📅 Download Report"
])

# Tab 1 - Profile
with tabs[0]:
    resume_data = get_resume_data()
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.header("👤 Profile Snapshot")
        st.markdown("Here’s a quick overview of your profile based on the selected resume. Understand your background and current match score.")
        st.write(f"**Age:** {resume_data['Age']}")
        st.write(f"**Education:** {resume_data['EducationLevel']} in {resume_data['FieldOfStudy']}")
        st.write(f"**Applied For:** {resume_data['JobAppliedFor']}")
        st.write(f"**Resume Style:** {resume_data['ResumeStyle']}")
        st.write(f"**Certifications:** {resume_data['Certifications'] if pd.notna(resume_data['Certifications']) else 'None'}")
        st.metric("AI Match Score", f"{resume_data['AI_MatchScore']}/100")
        st.progress(resume_data["AI_MatchScore"] / 100)
        role_map = {
            'Data Science': ['Data Analyst', 'ML Engineer'],
            'Marketing': ['Brand Associate', 'Content Strategist'],
            'Finance': ['Credit Analyst', 'Business Analyst']
        }
        roles = role_map.get(resume_data['FieldOfStudy'], ['General Analyst', 'Executive Trainee'])
        st.markdown(f"👀 Suggested Roles: {', '.join(roles)}")
        st.markdown('<div class="feedback-box">✨ Tip: Keep your resume updated and tailor it per role for best results.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# Tab 2 - Market Comparison
with tabs[1]:
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.header("📈 Market Comparison")
        st.markdown("Analyze how your resume's domain and skills compare to the broader market and see common skill gaps.")
        st.subheader("AI Match Score by Domain")
        st.plotly_chart(px.box(df, x="Domain", y="AI_MatchScore", color="Domain", template="ggplot2"))
        st.subheader("Top Skill Gaps Across Resumes")
        gap_counts = df['TopSkillGap'].value_counts().head(10)
        st.plotly_chart(px.bar(gap_counts, title="Top Skill Gaps", template="ggplot2"))
        st.markdown('<div class="feedback-box">🔍 Insight: Focus on bridging the top skill gaps to improve your market fit.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# Tab 3 - Match Score Pie
with tabs[2]:
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.header("📊 Match Score Breakdown")
        st.markdown("This visual breaks down how many job-required skills you currently match versus the ones missing.")
        listed = set(resume_data.get("SkillsListed", "").split(", "))
        required = set(resume_data.get("JobPostingSkillsRequired", "").split(", "))
        overlap = listed & required
        missing = required - listed
        st.metric("Skill Match", f"{len(overlap)} / {len(required)}")
        st.plotly_chart(px.pie(values=[len(overlap), len(missing)], names=["Matched", "Missing"], template="ggplot2"))
        st.markdown('<div class="feedback-box">💡 Feedback: Focus your upskilling on the missing skills for a better match.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# Tab 4 - Suggestions
with tabs[3]:
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.header("💡 Suggestions")
        st.markdown("Based on your resume gaps, here are targeted recommendations to strengthen your profile.")
        gap = resume_data.get("TopSkillGap", "a key skill")
        st.markdown(f"""
- 📚 Learn **{gap}** via Coursera, LinkedIn Learning, or YouTube  
- ✍️ Update your resume bullets using the STAR format (Situation, Task, Action, Result)  
- 🪞 Naturally mention **{gap}** in your summary section  
- 💼 Add relevant project links or GitHub repos if applying for technical roles  
- 🎨 Keep it minimal and clear for Finance or HR roles
""")
        st.markdown('<div class="feedback-box">🚀 Pro tip: Consistent small improvements in your resume skills can lead to big wins.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# Tab 5 - Trends
with tabs[4]:
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.header("📚 Trends & Insights")
        st.markdown("Explore hiring trends by education, fields of study, and popular certifications to inform your career strategy.")
        avg_score = df.groupby("EducationLevel")["AI_MatchScore"].mean().sort_values()
        top_fields = df.groupby("FieldOfStudy")["AI_MatchScore"].mean().sort_values(ascending=False).head(10)
        certs = df['Certifications'].dropna().str.split(', ').explode().value_counts().head(10)
        st.subheader("Avg. Score by Education")
        st.plotly_chart(px.bar(avg_score, orientation='h', template="seaborn"))
        st.subheader("Top Performing Fields")
        st.plotly_chart(px.bar(top_fields, template="seaborn"))
        st.subheader("Popular Certifications")
        st.plotly_chart(px.bar(certs, template="seaborn"))
        st.markdown('<div class="feedback-box">📈 Insight: Certifications like these boost resume appeal in competitive fields.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# Tab 6 - Download Report
with tabs[5]:
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.header("📅 Download Report")
        st.markdown("Download a personalized report summarizing your resume match and tailored advice.")
        resume_data = get_resume_data()
        text = f"""
Resume ID: {resume_data['ResumeID']}
Score: {resume_data['AI_MatchScore']}
Gap: {resume_data.get('TopSkillGap', 'N/A')}
Advice: Improve your skill in {resume_data.get('TopSkillGap', 'a key area')} and enhance formatting.
"""
        st.download_button("📄 Download as TXT", data=text, file_name="resume_vs_reality.txt")
        st.markdown('<div class="feedback-box">🎉 Great job! Use this report to guide your next career moves.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

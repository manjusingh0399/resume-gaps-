# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io

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

# Load dataset
@st.cache_data

def load_data():
    return pd.read_csv("genz_resume_market_data.csv")

df = load_data()

# --- Welcome Tab ---
st.markdown("""
<div class="welcome-container">
<h1>💼 Welcome to <span style='color:#3b82f6'>Resume vs Reality</span></h1>
<h3>Your sassy, smart career wingwoman. 💁‍♀️</h3>
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
""")

with st.expander("🛠️ How to Use This App"):
    st.markdown("""
1. **👤 Profile Snapshot** – Upload or select a sample resume. Get the overview.
2. **📈 Market Comparison** – How does your resume stand in your chosen field?
3. **📊 Match Score** – Visual breakdown of how close you are to ideal profiles.
4. **💡 Suggestions** – Helpful, no-BS advice to close skill and keyword gaps.
5. **📥 Download Report** – Save your growth map as a TXT report.
""")

with st.expander("🎁 What You'll Walk Away With"):
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
tabs = st.tabs(["👤 Profile Snapshot", "📈 Market Comparison", "📊 Match Score", "💡 Suggestions", "📥 Download Report"])




# --- Tab 0: Profile Snapshot ---
with tabs[0]:
    st.subheader("👤 Profile Snapshot")
    resume_ids = df["ResumeID"].unique()
    selected_resume = st.selectbox("🎯 Select a Resume ID to Explore", resume_ids)
    resume_data = df[df["ResumeID"] == selected_resume].iloc[0]

    st.markdown("### 💼 Quick Glance")
    st.write("Let’s break this down like your favorite sibling explaining what matters — quick, honest, and always with your best interest in mind.")

    col1, col2, col3 = st.columns([1,1,1])
    with col1:
        st.metric("🎓 Education Level", resume_data['EducationLevel'])
        st.metric("🧠 Gen Z Traits", resume_data['GenZ_Trait_Tags'])
    with col2:
        st.metric("📌 Applied Role", resume_data['JobAppliedFor'])
        st.metric("📑 Resume Style", resume_data['ResumeStyle'])
    with col3:
        st.metric("🎯 AI Match Score", f"{resume_data['AI_MatchScore']}/100")
        st.metric("🎟 Certifications", resume_data['Certifications'])

    st.markdown("---")
    st.markdown("### 🧬 Field of Study")
    st.info(f"You’re coming from a background in **{resume_data['FieldOfStudy']}**, which is a solid start for someone aiming to become a {resume_data['JobAppliedFor']}. Let's see if your skills align.")

    st.markdown("### 🧰 Skill Comparison")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**✅ Skills You Listed**")
        st.code("\n".join(resume_data["SkillsListed"].split(", ")))
    with col2:
        st.markdown("**📌 Skills the Role Wants**")
        st.code("\n".join(resume_data["JobPostingSkillsRequired"].split(", ")))

    listed = len(resume_data['SkillsListed'].split(', '))
    required = len(resume_data['JobPostingSkillsRequired'].split(', '))
    gap = required - listed

    st.markdown("### 💡 Insight + Big Sis Advice")
    if gap > 0:
        st.warning(f"You listed **{listed}** skills, but this role expects around **{required}**. That's a gap of {gap} important ones. Don’t panic — now we know what to fix. This is your growth checklist!")
        st.info("💬 Tip: Try adding **one skill per project** you've done — be specific. Recruiters love context, not just buzzwords.")
    elif gap == 0:
        st.success("You're right on target with skill count! Now make sure they're **quality, not just quantity**. Would an employer *feel* your experience from those words?")
    else:
        st.success("You've got more skills listed than required — great! But double-check: Are they relevant to **this** job? Sometimes trimming down is powerful.")

    st.markdown("---")
    st.markdown("👀 Let’s dive deeper into market trends next. If you were a product, how in-demand would you be?")

# --- Tab 1: Market Comparison ---
with tabs[1]:
    st.subheader("📈 Market Comparison")
    domain_scores = df.groupby("Domain")["AI_MatchScore"].mean().sort_values().reset_index()
    fig = px.bar(
        domain_scores,
        x="AI_MatchScore", y="Domain",
        orientation="h",
        title="🔍 Average AI Match Score by Domain",
        color="AI_MatchScore",
        color_continuous_scale="Blues"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 💬 Big Sis Says:")
    st.info("🧠 If you're in domains like **Data Science** or **Marketing**, you're in high demand — but competition is fierce. Stay sharp and stay learning.")

    st.subheader("📌 Top 10 Skill Gaps Across All Resumes")
    top_gaps = df["TopSkillGap"].value_counts().head(10).reset_index()
    top_gaps.columns = ["Skill", "Count"]
    fig2 = px.bar(top_gaps, x="Count", y="Skill", orientation="h", color="Count", title="Top Skill Gaps in Market")
    st.plotly_chart(fig2, use_container_width=True)

    st.warning("🔎 Tip: Even one missing key skill can get your resume skipped. Focus on high-frequency gaps first.")

# --- Tab 2: Match Score Breakdown ---
with tabs[2]:
    st.subheader("📊 Resume vs Market Match Score")
    skills_present = len(resume_data["SkillsListed"].split(", "))
    skills_required = len(resume_data["JobPostingSkillsRequired"].split(", "))
    match_score = resume_data["AI_MatchScore"]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=[skills_present, skills_required, match_score / 10],
        theta=['Skills Listed', 'Skills Required', 'AI Match Score'],
        fill='toself',
        name='Resume Match'
    ))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True)), showlegend=False)
    st.plotly_chart(fig)

    st.markdown("### 💡 Score Insight")
    if match_score < 50:
        st.error("🚨 Your match score is quite low. Let’s work on building stronger, more aligned skill sets.")
    elif match_score < 75:
        st.warning("⚠️ You’re getting there! Focus on polishing those 2–3 missing skills.")
    else:
        st.success("🎉 Your resume is hitting the mark! Still — there's always room to sparkle more ✨.")

# --- Tab 3: Suggestions ---
with tabs[3]:
    st.subheader("💡 Suggestions from Your Career Mentor")
    gap = resume_data["TopSkillGap"]
    st.markdown(f"### 🔎 Personalized Feedback for Resume ID: {selected_resume}")

    if gap != 'None':
        st.warning(f"💥 You’re missing **{gap}** — a high-impact skill for this role.")
        st.markdown(f"📚 **Advice:** Enroll in a free course on {gap} from platforms like Coursera, edX, or YouTube today. Just 1 hour a week can change your life.")
    else:
        st.success("🎯 You don’t have any major skill gaps — now focus on telling your story with clarity and confidence.")

    style = resume_data["ResumeStyle"]
    if style == "Minimalist":
        st.info("🧾 Minimalist resumes are clean. Add color blocks or project sections if you’re applying for creative roles.")
    elif style == "Infographic":
        st.warning("📊 Infographics are eye-catching but risky for ATS. Keep a simpler version ready for big company portals.")

    st.markdown("### 🧠 Advice Nuggets")
    st.markdown("""
- Use strong verbs like *built*, *led*, *analyzed*, *scaled*.
- Quantify achievements: “Increased engagement by 45%”, “Reduced churn by 12%”.
- One resume doesn’t fit all — tweak keywords per job.
- Confidence doesn’t mean overstuffing — clarity wins.
""")

# --- Tab 4: Download Report ---
with tabs[4]:
    st.subheader("📥 Export Your Report")

    report_text = f'''
    📄 Resume ID: {resume_data["ResumeID"]}
    🧠 Match Score: {resume_data["AI_MatchScore"]}/100
    ❌ Skill Gap: {gap}
    🎨 Style: {resume_data["ResumeStyle"]}
    ✨ Advice:
    - Close skill gap by learning {gap} if applicable.
    - Optimize resume structure based on ATS-friendliness.
    - Use action-driven language and match job keywords.
    '''
    st.download_button(
        label="Download as TXT",
        data=report_text.encode('utf-8'),
        file_name="resume_vs_reality_report.txt",
        mime="text/plain"
    )

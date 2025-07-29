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
</style>
""", unsafe_allow_html=True)

st.title("📄 Resume vs Reality")
st.caption("Let your resume speak reality, not just aspiration.")

# Load dataset
@st.cache_data

def load_data():
    return pd.read_csv("genz_resume_market_data.csv")

df = load_data()

# Tabs
tabs = st.tabs(["📝 Resume Overview", "📈 Market Comparison", "📊 Match Score", "💡 Suggestions", "📥 Download Report"])

# --- Tab 0: Resume Overview ---
with tabs[0]:
    st.subheader("📝 Resume Overview")
    resume_ids = df["ResumeID"].unique()
    selected_resume = st.selectbox("🎯 Choose a Resume ID to Analyze", resume_ids)
    resume_data = df[df["ResumeID"] == selected_resume].iloc[0]

    st.markdown("""
    <div style='background-color:#f0f4ff;padding:20px;border-radius:10px'>
    <h4>📌 Resume Summary</h4>
    <ul>
      <li><b>Age:</b> {}</li>
      <li><b>Education Level:</b> {}</li>
      <li><b>Field of Study:</b> {}</li>
      <li><b>Applied Job:</b> {}</li>
      <li><b>Resume Style:</b> {}</li>
      <li><b>GenZ Traits:</b> {}</li>
      <li><b>Certifications:</b> {}</li>
    </ul>
    </div>
    """.format(
        resume_data['Age'], resume_data['EducationLevel'], resume_data['FieldOfStudy'],
        resume_data['JobAppliedFor'], resume_data['ResumeStyle'], resume_data['GenZ_Trait_Tags'], resume_data['Certifications']
    ), unsafe_allow_html=True)

    st.markdown(f"### 🧠 Insight:")
    st.info(f"This candidate is applying for **{resume_data['JobAppliedFor']}** with a background in **{resume_data['FieldOfStudy']}**. Let's see how their skills match the market.")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🧰 Skills in Resume")
        st.write(resume_data["SkillsListed"].split(", "))
    with col2:
        st.markdown("### 🧠 Skills Required by Job")
        st.write(resume_data["JobPostingSkillsRequired"].split(", "))

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

    st.markdown("### 📊 Insight:")
    st.success("Data and Marketing domains currently show the highest match scores among Gen Z applicants.")

    st.subheader("📌 Most Common Top Skill Gaps")
    top_gaps = df["TopSkillGap"].value_counts().head(10).reset_index()
    top_gaps.columns = ["Skill", "Count"]
    fig2 = px.bar(top_gaps, x="Count", y="Skill", orientation="h", title="Top 10 Skill Gaps", color="Count")
    st.plotly_chart(fig2, use_container_width=True)

    st.info("These are the most common missing skills across all resumes. Prioritize filling these gaps if you're applying to tech-heavy roles.")

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

    st.markdown("### 🔍 Insight:")
    st.warning(f"You listed **{skills_present}** skills, but **{skills_required}** were expected. Your AI match score is **{match_score}/100**. Focus on aligning more with job expectations.")

# --- Tab 3: Suggestions ---
with tabs[3]:
    st.subheader("💡 Mentor Suggestions")
    gap = resume_data['TopSkillGap']
    st.markdown(f"### 🚀 Personalized Tips for Resume ID: {selected_resume}")

    if gap != 'None':
        st.warning(f"🔧 Top Skill Gap: **{gap}**. Consider learning it via free platforms like Coursera or YouTube.")
    else:
        st.success("✅ No major skill gaps! You're doing great!")

    style = resume_data["ResumeStyle"]
    if style == "Minimalist":
        st.info("🎨 Your resume style is clean. Make sure it also stands out visually.")
    elif style == "Infographic":
        st.warning("⚠️ Infographic resumes look great, but be cautious — ATS systems may not parse them correctly.")

    st.markdown("### 📌 Insight:")
    st.info("Tailoring your resume style to the job you're applying for — while maintaining ATS compatibility — increases your shortlisting chances.")

# --- Tab 4: Download Report ---
with tabs[4]:
    st.subheader("📥 Export Your Report")
    if st.button("📥 Download My Resume Report"):
        result_text = f"""
        Resume ID: {resume_data['ResumeID']}
        Match Score: {match_score}
        Skill Gap: {gap}
        Style: {style}
        Suggested Improvement: Learn {gap} and improve formatting if applying to ATS-heavy roles.
        """
        st.download_button("Download as TXT", io.StringIO(result_text), file_name="resume_vs_reality_report.txt")

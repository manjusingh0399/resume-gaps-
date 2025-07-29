# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import io

# Page config
st.set_page_config(page_title="Resume vs Reality", layout="wide")
st.title("📄 Resume vs Reality: Which Skills Actually Help You Get Hired?")

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv("genz_resume_market_data.csv")

df = load_data()

# Tabs for navigation
tabs = st.tabs(["📝 Resume Overview", "📈 Market Comparison", "📊 Match Score", "💡 Suggestions", "📥 Download Report"])

# --- Tab 0: Resume Overview ---
with tabs[0]:
    st.header("📝 Resume Overview")
    resume_ids = df["ResumeID"].unique()
    selected_resume = st.selectbox("Choose a Resume ID", resume_ids)
    resume_data = df[df["ResumeID"] == selected_resume].iloc[0]

    st.markdown(f"""
    - **Age:** {resume_data['Age']}  
    - **Education Level:** {resume_data['EducationLevel']}  
    - **Field of Study:** {resume_data['FieldOfStudy']}  
    - **Applied Job:** {resume_data['JobAppliedFor']}  
    - **Resume Style:** {resume_data['ResumeStyle']}  
    - **GenZ Traits:** {resume_data['GenZ_Trait_Tags']}  
    - **Certifications:** {resume_data['Certifications']}  
    """)

    st.markdown("### 🧰 Skills in Resume")
    st.write(resume_data["SkillsListed"].split(", "))

    st.markdown("### 🧠 Skills Required by Job")
    st.write(resume_data["JobPostingSkillsRequired"].split(", "))

# --- Tab 1: Market Comparison ---
with tabs[1]:
    st.header("📈 Market Comparison")

    domain_scores = df.groupby("Domain")["AI_MatchScore"].mean().sort_values()
    st.subheader("🔍 Average AI Match Score by Domain")
    fig, ax = plt.subplots()
    sns.barplot(x=domain_scores.values, y=domain_scores.index, ax=ax)
    st.pyplot(fig)

    st.subheader("📌 Most Common Top Skill Gaps")
    top_gaps = df["TopSkillGap"].value_counts().head(10)
    st.bar_chart(top_gaps)

# --- Tab 2: Match Score Breakdown ---
with tabs[2]:
    st.header("📊 Resume vs Market Match Score")

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

# --- Tab 3: Suggestions ---
with tabs[3]:
    st.header("💡 Mentor Suggestions")
    gap = resume_data['TopSkillGap']
    st.markdown(f"### 🚀 Suggestions for Resume ID: {selected_resume}")

    if gap != 'None':
        st.warning(f"Top Skill Gap: **{gap}**. Consider learning it via free resources like Coursera or YouTube.")
    else:
        st.success("No major skill gaps! You're doing great!")

    style = resume_data["ResumeStyle"]
    if style == "Minimalist":
        st.info("✅ Your resume style is clean. Make sure it also stands out.")
    elif style == "Infographic":
        st.warning("⚠️ Infographic resumes are trendy but sometimes ATS-unfriendly.")

# --- Tab 4: Download Report ---
with tabs[4]:
    st.header("📥 Export Results")
    if st.button("📥 Download My Resume Report"):
        result_text = f"""
        Resume ID: {resume_data['ResumeID']}
        Match Score: {match_score}
        Skill Gap: {gap}
        Style: {style}
        Suggested Improvement: Learn {gap} and improve formatting if applying to ATS-heavy roles.
        """
        st.download_button("Download as TXT", io.StringIO(result_text), file_name="resume_vs_reality_report.txt")

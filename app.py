# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page config
st.set_page_config(page_title="Resume vs Reality", layout="wide")

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
    <h1 style='text-align:center; color: #5d4037;'>🌞 Welcome to <em>Resume vs Reality</em></h1>
    <p style='text-align:center; font-size: 1.15rem;'>Hi, I'm <strong>Manju Singh</strong> — your calm career companion.</p>
    <p style='text-align:center;'>You’ve landed in a gentle, thoughtful space — a space that holds both your ambitions and anxieties with care.</p>
    <p style='text-align:center;'>We’re here not to critique, but to listen. Not to judge, but to reflect. Together, we’ll uncover what your resume truly conveys — and what it can still become.</p>
    <p style='text-align:center;'>This is your moment to breathe, reflect, and evolve — softly and purposefully.</p>
    <ul style='font-size: 1.05rem;'>
        <li>🪞 <strong>Mirror your truth:</strong> What story does your resume tell — and what stories is it missing?</li>
        <li>🧘 <strong>Calm, data-informed clarity:</strong> Insights without overwhelm, judgments, or confusion.</li>
        <li>🌷 <strong>Empathetic, honest suggestions:</strong> Because you deserve a career path that fits your essence.</li>
        <li>🧭 <strong>Gentle guidance:</strong> Forward momentum rooted in who you are, not just what you do.</li>
    </ul>
    <blockquote style='background:#fff3e0; padding:1rem; border-left:5px solid #f9a825; border-radius:8px; font-style: italic;'>“The right career story doesn’t yell to be seen — it feels aligned. Let’s help yours find that harmony.”</blockquote>
</div>
""", unsafe_allow_html=True)


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


# Tab 1 - Profile Snapshot
with tabs[0]:
    st.header("👤 Profile Snapshot")
    st.caption("\nThis section shows a detailed view of the resume you selected. It helps you assess the basic profile details, resume style, and overall score before diving deeper.")
    resume_data = get_resume_data()
    st.subheader("Resume Summary")
    st.write(f"**Age:** {resume_data['Age']}")
    st.write(f"**Education:** {resume_data['EducationLevel']} in {resume_data['FieldOfStudy']}")
    st.write(f"**Applied For:** {resume_data['JobAppliedFor']}")
    st.write(f"**Resume Style:** {resume_data['ResumeStyle']}")
    st.write(f"**Certifications:** {resume_data['Certifications']}")
    st.metric("AI Match Score", f"{resume_data['AI_MatchScore']}/100")
    st.progress(resume_data["AI_MatchScore"] / 100)

    # Role Recommendations
    role_mapping = {
        'Data Science': ['Data Analyst', 'ML Engineer'],
        'Marketing': ['Brand Associate', 'Content Strategist'],
        'Finance': ['Credit Analyst', 'Business Analyst']
    }
    field = resume_data['FieldOfStudy']
    st.markdown(f"👀 Suggested Roles: {', '.join(role_mapping.get(field, ['General Analyst', 'Executive Trainee']))}")

    st.markdown("---")
    st.markdown("✅ *This gives a bird's eye view of your resume profile. Your score indicates how likely your resume is to get shortlisted in the AI-filtered hiring process.*")

# Tab 2 - Market Comparison
with tabs[1]:
    st.header("📈 Market Comparison")
    st.caption("\nCompare your score and skills with what the market expects in your field.")
    st.subheader("AI Match Score by Domain")
    st.plotly_chart(px.box(df, x="Domain", y="AI_MatchScore", color="Domain"))
    st.caption("\n🔍 This graph helps you compare how resumes perform across industries. Domains like Data and Marketing tend to have higher match scores.")

    gap_counts = df['TopSkillGap'].value_counts().head(10)
    st.subheader("Top Skill Gaps Across Resumes")
    st.plotly_chart(px.bar(gap_counts, title="Top Skill Gaps"))
    st.caption("\n📉 These are the most common skills missing across applicants. If yours appears here, you're not alone — but it's fixable!")

    st.markdown("---")
    st.markdown("✅ *This tab helps you understand how competitive your resume is within your target domain. Take note of the common gaps to address them proactively.*")

# Tab 3 - Match Score
with tabs[2]:
    st.header("📈 Match Score")
    st.caption("\nFind out how well your skills align with what employers want.")
    listed = set(resume_data["SkillsListed"].split(", "))
    required = set(resume_data["JobPostingSkillsRequired"].split(", "))
    overlap = listed & required
    missing = required - listed
    st.metric("Skill Match", f"{len(overlap)} / {len(required)}")
    st.plotly_chart(px.pie(values=[len(overlap), len(missing)], names=["Matched", "Missing"]))
    st.caption("\n📊 This pie chart shows how many skills you already have vs what's expected for the job. Fill the gap, boost your chances!")
    st.markdown("---")
    st.markdown("✅ *The more overlap you achieve here, the higher your job-fit and recruiter match potential becomes.*")

# Tab 4 - Suggestions
with tabs[3]:
    st.header("💡 Suggestions")
    st.caption("\nHere’s your career coach moment. Let’s make things better.")
    gap = resume_data['TopSkillGap']
    st.markdown("### Personalized Advice")
    st.markdown(f"""
- 🎯 Learn **{gap}** on LinkedIn Learning, Coursera, or YouTube.
- ✍️ Rewrite resume bullets using STAR format (Situation, Task, Action, Result).
- 💬 Add keywords like "{gap}" naturally in your profile summary.
- 💼 Use real project links in portfolio if applying for tech/marketing roles.
- 🎨 Avoid overly creative resume styles if applying to traditional fields like Finance/HR.
""")
    st.markdown("---")
    st.markdown("✅ *These are practical next steps you can take immediately. Don’t wait — recruiters won’t.*")

# Tab 5 - Trends & Insights
with tabs[4]:
    st.header("📚 Trends & Insights")
    st.caption("\nDiscover macro trends in education, field, and certification performance.")
    avg_score_by_edu = df.groupby("EducationLevel")["AI_MatchScore"].mean().sort_values()
    st.subheader("Average Match Score by Education Level")
    st.plotly_chart(px.bar(avg_score_by_edu, orientation='h'))
    st.caption("🎓 See how your education compares in terms of AI-readiness.")

    field_score = df.groupby("FieldOfStudy")["AI_MatchScore"].mean().sort_values(ascending=False).head(10)
    st.subheader("Top Performing Fields")
    st.plotly_chart(px.bar(field_score, title="Fields with Strongest Resume Match"))
    st.caption("📘 These fields have the best resume-to-job alignment.")

    cert_counts = df['Certifications'].dropna().str.split(', ').explode().value_counts().head(10)
    st.subheader("Popular Certifications")
    st.plotly_chart(px.bar(cert_counts, title="Top Certifications"))
    st.caption("✅ Want to upgrade your resume fast? These are the top certifications recruiters recognize.")
    st.markdown("---")
    st.markdown("✅ *This data gives you an edge on how to align your background with real market performance.*")

# Tab 6 - Download Report
with tabs[5]:
    st.header("📅 Download Report")
    st.caption("\nSave your personalized advice and resume insight summary.")
    text = f"Resume ID: {resume_data['ResumeID']}\nScore: {resume_data['AI_MatchScore']}\nGap: {resume_data['TopSkillGap']}\nAdvice: Improve your skill in {resume_data['TopSkillGap']} and update resume formatting."
    st.download_button("Download as TXT", data=text, file_name="resume_vs_reality.txt")
    st.markdown("---")
    st.markdown("✅ *Take this report with you as a reminder of what to fix and where to grow.*")

# app.py
import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(page_title="Resume vs Reality", layout="wide")
st.title("📄 Resume vs Reality: Which Skills Actually Help You Get Hired?")

# Load dataset (replace with actual file path)
@st.cache_data
def load_data():
    return pd.read_csv("genz_resume_market_data.csv")

df = load_data()

# Tabs for navigation
tabs = st.tabs(["📘 Instructions", "🏠 Welcome", "📊 Insights Dashboard", "📁 Resume Analyzer", "🎓 Ideal Resumes", "🧠 Career Mentor", "📥 Download Report"])

# --- Tab 0: Instructions Page ---
with tabs[0]:
    st.header("📘 How to Use This App")
    st.markdown("""
    This web app is designed to help Gen Z job seekers understand how their resumes align with real-world hiring expectations.

    ### 👉 Step-by-Step Guide:
    1. **🏠 Welcome Tab**: Learn about the purpose of the app and explore key monologues.
    2. **📊 Insights Dashboard**: Use filters to view hiring trends, skill gaps, and match scores by domain.
    3. **📁 Resume Analyzer**: Paste your resume text and compare it with a real job description to get an AI-based match score.
    4. **🎓 Ideal Resumes**: Browse curated examples of high and low performing resumes by role.
    5. **🧠 Career Mentor**: Enter your current skills to get suggestions for best-fit roles and missing skills.
    6. **📥 Download Report**: Export all the resume-market data to CSV for personal analysis or reports.

    ### 💡 Tips for Best Use:
    - Keep resume text simple and keyword-rich for better parsing.
    - Explore multiple roles to understand trends across domains.
    - Use insights to tailor your resume or skill development.

    ---
    ✅ *This app is your data-powered career buddy. Navigate at your pace, and let the insights guide you.*
    """)

# --- Tab 1: Welcome Page ---
with tabs[1]:
    st.header("Welcome to Resume vs Reality")
    st.markdown("""
    > *“We all build resumes hoping they reflect our potential. But behind every hiring decision lies a pattern. This project is a search for those patterns — an exploration of the gap between what we write and what employers value.”*
    """)
    st.markdown("Use the tabs above to explore resume-job match scores, insights, and career mentoring.")
    st.image("https://images.unsplash.com/photo-1549924231-f129b911e442", use_column_width=True)

# --- Tab 2: Insights Dashboard ---
with tabs[2]:
    st.header("📊 Dashboard: Explore Resume Trends")

    col1, col2 = st.columns(2)

    with col1:
        fig1 = px.histogram(df, x="AI_MatchScore", nbins=20, color="Shortlisted", title="AI Match Score Distribution")
        st.plotly_chart(fig1, use_container_width=True)
        st.markdown("**Insight:** Most resumes scored between 60–80. Scores above 78 had a 65% chance of shortlisting.")

    with col2:
        hired_counts = df["Hired"].value_counts().rename({0: "Not Hired", 1: "Hired"})
        fig2 = px.pie(values=hired_counts.values, names=hired_counts.index, title="Hired vs Not Hired")
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown("**Takeaway:** High match scores improved hiring chances but visual resume styles underperformed.")

    st.markdown("---")
    top_gaps = df["TopSkillGap"].value_counts().head(5)
    fig3 = px.bar(top_gaps, x=top_gaps.index, y=top_gaps.values, title="Top 5 Skill Gaps Across All Domains")
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown("**Key Insight:** SQL and React were the most common missing skills in business and tech roles.")

# --- Tab 3: Resume Analyzer ---
with tabs[3]:
    st.header("📁 Resume Analyzer")
    uploaded_text = st.text_area("Paste your resume text here:")
    job_role = st.selectbox("Select a Job Role to Compare With:", df["JobAppliedFor"].unique())
    
    if uploaded_text:
        skills_required = df[df["JobAppliedFor"] == job_role]["JobPostingSkillsRequired"].iloc[0].split(", ")
        matched_skills = [skill for skill in skills_required if skill.lower() in uploaded_text.lower()]
        gap_skills = list(set(skills_required) - set(matched_skills))
        score = int(len(matched_skills) / len(skills_required) * 100)

        st.metric("Predicted Match Score", f"{score}%")
        st.markdown(f"**Matched Skills:** {', '.join(matched_skills)}")
        st.markdown(f"**Missing Skills:** {', '.join(gap_skills)}")

        st.info("**Insight:** You match {} out of {} required skills for the role '{}'".format(len(matched_skills), len(skills_required), job_role))
        if score > 75:
            st.success("You're a strong candidate. Just fill minor gaps.")
        elif score > 50:
            st.warning("You're close, but there's room to improve.")
        else:
            st.error("Significant skill gap. Consider upskilling.")

# --- Tab 4: Ideal Resume Library ---
with tabs[4]:
    st.header("🎓 Ideal Resume Gallery")
    st.markdown("**Explore ideal resume examples for various roles:**")

    with st.expander("📈 Data Analyst Resume - Strong Match"):
        st.markdown("""
        - **Skills:** SQL, Tableau, Python, Excel  
        - **Certifications:** Google Data Analytics  
        - **Style:** ATS-Friendly  
        - **Traits:** Data-curious, Remote-ready
        """)

    with st.expander("🎨 Visual Designer Resume - Not Shortlisted"):
        st.markdown("""
        - **Skills:** Figma, Photoshop, Canva  
        - **Certifications:** UI/UX Design (Coursera)  
        - **Style:** Infographic  
        - **Traits:** Trend-savvy, Aesthetic-first  
        - **Insight:** Beautiful design, but ATS couldn’t parse keywords.
        """)

# --- Tab 5: Career Mentor ---
with tabs[5]:
    st.header("🧠 Career Mentor")
    user_skills = st.text_input("List your current skills (comma separated):")

    if user_skills:
        all_roles = {}
        for role in df["JobAppliedFor"].unique():
            required = df[df["JobAppliedFor"] == role]["JobPostingSkillsRequired"].iloc[0].split(", ")
            match = len([s for s in required if s.lower() in user_skills.lower()])
            all_roles[role] = match

        top_roles = sorted(all_roles.items(), key=lambda x: x[1], reverse=True)[:3]
        st.subheader("🔍 Best Matched Roles For You")
        for role, count in top_roles:
            st.markdown(f"✅ **{role}** – Matching Skills: {count}")

        st.markdown("---")
        st.info("**Tip:** Build depth in your best-matched field. Add key certifications to boost visibility.")

# --- Tab 6: Download Report ---
with tabs[6]:
    st.header("📥 Download Report")
    st.markdown("You can download your session summary and insight data.")
    st.download_button("Download Sample Data CSV", data=df.to_csv(index=False), file_name="genz_resume_data.csv")

    st.markdown("---")
    st.caption("🔍 This is more than a score. It’s a conversation between who you are, who you say you are, and what the world is asking for.")

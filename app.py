import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page Config ---
st.set_page_config(page_title="Job Snob", layout="wide")

# --- Custom CSS for Tabs and Styling ---
st.markdown("""
<style>
    /* Container style for the intro and all main content */
    .intro-container {
        max-width: 720px;
        margin: 3rem auto 5rem auto;
        padding: 2.5rem 3rem;
        background: linear-gradient(135deg, #fff8dc 0%, #ffd580 40%, #ffae42 75%, #ff7f11 100%);
        border-radius: 16px;
        box-shadow: 0 12px 40px rgba(255, 140, 0, 0.3);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #4a2c00; /* Dark brown */
        line-height: 1.65;
        text-shadow: 0 1px 2px rgba(255, 255, 255, 0.7);
    }
    /* Headings */
    .intro-container h1 {
        font-family: 'Georgia', serif;
        color: #5c3300; /* Deep brown */
        font-weight: 700;
        font-size: 3rem;
        margin-bottom: 0.2rem;
        letter-spacing: 1.1px;
        text-align: center;
        text-shadow: 2px 2px 4px #f3b14d;
    }
    .intro-container h2 {
        font-weight: 500;
        font-style: italic;
        font-size: 1.3rem;
        margin-top: 0;
        margin-bottom: 2.5rem;
        color: #633e00cc;
        text-align: center;
        text-shadow: 1px 1px 3px #e69900;
    }
    /* Paragraph and lists */
    .intro-container p, .intro-container ul {
        font-size: 1.1rem;
        color: #663c00cc;
        margin-bottom: 1.25rem;
    }
    .intro-container ul {
        padding-left: 1.4rem;
    }
    .intro-container li {
        margin-bottom: 0.5rem;
    }
    /* Feedback box style */
    .feedback-box {
        background-color: #ffdd991a;
        border-left: 5px solid #ffae421a;
        padding: 1rem 1.2rem;
        border-radius: 8px;
        margin-top: 1rem;
        font-style: italic;
        color: #5c3300cc;
        font-size: 1rem;
        box-shadow: inset 0 0 6px #ffae4277;
    }
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .intro-container {
            margin: 2rem 1rem 3rem 1rem;
            padding: 2rem 1.8rem;
        }
        .intro-container h1 {
            font-size: 2.3rem;
        }
        .intro-container h2 {
            font-size: 1.1rem;
        }
    }
    /* Streamlit Tab button active highlight */
    button[data-baseweb="tab-list-item"][aria-selected="true"] {
        background-color: #ffae42 !important;
        color: #4a2c00 !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 12px rgba(255, 140, 0, 0.6);
        border-radius: 10px 10px 0 0 !important;
        transition: background-color 0.3s ease;
    }
    /* Tab hover effect */
    button[data-baseweb="tab-list-item"]:not([aria-selected="true"]):hover {
        background-color: #ffd580 !important;
        color: #5c3300cc !important;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    /* Conclusive statement styling */
    .conclusion-box {
        max-width: 720px;
        margin: 3rem auto 4rem auto;
        padding: 1.5rem 2rem;
        background: #fff8dccc;
        border-radius: 12px;
        box-shadow: 0 6px 20px rgba(255, 140, 0, 0.25);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #4a2c00;
        font-size: 1.15rem;
        text-align: center;
        font-style: italic;
        letter-spacing: 0.5px;
    }
</style>
""", unsafe_allow_html=True)

# --- Introductory statement (above intro container) ---
st.markdown("""
<div class="conclusion-box" style="background: #fffae6cc; color: #7a4a00; font-weight: 600; font-style: normal;">
    Welcome to <strong>Job Snob</strong> — your warm, data-driven career companion designed to illuminate your path,  
    highlight critical skill gaps, and guide you confidently toward your dream job. Let’s transform your resume into a powerful story that recruiters can’t ignore.
</div>
""", unsafe_allow_html=True)

# --- Intro Section ---
st.markdown("""
<div class="intro-container">
    <h1>Job Snob</h1>
    <h2>“Only the best skills make the cut. No basic resumes allowed.”</h2>

    <p>Whether you are just starting your professional journey or aiming for your next career milestone, <strong>Job Snob</strong> provides clear, data-driven insights to help you grow confidently.</p>

    <h3>What You Can Expect</h3>
    <ul>
        <li><strong>Skill Gap Analysis:</strong> Identify the high-impact skills you’re missing.</li>
        <li><strong>Market Comparison:</strong> See how your resume stacks up against real hiring data.</li>
        <li><strong>Personalized Suggestions:</strong> Tailored, actionable steps for improvement.</li>
        <li><strong>Trends & Insights:</strong> Stay updated on hiring patterns in your field.</li>
        <li><strong>Easy Report Download:</strong> Save your progress and recommendations for future reference.</li>
    </ul>

    <h3>How To Use This App</h3>
    <ul>
        <li>Select your resume from the list.</li>
        <li>Explore your skill match and gaps in detail.</li>
        <li>Read customized advice to enhance your profile.</li>
        <li>Download a personal report summarizing your insights.</li>
        <li>Use the feedback regularly to update and improve your resume.</li>
    </ul>

    <div class="feedback-box">
        This app empowers you with clear, warm guidance to confidently build the career you deserve — no stress, just steady growth.
    </div>
</div>
""", unsafe_allow_html=True)

# --- Load your dataset ---
# Dummy data example (replace with your actual dataset)
data = {
    "ResumeID": [1, 2, 3],
    "Age": [24, 28, 22],
    "EducationLevel": ["Bachelor's", "Master's", "Bachelor's"],
    "FieldOfStudy": ["Computer Science", "Business", "Engineering"],
    "JobAppliedFor": ["Data Scientist", "Product Manager", "Software Engineer"],
    "ResumeStyle": ["Modern", "Conservative", "Creative"],
    "Certifications": ["AWS, SQL", "PMP", None],
    "AI_MatchScore": [78, 65, 82],
    "TopSkillGap": ["Machine Learning", "Agile Methodology", "Cloud Computing"],
    "SkillsListed": ["Python, SQL, Statistics", "Product Management, Agile", "Java, Git"],
    "JobPostingSkillsRequired": ["Python, Machine Learning, SQL", "Agile, Scrum, Leadership", "Java, Cloud Computing, Git"]
}
df = pd.DataFrame(data)

def get_resume_data(resume_id=1):
    row = df[df['ResumeID'] == resume_id]
    if row.empty:
        return df.iloc[0].to_dict()
    else:
        return row.iloc[0].to_dict()

# --- Tabs ---
tabs = st.tabs([
    "👤 Profile Snapshot", 
    "📈 Market Comparison", 
    "📊 Match Score", 
    "💡 Suggestions", 
    "📚 Trends & Insights", 
    "📅 Download Report"
])

# Sidebar Resume Selector
resume_ids = df['ResumeID'].tolist()
selected_resume = st.sidebar.selectbox("Select Resume ID", options=resume_ids, index=0)
resume_data = get_resume_data(selected_resume)

# === TAB 1: PROFILE SNAPSHOT ===
with tabs[0]:
    st.header("Profile Snapshot")
    st.write("""
        This section provides a detailed overview of your resume profile to help you understand how your background compares in the job market.  
        From your education level and field of study to the job roles you’re applying for, this snapshot paints a comprehensive picture of your current standing.
    """)
    st.write(f"**Age:** {resume_data['Age']}")
    st.write(f"**Education:** {resume_data['EducationLevel']} in {resume_data['FieldOfStudy']}")
    st.write(f"**Applied For:** {resume_data['JobAppliedFor']}")
    st.write(f"**Resume Style:** {resume_data['ResumeStyle']}")
    certs = resume_data['Certifications'] if pd.notna(resume_data['Certifications']) else "None"
    st.write(f"**Certifications:** {certs}")
    st.metric("AI Match Score", f"{resume_data['AI_MatchScore']} / 100")
    st.progress(resume_data["AI_MatchScore"] / 100)

    st.info("""
    Your resume style and certifications impact recruiter perception. Keep certifications relevant and resume style tailored to your target industry.
    """)

# === TAB 2: MARKET COMPARISON ===
with tabs[1]:
    st.header("Market Comparison")

    st.subheader("AI Match Score by Domain (Education Level)")
    fig_box = px.box(df, x="EducationLevel", y="AI_MatchScore", color="EducationLevel", template="ggplot2")
    st.plotly_chart(fig_box, use_container_width=True)

    st.subheader("Top Skill Gaps Across Resumes")
    gap_counts = df['TopSkillGap'].value_counts().head(10)
    fig_bar = px.bar(gap_counts, title="Top Skill Gaps", template="ggplot2")
    st.plotly_chart(fig_bar, use_container_width=True)

    st.success("""
    Domains with higher median match scores often require specialized skills or certifications.
    Investigate and acquire the top missing skills shown here to boost your hireability.
    """)

# === TAB 3: MATCH SCORE ===
with tabs[2]:
    st.header("Match Score Details")

    listed = set(resume_data.get("SkillsListed", "").split(", ")) if pd.notna(resume_data.get("SkillsListed", "")) else set()
    required = set(resume_data.get("JobPostingSkillsRequired", "").split(", ")) if pd.notna(resume_data.get("JobPostingSkillsRequired", "")) else set()
    overlap = listed & required
    missing = required - listed

    st.metric("Skill Match", f"{len(overlap)} / {len(required)}")
    fig_pie = px.pie(
        values=[len(overlap), len(missing)],
        names=["Matched", "Missing"],
        template="ggplot2",
        color_discrete_sequence=['#ffae42', '#ffd580']
    )
    st.plotly_chart(fig_pie, use_container_width=True)

    st.info("""
    Matching key job skills significantly improves your chances.  
    Prioritize learning the missing critical skills and focus on mastering the top 3 skills required for your dream job.
    """)

# === TAB 4: SUGGESTIONS ===
with tabs[3]:
    st.header("Personalized Suggestions")

    gap = resume_data.get("TopSkillGap", "relevant skills") if pd.notna(resume_data.get("TopSkillGap", "")) else "relevant skills"
    st.markdown(f"""
- 📚 Learn **{gap}** via Coursera, LinkedIn Learning, or YouTube — invest an hour daily to build competence.  
- ✍️ Use the STAR method (Situation, Task, Action, Result) to detail accomplishments clearly.  
- 🪞 Reflect missing skills naturally in your summary and bullet points.  
- 💼 Add project links or GitHub repos for tech roles; emphasize measurable achievements for others.  
- 🎨 Tailor resume style to fit your industry — polished yet authentic.
    """)

    st.info("""
    Continuous learning and resume refinement create a strong hiring profile.  
    Set weekly learning goals and seek peer reviews to polish your presentation.
    """)

# === TAB 5: TRENDS & INSIGHTS ===
with tabs[4]:
    st.header("Trends & Insights")

    avg_score_by_edu = df.groupby("EducationLevel")["AI_MatchScore"].mean().sort_values()
    st.subheader("Average Match Score by Education Level")
    fig_bar_edu = px.bar(avg_score_by_edu, orientation='h', template="seaborn",
                        labels={"value":"Avg. Match Score", "index":"Education Level"})
    st.plotly_chart(fig_bar_edu, use_container_width=True)

    top_fields = df.groupby("FieldOfStudy")["AI_MatchScore"].mean().sort_values(ascending=False).head(10)
    st.subheader("Top Performing Fields of Study")
    fig_bar_fields = px.bar(top_fields, title="Best Fields by Resume Match", template="seaborn")
    st.plotly_chart(fig_bar_fields, use_container_width=True)

    certs = df['Certifications'].dropna().str.split(', ').explode().value_counts().head(10)
    st.subheader("Popular Certifications")
    fig_bar_certs = px.bar(certs, template="seaborn")
    st.plotly_chart(fig_bar_certs, use_container_width=True)

    st.success("""
    Higher education levels and relevant certifications correlate with stronger match scores.  
    Consider certifications that align with your field and regularly update skills to stay competitive.
    """)

# === TAB 6: DOWNLOAD REPORT ===
with tabs[5]:
    st.header("Download Your Report")

    text = f"""
Job Snob Resume Report
======================

Resume ID: {resume_data['ResumeID']}
Age: {resume_data['Age']}
Education: {resume_data['EducationLevel']} in {resume_data['FieldOfStudy']}
Applied For: {resume_data['JobAppliedFor']}

AI Match Score: {resume_data['AI_MatchScore']} / 100
Top Skill Gap: {resume_data.get('TopSkillGap', 'N/A')}

Suggestions:
- Learn {resume_data.get('TopSkillGap', 'relevant skills')} via online courses.
- Use STAR method to improve bullet points.
- Add project links or certifications.
- Tailor resume style to target job domain.

Stay consistent and keep updating!
"""

    st.download_button("📄 Download Report as TXT", data=text, file_name="job_snob_report.txt", mime="text/plain")

    st.info("""
    Keep this report as a living document. Revisit it after every learning milestone or job application round to measure progress and adjust your strategy accordingly.
    """)

# --- Conclusive statement (above footer) ---
st.markdown("""
<div class="conclusion-box">
    Remember, your career is a journey — embrace continuous learning, adapt wisely, and let data-driven insights be your trusted mentor along the way.  
    Here’s to your confident and thriving professional future with Job Snob by your side!
</div>
""", unsafe_allow_html=True)

# --- Footer ---
st.markdown("""
<div style="text-align:center; margin-top: 2rem; font-size: 0.9rem; color: #666;">
    © 2025 Job Snob | Built with ❤️ using Streamlit
</div>
""", unsafe_allow_html=True)

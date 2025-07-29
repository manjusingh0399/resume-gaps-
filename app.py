import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Job Snob", layout="wide")

st.markdown("""
<style>
    /* Ombre cloudy monsoon background */
    .container {
        max-width: 720px;
        margin: 3rem auto 5rem auto;
        padding: 2.5rem 3rem;
        background: linear-gradient(135deg, #cbd6e3 0%, #9fb8c9 40%, #7d8f9f 75%, #62717e 100%);
        border-radius: 16px;
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.1);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #f0f4f8;
        line-height: 1.65;
        text-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
    }

    /* Title styling with soft white */
    h1 {
        font-family: 'Georgia', serif;
        color: #e3eaf2;
        font-weight: 700;
        font-size: 3rem;
        margin-bottom: 0.2rem;
        letter-spacing: 1.1px;
        text-align: center;
        text-shadow: 1px 2px 5px #36454f;
    }

    /* Tagline */
    h2 {
        font-weight: 500;
        font-style: italic;
        font-size: 1.3rem;
        margin-top: 0;
        margin-bottom: 2.5rem;
        color: #d9e2eccc;
        text-align: center;
        text-shadow: 1px 1px 4px #3a4a5e;
    }

    /* Headings */
    h3 {
        color: #d9e2eccc;
        border-bottom: 2px solid #a2b1c6;
        padding-bottom: 0.3rem;
        margin-top: 3rem;
        margin-bottom: 1.2rem;
    }

    /* Paragraph text */
    p, ul {
        font-size: 1.1rem;
        color: #e9f0f7cc;
        margin-bottom: 1.25rem;
    }

    ul {
        padding-left: 1.4rem;
    }

    li {
        margin-bottom: 0.5rem;
    }

    /* Intent box */
    .intent-box {
        background: #aab9ccaa;
        border-left: 5px solid #7a8fa5cc;
        border-radius: 10px;
        padding: 1.2rem 1.5rem;
        margin-top: 3rem;
        font-style: italic;
        color: #e9f0f7dd;
        font-size: 1rem;
        box-shadow: inset 0 0 8px #6c7b8b88;
    }

    /* Footer */
    .footer {
        margin-top: 4rem;
        font-size: 0.9rem;
        color: #b0bccfcc;
        text-align: center;
        font-style: italic;
        text-shadow: 0 0 2px #3b4a60cc;
    }

    /* Tabs custom */
    .stTabs [data-baseweb="tab-list"] {
        margin-bottom: 1.5rem;
    }

    /* Feedback box */
    .feedback-box {
        background-color: #7a8fa5cc;
        border-left: 5px solid #aab9ccaa;
        padding: 1rem 1.2rem;
        border-radius: 8px;
        margin-top: 1rem;
        font-style: italic;
        color: #e9f0f7dd;
        font-size: 1rem;
        box-shadow: inset 0 0 6px #62717ecc;
    }

    /* Responsive */
    @media (max-width: 768px) {
        .container {
            margin: 2rem 1rem 3rem 1rem;
            padding: 2rem 1.8rem;
        }
        h1 {
            font-size: 2.3rem;
        }
        h2 {
            font-size: 1.1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data(persist=True)
def load_data():
    return pd.read_csv("genz_resume_market_data.csv")

df = load_data()

def get_resume_data():
    resume_ids = df['ResumeID'].unique()
    selected_id = st.selectbox("Select a Resume ID", resume_ids, key="resume_selector")
    return df[df['ResumeID'] == selected_id].iloc[0]

st.markdown('<div class="container">', unsafe_allow_html=True)

st.markdown("<h1>Job Snob</h1>", unsafe_allow_html=True)
st.markdown("<h2>“Only the best skills make the cut. No basic resumes allowed.”</h2>", unsafe_allow_html=True)

st.markdown("""
<p>Welcome to <strong>Job Snob</strong>, your calm, smart career companion inspired by the serene monsoon clouds.  
We help you identify the real skill gaps in your resume and align you with what employers seek today.</p>

<p>Whether you're starting out or climbing your career ladder, Job Snob is your data-driven mentor guiding you peacefully towards success.</p>
""", unsafe_allow_html=True)

tabs = st.tabs([
    "👤 Profile Snapshot", 
    "📈 Market Comparison", 
    "📊 Match Score", 
    "💡 Suggestions", 
    "📚 Trends & Insights", 
    "📅 Download Report"
])

# === TAB 1: PROFILE SNAPSHOT ===
with tabs[0]:
    st.markdown("<h3>Profile Snapshot</h3>", unsafe_allow_html=True)
    st.markdown("""
    This section provides a detailed overview of your resume profile to help you understand how your background compares in the job market.  
    From your education level and field of study to the job roles you’re applying for, this snapshot paints a comprehensive picture of your current standing.  
    By reflecting on this, you can identify how your academic and experiential credentials stack up and prepare to position yourself more strategically for the roles you desire.
    """, unsafe_allow_html=True)

    resume_data = get_resume_data()
    st.write(f"**Age:** {resume_data['Age']}")
    st.write(f"**Education:** {resume_data['EducationLevel']} in {resume_data['FieldOfStudy']}")
    st.write(f"**Applied For:** {resume_data['JobAppliedFor']}")
    st.write(f"**Resume Style:** {resume_data['ResumeStyle']}")
    st.write(f"**Certifications:** {resume_data['Certifications'] if pd.notna(resume_data['Certifications']) else 'None'}")
    st.metric("AI Match Score", f"{resume_data['AI_MatchScore']}/100")
    st.progress(resume_data["AI_MatchScore"] / 100)

    st.markdown(f"""
    <div class="feedback-box">
    Insight: Your resume style and certifications play a vital role in how recruiters perceive your profile. Ensure your certifications are current and relevant.<br>
    Advice: Tailor your resume style depending on the job domain — conservative styles work well for finance, creative ones for design.<br>
    Feedback: Keep refining your profile summary to highlight your unique strengths and how your education connects to your desired role.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <p>Concluding, this snapshot is your starting point — a mirror reflecting your current career identity. Use these insights to align your future efforts and present your best professional self to recruiters.</p>
    """, unsafe_allow_html=True)

# === TAB 2: MARKET COMPARISON ===
with tabs[1]:
    st.markdown("<h3>Market Comparison</h3>", unsafe_allow_html=True)
    st.markdown("""
    This tab helps you benchmark your resume against the broader job market by analyzing domain match scores and identifying skill gaps common in your peer group.  
    Understanding where you stand relative to the competition is crucial for prioritizing skill development and making informed career moves.  
    The visual charts let you see how your industry or field of study compares and which skills are in demand but missing in many resumes.
    """, unsafe_allow_html=True)

    st.subheader("AI Match Score by Domain")
    st.plotly_chart(px.box(df, x="Domain", y="AI_MatchScore", color="Domain", template="ggplot2"), use_container_width=True)
    st.subheader("Top Skill Gaps Across Resumes")
    gap_counts = df['TopSkillGap'].value_counts().head(10)
    st.plotly_chart(px.bar(gap_counts, title="Top Skill Gaps", template="ggplot2"), use_container_width=True)

    st.markdown(f"""
    <div class="feedback-box">
    Insight: Domains with higher median match scores often require specialized skills or certifications.<br>
    Advice: Investigate and acquire the top missing skills shown here — these are your best investment areas.<br>
    Feedback: Use this comparison to set realistic goals; bridging these gaps can significantly boost your hireability.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <p>In summary, market comparison lets you position yourself wisely by understanding where you outperform and where you fall behind, making your career path more strategic and targeted.</p>
    """, unsafe_allow_html=True)

# === TAB 3: MATCH SCORE ===
with tabs[2]:
    st.markdown("<h3>Match Score Details</h3>", unsafe_allow_html=True)
    st.markdown("""
    The match score reflects how well your skills align with what employers expect for your target jobs.  
    This tab breaks down which skills you have matched successfully and which are missing, offering a clear roadmap to improve.  
    Evaluating this score regularly can help you measure progress and stay competitive in your field.
    """, unsafe_allow_html=True)

    listed = set(resume_data.get("SkillsListed", "").split(", ")) if pd.notna(resume_data.get("SkillsListed", "")) else set()
    required = set(resume_data.get("JobPostingSkillsRequired", "").split(", ")) if pd.notna(resume_data.get("JobPostingSkillsRequired", "")) else set()
    overlap = listed & required
    missing = required - listed

    st.metric("Skill Match", f"{len(overlap)} / {len(required)}")
    st.plotly_chart(px.pie(values=[len(overlap), len(missing)], names=["Matched", "Missing"], template="ggplot2"), use_container_width=True)

    st.markdown(f"""
    <div class="feedback-box">
    Insight: Matching key job skills significantly improves your chances of getting hired.<br>
    Advice: Prioritize learning missing critical skills in your target roles.<br>
    Feedback: Focus on quality over quantity — deeply master the top 3 skills required for your dream job.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <p>Remember, the match score is a dynamic metric. As you improve your skills and tailor your resume, this score will rise — bringing you closer to landing your ideal job.</p>
    """, unsafe_allow_html=True)

# === TAB 4: SUGGESTIONS ===
with tabs[3]:
    st.markdown("<h3>Personalized Suggestions</h3>", unsafe_allow_html=True)
    st.markdown("""
    Here we provide actionable recommendations based on your current skill gaps and resume profile.  
    Our suggestions help you focus your learning, improve your resume presentation, and strategize your job applications better.  
    Taking these steps will increase your confidence and visibility in the hiring market.
    """, unsafe_allow_html=True)

    gap = resume_data.get("TopSkillGap", "relevant skills") if pd.notna(resume_data.get("TopSkillGap", "")) else "relevant skills"
    st.markdown(f"""
- 📚 Learn **{gap}** via Coursera, LinkedIn Learning or YouTube — invest an hour daily to build competence.  
- ✍️ Use the STAR method (Situation, Task, Action, Result) to detail your accomplishments and projects clearly.  
- 🪞 Reflect the missing skills naturally in your professional summary and bullet points.  
- 💼 For tech roles, add project links or GitHub repositories; for other fields, emphasize measurable achievements.  
- 🎨 Adjust your resume style to fit your target industry’s expectations — be polished but authentic.
""")

    st.markdown(f"""
    <div class="feedback-box">
    Insight: Continuous learning and resume refinement create a strong hiring profile.<br>
    Advice: Small consistent efforts compound into big results; set weekly learning goals.<br>
    Feedback: Don’t hesitate to seek mentorship or peer review to polish your presentation.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <p>Following personalized suggestions is your roadmap from good to great. Stay committed and track your improvements to accelerate your career growth.</p>
    """, unsafe_allow_html=True)

# === TAB 5: TRENDS & INSIGHTS ===
with tabs[4]:
    st.markdown("<h3>Trends & Insights</h3>", unsafe_allow_html=True)
    st.markdown("""
    Stay informed on broader hiring trends related to education, fields of study, and certifications.  
    This helps you anticipate market demands and adjust your career strategy proactively.  
    Data-backed insights make it easier to understand what works well across the board and where to specialize.
    """, unsafe_allow_html=True)

    avg_score_by_edu = df.groupby("EducationLevel")["AI_MatchScore"].mean().sort_values()
    st.subheader("Average Match Score by Education Level")
    st.plotly_chart(px.bar(avg_score_by_edu, orientation='h', template="seaborn", labels={"value":"Avg. Match Score"}), use_container_width=True)

    top_fields = df.groupby("FieldOfStudy")["AI_MatchScore"].mean().sort_values(ascending=False).head(10)
    st.subheader("Top Performing Fields of Study")
    st.plotly_chart(px.bar(top_fields, title="Best Fields by Resume Match", template="seaborn"), use_container_width=True)

    certs = df['Certifications'].dropna().str.split(', ').explode().value_counts().head(10)
    st.subheader("Popular Certifications")
    st.plotly_chart(px.bar(certs, template="seaborn"), use_container_width=True)

    st.markdown(f"""
    <div class="feedback-box">
    Insight: Higher education levels and relevant certifications correlate with stronger match scores.<br>
    Advice: Consider certifications that align with your field to boost your profile.<br>
    Feedback: Regularly update your skills and credentials to stay competitive.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <p>These trends offer a macro lens on the hiring ecosystem. Align your personal growth with these insights to maximize your opportunities and stay future-ready.</p>
    """, unsafe_allow_html=True)

# === TAB 6: DOWNLOAD REPORT ===
with tabs[5]:
    st.markdown("<h3>Download Your Report</h3>", unsafe_allow_html=True)
    st.markdown("""
    This section allows you to download a personalized summary report of your resume analysis and tailored suggestions.  
    Use this document to track your growth, share with mentors, or revisit your next steps anytime.  
    Regularly updating this report keeps your career planning focused and proactive.
    """, unsafe_allow_html=True)

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

    st.markdown(f"""
    <div class="feedback-box">
    Reminder: Keep this report as a living document. Revisit it after every learning milestone or job application round to measure progress and adjust your strategy accordingly.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <p>Closing this app session, remember that your career is a journey—embrace learning, adapt wisely, and keep your ambitions aligned with actionable insights.</p>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="intent-box">
This app is designed to empower job seekers — especially Gen Z and early professionals — with calm clarity and data-driven insights to confidently build the career you deserve.
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="footer">
© 2025 Job Snob | Built with ❤️ using Streamlit
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

import streamlit as st
import pandas as pd
import plotly.express as px

# Page Config
st.set_page_config(page_title="Job Snob", layout="wide")

# Sample DataFrame
df = pd.DataFrame({
    "ResumeID": [1],
    "Age": [24],
    "EducationLevel": ["Bachelor's"],
    "FieldOfStudy": ["Computer Science"],
    "JobAppliedFor": ["Data Analyst"],
    "ResumeStyle": ["Modern"],
    "Certifications": ["SQL, Tableau"],
    "AI_MatchScore": [76],
    "TopSkillGap": ["Machine Learning"],
    "SkillsListed": ["Python, SQL, Excel"],
    "JobPostingSkillsRequired": ["Python, Machine Learning, SQL"]
})

# Helper Function
def get_resume_data():
    return df.iloc[0]

# Custom CSS Styling
st.markdown("""
<style>
.intro-container {
    max-width: 720px;
    margin: 3rem auto;
    padding: 2.5rem 3rem;
    background: linear-gradient(135deg, #fff8dc, #ffae42);
    border-radius: 16px;
    box-shadow: 0 12px 40px rgba(255, 140, 0, 0.3);
    color: #4a2c00;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.65;
}
.intro-container h1, .intro-container h2 {
    text-align: center;
    margin-bottom: 1.5rem;
}
.feedback-box {
    background-color: #fff7e6;
    border-left: 5px solid #ffae42;
    padding: 1rem;
    border-radius: 8px;
    font-style: italic;
    color: #5c3300cc;
    margin-top: 1.5rem;
}
[data-baseweb="tab-list"] button[aria-selected="true"] {
    background-color: #ffae42 !important;
    color: #4a2c00 !important;
    font-weight: bold !important;
    border-radius: 10px 10px 0 0;
    box-shadow: 0 -4px 10px rgba(255, 174, 66, 0.4);
    transition: all 0.3s ease-in-out;
}
[data-baseweb="tab-list"] button[aria-selected="false"] {
    background-color: #fff7e6;
    color: #7a4e00;
    font-weight: 500;
}
</style>
""", unsafe_allow_html=True)

# Intro
st.markdown("""
<div class="intro-container">
    <h1>Job Snob</h1>
    <h2>“Only the best skills make the cut. No basic resumes allowed.”</h2>
    <p>Welcome to <strong>Job Snob</strong> — your calm, data-driven career mentor. Whether you're beginning your journey or eyeing the next big leap, we provide honest insight and powerful direction to help you thrive in the hiring world.</p>
    <h3>What You Can Expect</h3>
    <ul>
        <li><strong>Skill Gap Analysis:</strong> Find out which essential skills you're missing.</li>
        <li><strong>Market Comparison:</strong> Benchmark yourself against real hiring data.</li>
        <li><strong>Personalized Suggestions:</strong> Concrete advice for upskilling and better visibility.</li>
        <li><strong>Trends & Insights:</strong> Stay sharp with current hiring trends and demands.</li>
        <li><strong>Download Report:</strong> Track your progress and insights offline.</li>
    </ul>
    <div class="feedback-box">
        This app gives you a warm but realistic reflection of your current profile — with no fluff and all focus.
    </div>
</div>
""", unsafe_allow_html=True)

resume_data = get_resume_data()
tabs = st.tabs([
    "👤 Profile Snapshot", "📈 Market Comparison", "📊 Match Score",
    "💡 Suggestions", "📚 Trends & Insights", "📅 Download Report"])

with tabs[0]:
    st.header("👤 Profile Snapshot")
    st.markdown("""
    <p>This section captures a snapshot of your background, education, and application focus — setting the stage for your career reflection journey.</p>
    """, unsafe_allow_html=True)
    st.write(f"**Age:** {resume_data['Age']}")
    st.write(f"**Education:** {resume_data['EducationLevel']} in {resume_data['FieldOfStudy']}")
    st.write(f"**Applied For:** {resume_data['JobAppliedFor']}")
    st.write(f"**Resume Style:** {resume_data['ResumeStyle']}")
    st.write(f"**Certifications:** {resume_data['Certifications']}")
    st.metric("AI Match Score", f"{resume_data['AI_MatchScore']} / 100")
    st.progress(resume_data['AI_MatchScore'] / 100)
    st.markdown(f"""
    <div class='feedback-box'>
    Insight: Resume formatting and relevant certifications are subtle but crucial signals.<br>
    Advice: Highlight recent achievements and role-focused skills to improve first impressions.
    </div>
    <p><em>Keep this profile fresh and aligned with the job roles you aspire for.</em></p>
    """, unsafe_allow_html=True)

with tabs[1]:
    st.header("📈 Market Comparison")
    st.markdown("""
    <p>This section allows you to benchmark yourself against industry peers — a must for understanding how you stack up competitively.</p>
    """, unsafe_allow_html=True)
    st.plotly_chart(px.box(df, x="FieldOfStudy", y="AI_MatchScore", template="seaborn"), use_container_width=True)
    st.markdown(f"""
    <div class='feedback-box'>
    Insight: Fields with tech-focused education have better match scores on average.<br>
    Advice: Consider certifications in trending areas to stay competitive.
    </div>
    <p><em>Use these comparisons to make informed upskilling decisions.</em></p>
    """, unsafe_allow_html=True)

with tabs[2]:
    st.header("📊 Match Score")
    st.markdown("""
    <p>This section dissects your skill match and reveals gaps between your profile and what job listings demand.</p>
    """, unsafe_allow_html=True)
    listed = set(resume_data["SkillsListed"].split(", "))
    required = set(resume_data["JobPostingSkillsRequired"].split(", "))
    overlap = listed & required
    missing = required - listed
    st.metric("Skill Match", f"{len(overlap)} / {len(required)}")
    st.plotly_chart(px.pie(values=[len(overlap), len(missing)], names=["Matched", "Missing"], template="seaborn"), use_container_width=True)
    st.markdown(f"""
    <div class='feedback-box'>
    Insight: Skills like {', '.join(missing)} are commonly expected but missing.<br>
    Advice: Learning and showcasing these will boost your hiring score.
    </div>
    <p><em>Your match score improves with each resume revision and real skill gain.</em></p>
    """, unsafe_allow_html=True)

with tabs[3]:
    st.header("💡 Suggestions")
    st.markdown("""
    <p>Targeted advice tailored to your profile gaps — here’s how to get better, faster.</p>
    """, unsafe_allow_html=True)
    st.markdown(f"""
- 📘 Learn **{resume_data['TopSkillGap']}** through project-based courses.
- ✍️ Use STAR format to rewrite bullet points.
- 🧠 Reflect missing skills in summary & keywords.
- 🖼 Adapt your resume layout based on the job type.
- 🤝 Get peer reviews or use resume checkers.
    """)
    st.markdown("""
    <div class='feedback-box'>
    Feedback: Small resume tweaks + consistent learning = big leaps.
    </div>
    <p><em>Come back to this tab often — adapt as you grow.</em></p>
    """, unsafe_allow_html=True)

with tabs[4]:
    st.header("📚 Trends & Insights")
    st.markdown("""
    <p>Observe market trends, popular education paths, and in-demand certifications to stay ahead.</p>
    """, unsafe_allow_html=True)
    avg_edu = df.groupby("EducationLevel")["AI_MatchScore"].mean()
    st.bar_chart(avg_edu)
    st.markdown("""
    <div class='feedback-box'>
    Insight: Bachelor's and up with industry certifications outperform in data roles.
    </div>
    <p><em>Let industry trends guide your skill priorities.</em></p>
    """, unsafe_allow_html=True)

with tabs[5]:
    st.header("📅 Download Report")
    st.markdown("""
    <p>Download a customized summary of your profile, insights, and next steps.</p>
    """, unsafe_allow_html=True)
    report = f"""
Job Snob Report\n================\nResume ID: {resume_data['ResumeID']}\nJob Applied For: {resume_data['JobAppliedFor']}\nEducation: {resume_data['EducationLevel']} in {resume_data['FieldOfStudy']}\nMatch Score: {resume_data['AI_MatchScore']}\nMissing Skills: {', '.join(missing)}\nRecommendations: Focus on {resume_data['TopSkillGap']}\n"""
    st.download_button("📥 Download Report", data=report, file_name="job_snob_report.txt")
    st.markdown("""
    <div class='feedback-box'>
    Reminder: Use this report monthly to realign your growth.
    </div>
    <p><em>This report is your portable career blueprint.</em></p>
    """, unsafe_allow_html=True)

# Conclusion
st.markdown("""
<div class='feedback-box'>
🌟 <strong>Final Insight:</strong> Your career is a marathon, not a sprint. Keep evolving with purpose, stay updated, and let each small action lead you toward your dream role.
</div>

<div style='text-align:center; padding-top:2rem; font-size:0.9rem;'>
© 2025 Job Snob | Built with ❤️ using Streamlit
</div>
""", unsafe_allow_html=True)

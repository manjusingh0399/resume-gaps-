import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Resume vs Reality", layout="wide")

# Global Footer function
def footer():
    st.markdown(
        """
        <style>
        .footer {
            font-size: 0.8rem;
            text-align: center;
            margin-top: 2rem;
            color: #999;
            font-style: italic;
        }
        </style>
        <div class="footer">
        This is more than a score. It’s a conversation between who you are, who you say you are, and what the world is asking for. Data doesn’t decide your worth — but it can help you get heard.
        </div>
        """, unsafe_allow_html=True)

# Sidebar - page selection
page = st.sidebar.selectbox(
    "Navigate pages",
    [
        "Home",
        "Dashboard",
        "Resume Analyzer",
        "Ideal Resume Library",
        "Insights & Trends",
        "Career Mentor",
        "Download Report"
    ]
)

# Page 1: Home
if page == "Home":
    st.title("Resume vs Reality: Which Skills Actually Help You Get Hired?")
    monologues = [
        "We all build resumes hoping they reflect our potential. But behind every hiring decision lies a pattern…",
        "We're the most connected generation, yet the most confused about what really matters…",
        "Your resume says Python, Canva, and leadership. But are they looking for SQL, Excel, and grit?"
    ]
    selected_mono = st.selectbox("Reflection", monologues)
    st.markdown("### Let's start your journey towards a resume that truly matches the market demands.")
    if st.button("Get Started"):
        st.experimental_rerun()
    # Placeholder for hero image or animation
    st.image("https://cdn.pixabay.com/photo/2017/01/31/22/35/resume-2028276_1280.png", use_column_width=True)

# Page 2: Dashboard
elif page == "Dashboard":
    st.header("Dashboard / Explore Trends")

    # Sidebar Filters
    domain_filter = st.sidebar.multiselect("Domain", ["Technology", "Business", "Design", "Finance", "Healthcare"])
    job_filter = st.sidebar.multiselect("Job Applied For", ["Frontend Developer", "Marketing Analyst", "Visual Designer", "Financial Analyst", "Medical Writer"])
    style_filter = st.sidebar.multiselect("Resume Style", ["ATS-Friendly", "Visual", "Infographic", "Minimalist"])
    score_filter = st.sidebar.slider("AI Match Score", 0, 100, (50, 100))
    status_filter = st.sidebar.radio("Status", ["All", "Shortlisted", "Hired"])

    # Placeholder Data (replace with your CSV loading + filtering)
    skills = ["JavaScript", "React", "SQL", "Excel", "Python", "Canva", "Figma", "Photoshop", "Clinical Trials"]
    common_skills = np.random.randint(20, 80, len(skills))
    missing_skills = np.random.randint(0, 50, len(skills))

    # Bar Chart: Common vs Missing Skills
    df_skills = pd.DataFrame({
        "Skill": skills*2,
        "Count": np.concatenate([common_skills, missing_skills]),
        "Type": ["Common"]*len(skills) + ["Missing"]*len(skills)
    })

    fig_bar = px.bar(df_skills, x="Skill", y="Count", color="Type", barmode="group",
                     title="Most Common vs Most Missing Skills")
    st.plotly_chart(fig_bar, use_container_width=True)

    # Radar Chart Placeholder
    categories = ["Technical", "Soft Skills", "Certifications", "Experience", "Traits"]
    resume_vals = [80, 70, 60, 75, 50]
    job_vals = [85, 65, 70, 80, 55]
    radar_df = pd.DataFrame(dict(
        r=resume_vals+job_vals,
        theta=categories*2,
        group=["Resume"]*len(categories) + ["Job"]*len(categories)
    ))
    fig_radar = px.line_polar(radar_df, r='r', theta='theta', color='group', line_close=True,
                              title="Resume vs Job Skill Match Radar Chart")
    st.plotly_chart(fig_radar, use_container_width=True)

    # Pie Chart: Shortlisted vs Hired (dummy)
    pie_data = pd.DataFrame({
        "Status": ["Shortlisted", "Hired", "Not Selected"],
        "Count": [120, 60, 90]
    })
    fig_pie = px.pie(pie_data, values='Count', names='Status', title="Shortlisted vs Hired Ratios")
    st.plotly_chart(fig_pie, use_container_width=True)

    # Histogram: AI Match Score Distribution (dummy)
    scores = np.random.normal(75, 15, 300)
    fig_hist = px.histogram(scores, nbins=30, title="AI Match Score Distribution")
    st.plotly_chart(fig_hist, use_container_width=True)

    # Insights
    st.markdown("### Insights & Narratives")
    st.markdown("""
    - 84% of resumes for ‘Frontend Developer’ mention JavaScript. But only 42% of job listings prioritize it.<br>
    - Certifications help only when targeted. Generic certs didn’t improve hiring rates in creative fields.<br>
    - AI Match Scores above 78 had 65% shortlist chances. But visual resumes lowered ATS compatibility.<br>
    """, unsafe_allow_html=True)

    st.markdown("#### Resume Style vs Hiring Table")
    style_table = pd.DataFrame({
        "Resume Style": ["ATS-Friendly", "Visual"],
        "Avg. Score": [76, 68],
        "Hired (%)": [35, 21]
    })
    st.table(style_table)

# Page 3: Resume Analyzer
elif page == "Resume Analyzer":
    st.header("Resume Analyzer")

    uploaded_file = st.file_uploader("Upload your resume (.txt or .docx)", type=['txt', 'docx'])
    if uploaded_file:
        if uploaded_file.type == "text/plain":
            resume_text = uploaded_file.read().decode("utf-8")
        else:
            import docx
            doc = docx.Document(uploaded_file)
            resume_text = "\n".join([p.text for p in doc.paragraphs])
        st.subheader("Resume Text Preview")
        st.write(resume_text)
    else:
        resume_text = st.text_area("Or paste your resume text here:")

    # Dummy skill extraction
    import re
    skills_extracted = []
    if resume_text:
        # Simple pattern for skills separated by commas or new lines
        skills_extracted = re.findall(r'\b\w+\b', resume_text)
        skills_extracted = list(set(skills_extracted))  # unique

    st.markdown(f"**Extracted Skills ({len(skills_extracted)}):** {', '.join(skills_extracted[:15])}...")

    # Job profile selection for comparison
    job_profile = st.selectbox("Select Job Profile to Compare", ["Frontend Developer", "Marketing Analyst", "Visual Designer", "Financial Analyst", "Medical Writer"])

    # Dummy match % and score
    match_percent = np.random.randint(40, 90)
    ai_score = np.random.uniform(60, 95)

    st.metric("Skill Match %", f"{match_percent}%")
    st.metric("AI Match Score", f"{ai_score:.1f}")

    # Color-coded chart placeholder
    st.bar_chart({
        "Matched Skills": [match_percent],
        "Missing Skills": [100 - match_percent]
    })

# Page 4: Ideal Resume Library
elif page == "Ideal Resume Library":
    st.header("Ideal Resume Library")

    with st.expander("Data Analyst – High Match"):
        st.write("This resume highlights key data skills including SQL, Python, and Tableau.")
        st.download_button("Download Sample Resume", "Sample data analyst resume content", file_name="data_analyst_resume.txt")

    with st.expander("Marketing Analyst – Missed SQL"):
        st.write("This resume needs improvement in SQL and Google Ads.")
        st.download_button("Download Sample Resume", "Sample marketing analyst resume content", file_name="marketing_analyst_resume.txt")

    with st.expander("Creative Resume – Not Shortlisted"):
        st.write("This creative resume lacks technical skills required.")
        st.download_button("Download Sample Resume", "Sample creative resume content", file_name="creative_resume.txt")

# Page 5: Insights & Trends
elif page == "Insights & Trends":
    st.header("Insights & Trends")

    # Sample tables
    overused_skills = pd.DataFrame({
        "Skill": ["JavaScript", "Excel", "Photoshop"],
        "Count": [150, 130, 110]
    })

    missing_skills = pd.DataFrame({
        "Skill": ["React", "SQL", "Clinical Trials"],
        "Count": [40, 50, 30]
    })

    trait_vs_score = pd.DataFrame({
        "Gen Z Trait": ["Digital Native", "Side Hustler", "Fast Learner"],
        "Avg Match Score": [75, 70, 80]
    })

    st.subheader("Most Overused Skills")
    st.table(overused_skills)

    st.subheader("Top Missing Skills")
    st.table(missing_skills)

    st.subheader("Gen Z Trait Tags vs Match Scores")
    st.table(trait_vs_score)

# Page 6: Career Mentor
elif page == "Career Mentor":
    st.header("Career Mentor")

    user_skills = st.text_area("Enter your current skills (comma separated):")
    domain_goal = st.selectbox("Domain you're aiming for", ["Technology", "Business", "Design", "Finance", "Healthcare"])

    if st.button("Get Career Suggestions"):
        if not user_skills.strip():
            st.error("Please enter your skills.")
        else:
            skills_list = [s.strip() for s in user_skills.split(",")]

            # Dummy recommendations and confidence meter
            st.write(f"You are closest to roles in **{domain_goal}** domain.")
            st.write(f"Skill gap: Add SQL, Leadership, Communication")

            conf_score = np.random.randint(50, 95)
            emoji = "🔥" if conf_score > 80 else "🟢" if conf_score > 60 else "🔴"
            st.metric("Confidence Meter", f"{conf_score} % {emoji}")

# Page 7: Download Report
elif page == "Download Report":
    st.header("Download Your Report")

    st.write("Download a summary of your resume analysis and career insights.")

    # Dummy CSV download
    sample_data = pd.DataFrame({
        "Skill": ["Python", "SQL", "Excel"],
        "Match": [True, False, True]
    })

    csv = sample_data.to_csv(index=False).encode('utf-8')
    st.download_button(label="Download CSV Report", data=csv, file_name='resume_report.csv', mime='text/csv')

footer()

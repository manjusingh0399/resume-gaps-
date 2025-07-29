import streamlit as st
import pandas as pd
import plotly.express as px

# Page Config
st.set_page_config(page_title="Job Snob", layout="wide")

# Minimal Custom Styling with horizontal centering
st.markdown("""
    <style>
        /* Center container */
        .centered-content {
            max-width: 700px;
            margin-left: auto;
            margin-right: auto;
            padding: 2rem 1rem;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: #333333;
        }
        h1 {
            font-family: 'Georgia', serif;
            color: #6A0DAD;
            margin-bottom: 0.2rem;
            text-align: center;
        }
        h3 {
            color: #ff4da6;
            margin-top: 0;
            font-weight: normal;
            font-style: italic;
            text-align: center;
        }
        p {
            font-size: 1.1rem;
            line-height: 1.5;
            margin-top: 1rem;
            margin-bottom: 1rem;
            text-align: center;
        }
        ul {
            margin-top: 0.5rem;
            margin-bottom: 1rem;
            padding-left: 1.2rem;
            max-width: 500px;
            margin-left: auto;
            margin-right: auto;
        }
        li {
            margin-bottom: 0.4rem;
        }
        .intent {
            background-color: #fce4f0;
            border-left: 5px solid #ff4da6;
            padding: 1rem 1.2rem;
            border-radius: 5px;
            margin-top: 2rem;
            font-style: italic;
            color: #6a0d6a;
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
            text-align: center;
        }
        .footer {
            font-size: 0.9rem;
            color: #888;
            margin-top: 3rem;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# Wrap all content inside div.centered-content to center horizontally
st.markdown('<div class="centered-content">', unsafe_allow_html=True)

# Title and Tagline
st.markdown("<h1>Job Snob</h1>", unsafe_allow_html=True)
st.markdown("<h3>“Only the best skills make the cut. No basic resumes allowed.”</h3>", unsafe_allow_html=True)

# Introduction
st.markdown("""
Welcome to **Job Snob**, your smart career companion designed to help you uncover the real skill gaps in your resume and align it with what employers are actively looking for.

Whether you’re a fresh graduate or an early professional, this tool acts like a career mentor — providing clear insights, personalized feedback, and actionable advice to help you stand out in today's competitive job market.
""")

# What to Expect
st.markdown("""
### What You Can Expect

- **Skill Gap Analysis:** Discover which key skills you’re missing that employers value most.  
- **Market Comparison:** See how your resume stacks up against real hiring data.  
- **Personalized Suggestions:** Get tailored recommendations for improving your profile.  
- **Trends & Insights:** Stay updated with hiring trends in your field.  
- **Easy Report Download:** Summarize your analysis and advice in a shareable report.
""")

# How To Use
st.markdown("""
### How To Use This App

1. **Select your resume** from the available options.  
2. **Explore the skill match and gaps** compared to the job market.  
3. **Review personalized tips** and suggested next steps.  
4. **Download your tailored report** to keep track and share your progress.  
5. **Repeat regularly** as you grow your skills and update your resume.
""")

# Intent Behind Making It
st.markdown("""
<div class="intent">
This app was created to empower job seekers — especially Gen Z and early professionals — with data-driven clarity about what employers want today.  
Our goal is to move beyond generic advice and provide you with **real, actionable insights** so you can confidently build the career you deserve.
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
© 2025 Job Snob | Built with ❤️ using Streamlit
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True) 

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

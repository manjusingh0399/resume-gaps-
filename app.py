import streamlit as st
import plotly.express as px
import pandas as pd

# Load resume dataset
@st.cache_data

def load_data():
    return pd.read_csv("resumegaps_dataset.csv")  # Update this with your actual dataset filename

resume_df = load_data()

# Page Config
st.set_page_config(page_title="JobSnob: Resume vs Reality", layout="wide")

# Custom CSS for Styling
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

        html, body, [class*="css"]  {
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #fff7c0, #ffe6b3, #ffd27f);
        }

        .stApp {
            background: linear-gradient(135deg, #FFF9E3, #FFE3AC);
        }

        .job-snob-hero {
            background: linear-gradient(to right, #FFD700, #FFA500);
            border-radius: 25px;
            padding: 3rem;
            text-align: center;
            color: white;
            box-shadow: 0 10px 30px rgba(255, 165, 0, 0.2);
            animation: fadeIn 1.5s ease-in-out;
        }

        .job-snob-title {
            font-size: 3.5rem;
            font-weight: 800;
            margin-bottom: 0.5rem;
            letter-spacing: -1px;
        }

        .job-snob-tagline {
            font-size: 1.5rem;
            font-weight: 500;
            font-style: italic;
            margin-bottom: 1rem;
        }

        .job-snob-subtext {
            font-size: 1.1rem;
            font-weight: 400;
            max-width: 700px;
            margin: 0 auto;
            opacity: 0.95;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .stButton>button {
            background: linear-gradient(to right, #FFDD00, #FFA500);
            color: white;
            border-radius: 12px;
            padding: 0.6rem 1.2rem;
            font-weight: 600;
            box-shadow: 0 4px 12px rgba(255, 165, 0, 0.4);
        }
    </style>
""", unsafe_allow_html=True)

# Resume Selector
st.sidebar.header("🔍 Choose Resume Profile")
selected_resume = st.sidebar.selectbox("Select a Resume ID:", resume_df["ResumeID"].unique())
user_data = resume_df[resume_df["ResumeID"] == selected_resume].squeeze()

# Tabs Setup
tabs = st.tabs(["🏠 Welcome", "👤 Profile Snapshot", "📊 Market Comparison", "🎯 Match Score", "💡 Suggestions", "📚 Insights"])

# Welcome Tab
with tabs[0]:
    st.markdown("""
    <div class="job-snob-hero">
        <div class="job-snob-title">💼 JobSnob</div>
        <div class="job-snob-tagline">“We judge. But it’s character development.”</div>
        <div class="job-snob-subtext">Let’s glow up your resume and match it to what the job market actually wants.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    ### 👋 Welcome to Your Career Glow-Up
    You're not just here to upload a resume — you're here to understand your standing, identify hidden gaps, and align your strengths with roles that actually value you.

    This app compares your resume data to real hiring trends, job market signals, and peer-level benchmarks. Think of it as your brutally honest (but stylish) career mirror.

    ---
    
    #### Most resumes tell stories. We make sure yours tells the right one — for the jobs you actually want.

    ✨ Use the sidebar to select your resume and start exploring your profile snapshot.
    """)

# Profile Snapshot Tab
with tabs[1]:
    st.header("👤 Profile Snapshot")
    st.markdown("""
    Here's your extracted profile:
    """)
    st.json(user_data.to_dict())

    st.info("Most candidates either overshare or undershare. This will help you strike the perfect balance.")
    st.success("Tip: Use keywords from the job descriptions you’re targeting!")

# Market Comparison Tab
with tabs[2]:
    st.header("📊 Market Comparison")
    st.markdown("""
    Here's how your profile compares to what employers in your field are really asking for. 
    We’ll chart your skillset against hiring trends, demand data, and peer candidates.
    """)

    # Example chart
    skills = ["Python", "Excel", "SQL", "Power BI", "Communication"]
    user_scores = [user_data.get(skill, 0) for skill in skills]
    market_avg = [80, 75, 70, 60, 85]
    df_compare = pd.DataFrame({
        "Skill": skills,
        "You": user_scores,
        "Market Avg": market_avg
    })
    fig = px.bar(df_compare, x='Skill', y=['You', 'Market Avg'], barmode='group', title='Your Skills vs Market Demand')
    st.plotly_chart(fig, use_container_width=True)
    st.warning("If you're below average in key skills, that's your upgrade area!")

# Match Score Tab
with tabs[3]:
    st.header("🎯 Match Score")
    st.markdown("""
    Based on your resume and the job roles you're aiming for, here's your personalized match score.
    It helps you understand where you stand and what you can improve.
    """)

    score = int(user_data.get("MatchScore", 72))
    st.metric("Match Score", f"{score}%")

    if score >= 80:
        st.success("You're closely aligned with top industry requirements. Great job!")
    elif score >= 60:
        st.info("You're on the right track. A few enhancements will help you shine.")
    else:
        st.warning("Let's work on boosting your core skills for better alignment.")

# Suggestions Tab
with tabs[4]:
    st.header("💡 Suggestions & Role Fit")
    st.markdown("""
    These are some career roles where your current skillset already gives you a headstart. Let’s bridge the rest!
    """)
    st.markdown("""
    - 📌 **Data Analyst** — Needs deeper SQL & Power BI
    - 📌 **Marketing Associate** — You’re a great fit! Emphasize your communication & project work.
    - 📌 **Business Analyst** — Add 1-2 certifications in process mapping or Excel modeling
    """)
    st.success("Remember: Roles evolve, and so should you. Keep learning!")

# Insights Tab
with tabs[5]:
    st.header("📚 Career Insights & Trends")
    st.markdown("""
    Stay ahead with curated insights about hiring trends, resume best practices, and skill evolution.
    """)
    st.markdown("""
    - 🔥 Soft skills like adaptability and storytelling are more in-demand than ever.
    - 📈 Tools like Excel and Power BI are still gold — combine with Python for a killer combo.
    - 🚀 AI literacy is the new MS Office. Get comfortable with ChatGPT, Midjourney, or prompt writing.
    """)
    st.info("Reflect weekly: What did you learn this week that your resume still doesn’t show?")

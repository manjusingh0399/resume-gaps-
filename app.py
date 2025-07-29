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
tabs = st.tabs([
    "🏠 Welcome", "👤 Profile Snapshot", "📊 Market Comparison",
    "🎯 Match Score", "💡 Suggestions", "📚 Insights"])

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

    👈 Use the sidebar to select a resume profile.
    🔍 Then, explore each tab to uncover fun, insightful, and actionable insights — one click at a time.
    """
    )

# Profile Snapshot Tab
with tabs[1]:
    st.header("👤 Profile Snapshot")
    st.markdown("""
    🧾 Here’s a breakdown of what your resume is really saying about you — distilled into digestible data.
    """
    )
    st.json(user_data.to_dict())
    st.info("✨ This is your first impression on paper. Let’s make sure it’s saying the right things!")
    st.success("📌 Tip: Mirror your dream job descriptions — recruiters notice keyword alignment.")

# Market Comparison Tab
with tabs[2]:
    st.header("📊 Market Comparison")
    st.markdown("""
    🚀 See how your skills stack up against real job market demand and peer-level benchmarks.
    """
    )
    skills = ["Python", "Excel", "SQL", "Power BI", "Communication"]
    user_scores = [user_data.get(skill, 0) for skill in skills]
    market_avg = [80, 75, 70, 60, 85]
    df_compare = pd.DataFrame({"Skill": skills, "You": user_scores, "Market Avg": market_avg})
    fig = px.bar(df_compare, x='Skill', y=['You', 'Market Avg'],
                 barmode='group', title='🧠 Your Skills vs Market Expectations')
    st.plotly_chart(fig, use_container_width=True)
    st.warning("🧠 Insight: Any skill below market average = prime growth opportunity.")

# Match Score Tab
with tabs[3]:
    st.header("🎯 Match Score")
    st.markdown("""
    🎯 This score represents how aligned your resume is with the roles you're targeting.
    The closer to 100%, the more 'interview-ready' your profile is!
    """)
    score = int(user_data.get("MatchScore", 72))
    st.metric("🔥 Match Score", f"{score}%")
    if score >= 80:
        st.success("✅ Nailed it! You're closely aligned with what top roles require.")
    elif score >= 60:
        st.info("⚠️ Almost there! A few focused tweaks could level you up big time.")
    else:
        st.warning("🚧 Work in progress — this is your chance to stand out by upskilling smart.")

# Suggestions Tab
with tabs[4]:
    st.header("💡 Suggestions & Role Fit")
    st.markdown("""
    🧩 Based on your strengths and current resume highlights, here are roles you’re already pretty close to:
    """)
    st.markdown("""
    - 📌 **Data Analyst** — Strengthen SQL & Power BI to fully qualify.
    - 📌 **Marketing Associate** — Emphasize your storytelling & communication.
    - 📌 **Business Analyst** — Try adding certifications in Excel modeling or workflows.
    """)
    st.success("💬 Advice: Even a 5% upgrade in skills can unlock premium opportunities.")

# Insights Tab
with tabs[5]:
    st.header("📚 Career Insights & Trends")
    st.markdown("""
    💭 Want to future-proof your resume? Check out these growing trends in the job market:
    """)
    st.markdown("""
    - 🔥 Soft skills like adaptability and storytelling are more in-demand than ever.
    - 📈 Excel & Power BI are still industry essentials — even more when paired with Python.
    - 🚀 AI literacy is the new basic — from prompt crafting to using ChatGPT at work.
    """)
    st.info("✨ Weekly Challenge: Add one new achievement or learning to your resume every Friday!")

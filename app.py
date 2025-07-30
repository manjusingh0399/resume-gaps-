import streamlit as st
import plotly.express as px
import pandas as pd

# Load resume dataset
@st.cache_data
def load_data():
    return pd.read_csv("resumegaps_dataset.csv")  # Make sure this file exists in your directory

resume_df = load_data()

# Page Config
st.set_page_config(page_title="JobSnob: Resume vs Reality", layout="wide")

# Custom CSS Styling
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #fff2b0, #ffd280, #ffb347);
            color: #1f1f1f;
        }

        .stApp {
            background: linear-gradient(135deg, #FFF8DC, #FFEFD5);
        }

        .job-snob-hero {
            background: linear-gradient(to right, #FFD700, #FFA500);
            border-radius: 25px;
            padding: 2.5rem;
            text-align: center;
            color: #fff;
            box-shadow: 0 10px 30px rgba(255, 165, 0, 0.25);
            margin-bottom: 2rem;
        }

        .job-snob-title {
            font-size: 3.2rem;
            font-weight: 800;
            margin-bottom: 0.3rem;
        }

        .job-snob-tagline {
            font-size: 1.4rem;
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

        .stButton > button {
            background: linear-gradient(to right, #FFCC00, #FF9900);
            color: white;
            font-weight: 600;
            border-radius: 10px;
            padding: 0.5rem 1rem;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar Resume Selector
st.sidebar.header("🔍 Choose Resume Profile")
selected_resume = st.sidebar.selectbox("Select a Resume ID:", resume_df["ResumeID"].unique())
user_data = resume_df[resume_df["ResumeID"] == selected_resume].squeeze()

# Tabs Setup
tabs = st.tabs([
    "🏠 Welcome", "👤 Profile Snapshot", "📊 Market Comparison",
    "🎯 Match Score", "💡 Suggestions", "📚 Insights"
])

# ---------------------- TAB 1: Welcome ---------------------- #
with tabs[0]:
    st.markdown("""
    <div class="job-snob-hero">
        <div class="job-snob-title">💼 JobSnob</div>
        <div class="job-snob-tagline">“Only the best skills make the cut. No basic resumes allowed.”</div>
        <div class="job-snob-subtext">Welcome to your personalized resume reality check. Let’s match your skills to the job market and glow up your career potential.</div>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("👋 A New Kind of Resume Reality Check")
    st.markdown("""
    Welcome to **JobSnob**, where we unapologetically compare your resume with what the job market *actually* demands.
    
    This tool analyzes your skills, benchmarks them against industry expectations, and offers tailored feedback.
    
    Whether you're a newbie, a career switcher, or a rising star — this app gives you clarity, not fluff.

    👉 Start by choosing your resume profile on the sidebar.  
    👉 Then explore each tab — where we don’t just judge, we guide.
    """)

# ---------------------- TAB 2: Profile Snapshot ---------------------- #
with tabs[1]:
    st.header("👤 Profile Snapshot")
    st.markdown("""
    Here’s your resume decoded — clear and data-rich. Use this tab as your baseline.
    
    We look at what’s present — and what’s not — to set the stage for advice in later tabs.
    """)
    st.json(user_data.to_dict())

    st.info("📌 Tip: Highlight job-relevant keywords from listings — they act as magnets for recruiters.")
    st.warning("⚠️ If your resume is mostly text without metrics or impact — consider rewriting those bullets!")

# ---------------------- TAB 3: Market Comparison ---------------------- #
with tabs[2]:
    st.header("📊 Market Comparison")
    st.markdown("""
    Let’s pit your top skills against market averages. Where are you crushing it? Where can you level up?
    
    These gaps are golden — they show where growth = ROI.
    """)

    skills = ["Python", "Excel", "SQL", "Power BI", "Communication"]
    user_scores = [user_data.get(skill, 0) for skill in skills]
    market_avg = [80, 75, 70, 60, 85]
    df_compare = pd.DataFrame({"Skill": skills, "You": user_scores, "Market Avg": market_avg})
    fig = px.bar(df_compare, x='Skill', y=['You', 'Market Avg'],
                 barmode='group', title='🧠 Your Skills vs Market Expectations')
    st.plotly_chart(fig, use_container_width=True)

    st.success("✨ Skills above market average? Celebrate them in bold resume sections.")
    st.warning("📉 Skills lagging behind? Choose 1 to focus on for the next 30 days.")

# ---------------------- TAB 4: Match Score ---------------------- #
with tabs[3]:
    st.header("🎯 Match Score")
    st.markdown("""
    This score estimates how aligned your resume is with top industry roles.
    
    It’s not the final word — but it’s a strong signal of your current market readiness.
    """)
    
    score = int(user_data.get("MatchScore", 72))
    st.metric("📈 Resume Fit Score", f"{score}%")

    if score >= 80:
        st.success("🔥 Excellent! Your resume is tightly aligned with key job expectations.")
    elif score >= 60:
        st.info("📌 Almost there! Tweak phrasing or add missing tools to bump your score.")
    else:
        st.warning("⚠️ Time for a glow-up. Let’s turn this into a comeback story.")

    st.caption("💬 Want a higher score? Check role descriptions in your domain and backfill those missing bits!")

# ---------------------- TAB 5: Suggestions ---------------------- #
with tabs[4]:
    st.header("💡 Role Suggestions & Skill Moves")
    st.markdown("""
    Based on your resume strengths, here are roles where you’re a near-fit.
    
    Upgrade one or two key areas and you could be interview-ready in weeks.
    """)
    st.markdown("""
    - 💼 **Data Analyst** — You’re nearly there. Focus on SQL joins + Power BI dashboards.
    - 📈 **Business Analyst** — Try learning process modeling or Excel-based simulations.
    - 📢 **Marketing Executive** — Highlight content strategy and cross-channel campaigns.
    """)

    st.success("🎯 Action Step: Add one real-world project per target role to your portfolio/resume.")

# ---------------------- TAB 6: Career Insights ---------------------- #
with tabs[5]:
    st.header("📚 Career Insights")
    st.markdown("""
    What’s trending, what’s dying, and what makes you future-proof?
    
    We’ve scraped the signals so you don’t have to.
    """)
    st.markdown("""
    - 📊 **Excel + SQL = Basic toolkit** (still relevant!)
    - 🌱 **Adaptability & storytelling** are top soft skills in 2025.
    - 🤖 **Prompt engineering** and AI co-working are the next resume stars.
    """)

    st.info("🧠 Insight: Employers want proof of *learning ability* more than perfect skills.")
    st.success("📌 Tip: Weekly goal = 1 micro-certification or portfolio upgrade. Build proof, not fluff.")

# End Message
st.markdown("""
---
✅ **Ready to iterate?**  
Your resume is a prototype — every improvement gets you closer to your dream role.

🎯 Keep it evolving. Keep it honest. Keep it JobSnob.
""")

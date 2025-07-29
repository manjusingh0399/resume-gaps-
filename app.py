import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image

# --- CONFIGURATION ---
st.set_page_config(page_title="Resume vs Reality", layout="wide")

# --- Load Data ---
@st.cache_data
def load_data():
    df = pd.read_csv("data/skills_data.csv")
    return df

df = load_data()

# --- Header & Intro ---
st.markdown("""
    <style>
    html, body, [class*="css"]  {
        font-family: 'Helvetica';
        background-color: #fdfdfd;
    }
    .big-header {
        font-size: 2.4em;
        font-weight: bold;
        color: #ff4da6;
        margin-bottom: 10px;
    }
    .sub {
        font-size: 1.1em;
        color: #444;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="big-header">🚀 Resume vs Reality</div>', unsafe_allow_html=True)
st.markdown("""
<div class="sub">
    We all build resumes hoping they reflect our potential. But behind every hiring decision lies a pattern.<br>
    This app is an exploration of that gap — comparing what job seekers say, what jobs demand, and what actually gets you hired.<br><br>
    I’m Manju Singh, an MBA student and job seeker too. Like you, I’ve felt the anxiety and uncertainty — and I built this app to turn that doubt into clarity.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# --- Interactive Filters ---
industry = st.selectbox("📂 Choose Industry", ["All", "Tech", "Marketing", "Finance"])
role = st.selectbox("👩‍💼 Target Role", ["Analyst", "Marketer", "HR", "Sales", "Generalist"])
skill_level = st.radio("🧠 Skill Level", ["Beginner", "Intermediate", "Advanced"])

# --- Main Charts ---
st.subheader("📊 Visualizing Skills Across the Board")

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(
        px.bar(df, x="Skill", y=["Resumes", "Hires", "Job Ads"], barmode="group",
               title="Skill Distribution (Bar Chart)", color_discrete_sequence=["#ff4da6", "#3ec1d3", "#ffc93c"]),
        use_container_width=True
    )

    st.plotly_chart(
        px.scatter(df, x="Resumes", y="Hires", text="Skill", size="Job Ads",
                   title="Resume vs Hires (Scatter Plot)", color="Skill"),
        use_container_width=True
    )

with col2:
    st.plotly_chart(
        px.pie(df, names="Skill", values="Hires", title="Distribution of Hired Skills (Pie Chart)"),
        use_container_width=True
    )

    st.plotly_chart(
        px.area(df, x="Skill", y=["Resumes", "Hires", "Job Ads"],
                title="Skill Trend Overview (Area Chart)", color_discrete_sequence=["#e76f51", "#2a9d8f", "#f4a261"]),
        use_container_width=True
    )

# --- Smart Suggestions Panel ---
st.markdown("### 💡 Personalized Takeaways")
user_skills = st.text_input("Enter your skills (comma-separated)", "Excel, SQL, Communication").lower().split(',')

matched = df[df['Skill'].str.lower().isin([s.strip() for s in user_skills])]
unmatched = [s for s in user_skills if s.strip() not in df['Skill'].str.lower().tolist()]

if not matched.empty:
    st.success(f"✅ You listed {len(matched)} skill(s) that align with real hiring data.")
    st.dataframe(matched.set_index("Skill")[["Hires", "Job Ads"]])

if unmatched:
    st.warning(f"⚠️ These skills are not recognized in the current dataset: {', '.join(unmatched)}")

# --- Prediction-like Feature (Simple Likelihood Score) ---
score = (matched["Hires"].sum() / matched["Resumes"].sum()) if not matched.empty else 0
st.metric("📈 Likelihood Score (Based on Data)", f"{min(score * 100, 100):.2f}%")

# --- Footer ---
st.markdown("---")
st.markdown("""
<p style='text-align: center; font-size: 0.9em; color: gray;'>
Made with ❤️ by Manju Singh | Empowering careers with data. | Project: Resume vs Reality
</p>
""", unsafe_allow_html=True)

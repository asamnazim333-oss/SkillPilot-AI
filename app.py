import streamlit as st
from openai import OpenAI
import plotly.express as px
import pandas as pd

# ================== CONFIG ==================
st.set_page_config(page_title="SkillPilot AI", layout="wide")

st.title("🌍 SkillPilot AI")
st.markdown("### 💎 AI Career Decision Dashboard")

# ================== API ==================
client = OpenAI(
    api_key=st.secrets["GROQ_API_KEY"],
    base_url="https://api.groq.com/openai/v1",
)

language = st.sidebar.selectbox("🌐 Language", ["English", "Urdu"])

def ask_ai(prompt):
    if language == "Urdu":
        prompt = "Answer in simple Urdu:\n\n" + prompt

    response = client.responses.create(
        model="openai/gpt-oss-20b",
        input=prompt
    )
    return response.output_text


# ================== INPUT ==================
st.sidebar.header("🎯 Input")

skill = st.sidebar.text_input("Primary Skill", "Web Development")
compare_skill = st.sidebar.text_input("Compare Skill", "AI")

interests = st.sidebar.multiselect(
    "Interests",
    ["Coding", "Design", "Math", "AI", "Security", "Creativity"]
)

strengths = st.sidebar.multiselect(
    "Strengths",
    ["Logic", "Problem Solving", "Communication", "Creativity"]
)

generate = st.sidebar.button("🚀 Generate Dashboard")


# ================== DATA ==================
def market_data(skill):
    data = {
        "Web Development": (85, 80, 60),
        "AI": (95, 90, 75),
        "Cybersecurity": (90, 85, 80),
        "Data Science": (88, 87, 70),
    }
    return data.get(skill, (75, 70, 65))


# ================== MAIN DASHBOARD ==================
if generate:

    score, demand, difficulty = market_data(skill)

    # ================== 💎 NETFLIX STYLE CARDS ==================
    st.markdown("## 📊 Career Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.metric("🏆 Career Score", f"{score}/100")
    col2.metric("🔥 Demand", f"{demand}/100")
    col3.metric("⚠ Difficulty", f"{difficulty}/100")

    st.markdown("---")

    # ================== 📊 REAL GRAPH ==================
    st.subheader("📈 Career Visualization")

    df = pd.DataFrame({
        "Metric": ["Score", "Demand", "Difficulty"],
        "Value": [score, demand, difficulty]
    })

    fig = px.bar(df, x="Metric", y="Value", color="Metric")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ================== 🧠 AI DECISION ==================
    st.subheader("🧠 AI Career Decision")

    prompt = f"""
    Give ONLY:
    - Good / Risky / Not Recommended
    - One line reason
    - Final verdict

    Skill: {skill}
    Interests: {interests}
    Strengths: {strengths}
    """

    st.success(ask_ai(prompt))

    st.markdown("---")

    # ================== 🗺 ROADMAP ==================
    st.subheader("🗺 Roadmap")

    roadmap_prompt = f"""
    Give only bullet roadmap:
    Beginner → Intermediate → Advanced for {skill}
    """

    st.write(ask_ai(roadmap_prompt))

    st.markdown("---")

    # ================== 📚 RESOURCES ==================
    st.subheader("📚 Learning Resources")

    st.markdown(f"""
    - 🎥 [YouTube Courses](https://www.youtube.com/results?search_query={skill}+course)
    - 💻 GitHub Projects
    - 🧪 Practice Projects
    """)

    st.markdown("---")

    # ================== 🌍 JOB INSIGHT ==================
    st.subheader("🌍 Job Market Insight")

    st.info(f"""
    🔹 {skill} has strong global demand  
    🔹 Freelancing opportunities available  
    🔹 Remote jobs increasing  
    """)


# ================== COMPARISON ==================
st.markdown("---")
st.header("🆚 Skill Comparison")

if compare_skill:

    s1 = market_data(skill)
    s2 = market_data(compare_skill)

    df2 = pd.DataFrame({
        "Skill": [skill, compare_skill],
        "Score": [s1[0], s2[0]],
        "Demand": [s1[1], s2[1]],
        "Difficulty": [s1[2], s2[2]]
    })

    fig2 = px.bar(df2, x="Skill", y="Score", color="Skill", barmode="group")
    st.plotly_chart(fig2, use_container_width=True)

    winner = skill if s1[0] > s2[0] else compare_skill

    st.success(f"🏆 Recommended: {winner}")

else:
    st.info("Enter a skill to compare in sidebar")

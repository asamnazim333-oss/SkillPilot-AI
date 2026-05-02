import streamlit as st
from openai import OpenAI
import random

# ================== CONFIG ==================
st.set_page_config(page_title="SkillPilot AI", layout="wide")

st.title("🌍 SkillPilot AI")
st.markdown("AI-powered Career Intelligence Platform 🤖")

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


# ================== SIDEBAR ==================
st.sidebar.header("🎯 Input")

skill = st.sidebar.text_input("Enter Skill", "Web Development")

interests = st.sidebar.multiselect(
    "Interests",
    ["Coding", "Design", "Math", "AI", "Security", "Creativity"]
)

strengths = st.sidebar.multiselect(
    "Strengths",
    ["Logic", "Problem Solving", "Communication", "Creativity"]
)

generate = st.sidebar.button("🚀 Generate Analysis")


# ================== MOCK REAL-WORLD DATA (IMPORTANT) ==================
def get_market_data(skill):
    data = {
        "Web Development": (85, "High", "Medium"),
        "AI": (95, "Very High", "Hard"),
        "Cybersecurity": (90, "High", "Hard"),
        "Data Science": (88, "High", "Medium"),
    }
    return data.get(skill, (75, "Medium", "Medium"))


# ================== DASHBOARD ==================
if generate:

    st.markdown("## 📊 Career Dashboard")

    score, demand, difficulty = get_market_data(skill)

    col1, col2, col3 = st.columns(3)

    col1.metric("Career Score", f"{score}/100")
    col2.metric("Demand", demand)
    col3.metric("Difficulty", difficulty)

    st.markdown("---")


    # ================== 📈 GRAPH SECTION ==================
    st.subheader("📈 Career Insights Graph")

    st.bar_chart({
        "Demand": [score],
        "Difficulty": [random.randint(40, 90)],
        "Growth": [random.randint(60, 100)]
    })

    st.markdown("---")


    # ================== 🧠 AI ROADMAP ==================
    st.subheader("🗺 AI Roadmap")

    roadmap_prompt = f"""
    Create structured roadmap for {skill}:

    Beginner → Intermediate → Advanced

    Include:
    - Skills
    - Tools
    - Projects
    """

    st.markdown(ask_ai(roadmap_prompt))

    st.markdown("---")


    # ================== 🧠 REASONING MODE ==================
    st.subheader("🧠 AI Reasoning (Decision Engine)")

    reasoning_prompt = f"""
    Think step by step:

    User:
    Interests: {interests}
    Strengths: {strengths}
    Career: {skill}

    1. Analyze user profile
    2. Match with skill requirements
    3. Check market demand
    4. Evaluate difficulty
    5. Give final recommendation with confidence score
    """

    st.markdown(ask_ai(reasoning_prompt))

    st.markdown("---")


    # ================== ⚠ DRAWBACKS ==================
    st.subheader("⚠ Risks & Drawbacks")

    drawback_prompt = f"""
    List realistic drawbacks of {skill}:
    - Competition
    - Learning difficulty
    - Time required
    - Common mistakes
    """

    st.markdown(ask_ai(drawback_prompt))


# ================== 🤖 MENTOR MODE ==================
st.markdown("---")
st.subheader("🤖 AI Mentor")

question = st.text_input("Ask career question")

if question:
    mentor_prompt = f"""
    You are a career mentor.

    User Interests: {interests}
    User Strengths: {strengths}

    Question: {question}
    """

    st.markdown(ask_ai(mentor_prompt))


# ================== 🌍 JOB INSIGHT ==================
if generate:
    st.markdown("---")
    st.subheader("🌍 Job Market Insight")

    st.info(f"""
    📌 {skill} Career Outlook:
    - Freelancing: High
    - Remote Jobs: Medium-High
    - Internship Availability: Good
    - Global Demand: Increasing
    """)

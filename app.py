import streamlit as st
from openai import OpenAI

# ================== CONFIG ==================
st.set_page_config(page_title="SkillPilot AI", layout="wide")

st.title("🌍 SkillPilot AI")
st.markdown("### ⚡ Career Decision Dashboard (AI-Powered)")

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


# ================== MOCK MARKET DATA ==================
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

    st.markdown("## 📊 Career Dashboard")

    score, demand, difficulty = market_data(skill)

    col1, col2, col3 = st.columns(3)

    col1.metric("Career Score", f"{score}/100")
    col2.metric("Demand", f"{demand}/100")
    col3.metric("Difficulty", f"{difficulty}/100")

    st.markdown("---")

    # ================== VISUAL BARS ==================
    st.subheader("📈 Career Insights")

    st.progress(score / 100)
    st.caption("Overall Career Strength")

    st.progress(demand / 100)
    st.caption("Market Demand")

    st.progress(difficulty / 100)
    st.caption("Difficulty Level")

    st.markdown("---")

    # ================== AI REASONING (SHORT) ==================
    st.subheader("🧠 AI Decision")

    prompt = f"""
    Give ONLY:
    1. Is this a good career (Yes/No)
    2. One line reason
    3. Final recommendation

    Skill: {skill}
    Interests: {interests}
    Strengths: {strengths}
    """

    st.success(ask_ai(prompt))

    st.markdown("---")

    # ================== ROADMAP ==================
    st.subheader("🗺 Quick Roadmap")

    roadmap_prompt = f"""
    Give only bullet roadmap:
    Beginner → Intermediate → Advanced for {skill}
    """

    st.write(ask_ai(roadmap_prompt))

    st.markdown("---")

    # ================== RESOURCES (CLICKABLE) ==================
    st.subheader("📚 Learning Resources")

    st.markdown(f"""
    - 🎥 [YouTube Courses](https://www.youtube.com/results?search_query={skill}+full+course)
    - 📘 Free Learning Guides
    - 💻 GitHub Projects
    - 🧪 Practice Projects
    """)

    st.markdown("---")

    # ================== JOB INSIGHT ==================
    st.subheader("🌍 Job Market Insight")

    st.info(f"""
    🔹 {skill} has strong global demand  
    🔹 Freelancing opportunities available  
    🔹 Remote jobs increasing  
    🔹 Industry growth is positive
    """)


# ================== COMPARISON ==================
st.markdown("---")
st.header("🆚 Skill Comparison Dashboard")

if compare_skill:

    s1 = market_data(skill)
    s2 = market_data(compare_skill)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader(skill)
        st.metric("Score", f"{s1[0]}/100")
        st.metric("Demand", f"{s1[1]}/100")
        st.metric("Difficulty", f"{s1[2]}/100")

    with col2:
        st.subheader(compare_skill)
        st.metric("Score", f"{s2[0]}/100")
        st.metric("Demand", f"{s2[1]}/100")
        st.metric("Difficulty", f"{s2[2]}/100")

    st.markdown("---")

    st.subheader("🏆 Verdict")

    if s1[0] > s2[0]:
        st.success(f"Recommended: {skill} 🚀")
    else:
        st.success(f"Recommended: {compare_skill} 🚀")

else:
    st.info("Enter a skill to compare in sidebar")

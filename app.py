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

def ask_ai(prompt):
    response = client.responses.create(
        model="openai/gpt-oss-20b",
        input=prompt
    )
    return response.output_text


# ================== INPUT ==================
skill = st.sidebar.text_input("Skill", "Web Development")
compare = st.sidebar.text_input("Compare Skill", "AI")

generate = st.sidebar.button("🚀 Generate")


# ================== MOCK DATA ==================
def get_data(skill):
    data = {
        "Web Development": (85, 80, 60),
        "AI": (95, 90, 75),
        "Cybersecurity": (90, 85, 80),
    }
    return data.get(skill, (75, 70, 60))


# ================== MAIN ==================
if generate:

    score, demand, difficulty = get_data(skill)

    # ================== 💎 CARDS ==================
    st.subheader("📊 Career Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.metric("Career Score", f"{score}/100")
    col2.metric("Demand", f"{demand}/100")
    col3.metric("Difficulty", f"{difficulty}/100")

    st.markdown("---")

    # ================== 📊 PLOTLY GRAPH ==================
    st.subheader("📈 Career Visualization")

    df = pd.DataFrame({
        "Metric": ["Score", "Demand", "Difficulty"],
        "Value": [score, demand, difficulty]
    })

    fig = px.bar(df, x="Metric", y="Value", color="Metric", title="Career Analysis")
    st.plotly_chart(fig)

    st.markdown("---")

    # ================== 🧠 AI DECISION ==================
    st.subheader("🧠 AI Decision")

    prompt = f"""
    Give:
    - Is {skill} a good career?
    - One line reason
    - Final recommendation
    """

    st.success(ask_ai(prompt))

    st.markdown("---")

    # ================== 🗺 ROADMAP ==================
    st.subheader("🗺 Roadmap")

    roadmap = f"""
    Beginner → Intermediate → Advanced for {skill}
    """

    st.write(roadmap)

    st.markdown("---")

    # ================== 📚 RESOURCES ==================
    st.subheader("📚 Resources")

    st.markdown(f"""
    - 🎥 [YouTube](https://www.youtube.com/results?search_query={skill}+course)
    - 💻 GitHub Projects
    - 🧪 Practice Work
    """)

# ================== COMPARISON ==================
st.markdown("---")
st.header("🆚 Comparison")

if compare:

    s1 = get_data(skill)
    s2 = get_data(compare)

    df2 = pd.DataFrame({
        "Skill": [skill, compare],
        "Score": [s1[0], s2[0]],
        "Demand": [s1[1], s2[1]],
        "Difficulty": [s1[2], s2[2]]
    })

    fig2 = px.bar(df2, x="Skill", y="Score", color="Skill", title="Skill Comparison")
    st.plotly_chart(fig2)

    winner = skill if s1[0] > s2[0] else compare

    st.success(f"🏆 Recommended: {winner}")

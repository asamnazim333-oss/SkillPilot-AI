import streamlit as st
from openai import OpenAI

# ================== CONFIG ==================
st.set_page_config(page_title="SkillPilot AI", layout="wide")

st.title("🌍 SkillPilot AI")
st.markdown("AI-powered career decision & roadmap system 🤖")

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

skill = st.sidebar.text_input("Enter Skill", "Web Development")
compare_skill = st.sidebar.text_input("Compare Skill (optional)")

interests = st.sidebar.multiselect(
    "Interests",
    ["Coding", "Design", "Math", "AI", "Security", "Creativity"]
)

strengths = st.sidebar.multiselect(
    "Strengths",
    ["Logic", "Problem Solving", "Communication", "Creativity"]
)

generate = st.sidebar.button("🚀 Generate Analysis")
show_test = st.sidebar.button("🧪 Skill Test Result")

q1 = st.sidebar.radio("Problem Solving?", ["Yes", "No"])
q2 = st.sidebar.radio("Creativity?", ["Yes", "No"])
q3 = st.sidebar.radio("Math Comfort?", ["Yes", "No"])

# ================== TABS ==================
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["🗺 Roadmap", "📊 Career Score", "📚 Resources", "🤖 Mentor", "🆚 Compare"]
)

# ================== ROADMAP ==================
with tab1:
    if generate:
        st.subheader("📍 Roadmap")

        prompt = f"""
        Create structured roadmap for {skill}:
        Beginner → Intermediate → Advanced
        Timeline: 3-6 months
        """

        st.markdown(ask_ai(prompt))

# ================== CAREER SCORE ==================
with tab2:
    if generate:
        st.subheader("📊 Career Analysis")

        prompt = f"""
        Analyze {skill}:

        - Career Score (0-100)
        - Demand
        - Salary Range
        - Future Scope
        - Difficulty
        """

        st.markdown(ask_ai(prompt))

# ================== RESOURCES ==================
with tab3:
    if generate:
        st.subheader("📚 Learning Resources")

        st.markdown(
            f"👉 [YouTube Courses](https://www.youtube.com/results?search_query={skill}+full+course)"
        )

# ================== MENTOR ==================
with tab4:
    st.subheader("🤖 AI Mentor")

    question = st.text_input("Ask anything")

    if question:
        prompt = f"""
        Interests: {interests}
        Strengths: {strengths}

        Question: {question}
        """

        st.markdown(ask_ai(prompt))

# ================== COMPARE ==================
with tab5:
    st.subheader("🆚 Comparison")

    if generate and compare_skill:
        prompt = f"""
        Compare {skill} vs {compare_skill}:

        - Demand
        - Salary
        - Difficulty
        - Future Scope
        """

        st.markdown(ask_ai(prompt))

    elif generate:
        st.info("Enter a skill to compare")

# ================== SKILL TEST ==================
if show_test:
    st.markdown("---")
    st.subheader("🧪 Skill Test Result")

    prompt = f"""
    Answers:
    Problem Solving: {q1}
    Creativity: {q2}
    Math: {q3}

    Suggest best career path and explain.
    """

    st.markdown(ask_ai(prompt))

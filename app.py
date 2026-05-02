import streamlit as st
from openai import OpenAI

# ================== CONFIG ==================
st.set_page_config(page_title="SkillPilot AI", layout="wide")

st.title("🌍 SkillPilot AI")
st.markdown("AI-powered career roadmap & decision system 🤖")

# ================== API ==================
client = OpenAI(
    api_key=st.secrets["GROQ_API_KEY"],
    base_url="https://api.groq.com/openai/v1",
)

# ================== LANGUAGE ==================
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
compare_skill = st.sidebar.text_input("Compare Skill (optional)")

interests = st.sidebar.multiselect(
    "Interests",
    ["Coding", "Design", "Math", "AI", "Security", "Creativity"]
)

strengths = st.sidebar.multiselect(
    "Strengths",
    ["Logic", "Problem Solving", "Communication", "Creativity"]
)

# ================== SKILL TEST ==================
st.sidebar.markdown("### 🧪 Skill Test")

q1 = st.sidebar.radio("Do you enjoy problem solving?", ["Yes", "No"])
q2 = st.sidebar.radio("Do you like creativity?", ["Yes", "No"])
q3 = st.sidebar.radio("Are you comfortable with math?", ["Yes", "No"])

generate = st.sidebar.button("🚀 Generate Analysis")
show_test = st.sidebar.button("🧪 Show Skill Test Result")

# ================== TABS ==================
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["🗺 Roadmap", "📊 Career Score", "📚 Resources", "🤖 Mentor", "🆚 Compare"]
)

# ================== 1. ROADMAP ==================
with tab1:
    if generate:
        st.subheader("📍 Roadmap")

        prompt = f"""
        Create structured roadmap for {skill}:
        Beginner, Intermediate, Advanced, Timeline (3-6 months)
        """

        st.markdown(ask_ai(prompt))

# ================== 2. CAREER SCORE ==================
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

        st.markdown("---")
        st.subheader("⚠ Drawbacks")

        prompt2 = f"""
        Drawbacks of {skill}:
        - competition
        - learning difficulty
        - time required
        """

        st.markdown(ask_ai(prompt2))

# ================== 3. RESOURCES ==================
with tab3:
    if generate:
        st.subheader("📚 Learning Resources")

        st.markdown(
            f"👉 [Watch Full Courses on YouTube](https://www.youtube.com/results?search_query={skill}+full+course)"
        )

# ================== 4. MENTOR ==================
with tab4:
    st.subheader("🤖 AI Mentor")

    question = st.text_input("Ask anything about career")

    if question:
        prompt = f"""
        User interests: {interests}
        User strengths: {strengths}

        Question: {question}
        """

        st.markdown(ask_ai(prompt))

# ================== 5. COMPARISON ==================
with tab5:
    st.subheader("🆚 Skill Comparison")

    if generate and compare_skill:

        prompt = f"""
        Compare {skill} vs {compare_skill}:

        - Demand
        - Salary
        - Difficulty
        - Future Scope
        - Which is better and why
        """

        st.markdown(ask_ai(prompt))

    elif generate:
        st.info("Please enter a skill to compare in sidebar")

# ================== SKILL TEST RESULT ==================
if show_test:
    st.markdown("---")
    st.subheader("🧪 Skill Test Result")

    prompt = f"""
    Answers:
    Problem solving: {q1}
    Creativity: {q2}
    Math: {q3}

    Suggest best career path and explain why.
    """

    st.markdown(ask_ai(prompt))

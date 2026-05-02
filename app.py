import streamlit as st
from openai import OpenAI

# ================== CONFIG ==================
st.set_page_config(page_title="SkillPilot AI", layout="wide")

st.title("🌍 SkillPilot AI")
st.markdown("AI-powered career roadmap & guidance platform 🤖")

# ================== API ==================
client = OpenAI(
    api_key=st.secrets["GROQ_API_KEY"],
    base_url="https://api.groq.com/openai/v1",
)

# ================== LANGUAGE ==================
language = st.sidebar.selectbox(
    "🌐 Response Language",
    ["English", "Urdu"]
)

def ask_ai(prompt):
    try:
        if language == "Urdu":
            prompt = "Answer in simple Urdu:\n\n" + prompt

        response = client.responses.create(
            model="openai/gpt-oss-20b",
            input=prompt
        )
        return response.output_text
    except Exception as e:
        return f"Error: {e}"

# ================== SIDEBAR ==================
st.sidebar.header("🎯 Input")

skill = st.sidebar.text_input("Enter Skill / Career", "Web Development")

compare_skill = st.sidebar.text_input("Compare with another skill (optional)")

interests = st.sidebar.multiselect(
    "Your Interests",
    ["Coding", "Design", "Math", "AI", "Security", "Creativity"]
)

strengths = st.sidebar.multiselect(
    "Your Strengths",
    ["Logic", "Problem Solving", "Communication", "Creativity"]
)

st.sidebar.markdown("### 🧪 Quick Skill Test")

q1 = st.sidebar.radio("Do you enjoy problem solving?", ["Yes", "No"])
q2 = st.sidebar.radio("Do you like creativity?", ["Yes", "No"])
q3 = st.sidebar.radio("Are you comfortable with math?", ["Yes", "No"])

generate = st.sidebar.button("🚀 Generate")

# ================== TABS ==================
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["🗺 Roadmap", "📊 Scope", "📚 Resources", "🤖 Mentor", "🆚 Compare"]
)

# ================== ROADMAP ==================
with tab1:
    if generate:
        st.subheader("📍 Learning Roadmap")

        with st.spinner("Generating roadmap..."):
            prompt = f"""
            Create a structured roadmap for {skill}:

            Beginner:
            - topics
            - tools

            Intermediate:
            - projects

            Advanced:
            - real-world projects

            Timeline: 3-6 months
            """

            st.markdown(ask_ai(prompt))

# ================== SCOPE ==================
with tab2:
    if generate:
        st.subheader("📊 Career Scope")

        with st.spinner("Analyzing..."):
            prompt = f"""
            Analyze {skill}:

            - Demand
            - Salary range
            - Future scope
            - Difficulty
            """

            st.markdown(ask_ai(prompt))

        st.markdown("---")

        st.subheader("⚠ Drawbacks")

        prompt2 = f"""
        Drawbacks of {skill}:
        - competition
        - time required
        - challenges
        """

        st.markdown(ask_ai(prompt2))

# ================== RESOURCES ==================
with tab3:
    if generate:
        st.subheader("📚 Learning Resources")

        search_url = f"https://www.youtube.com/results?search_query={skill}+full+course"

        st.markdown("### 🎥 Best Learning Resources")
        st.markdown(f"[👉 Click here to watch courses on YouTube]({search_url})")

        st.info("Resources are generated using YouTube search for stability.")

# ================== MENTOR ==================
with tab4:
    st.subheader("🤖 AI Mentor")

    question = st.text_input("Ask anything about your career")

    if question:
        with st.spinner("Thinking..."):
            prompt = f"""
            You are a career mentor.

            Interests: {interests}
            Strengths: {strengths}

            Question: {question}
            """

            st.markdown(ask_ai(prompt))

# ================== COMPARISON ==================
with tab5:
    if generate and compare_skill:
        st.subheader("⚖ Skill Comparison")

        with st.spinner("Comparing..."):
            prompt = f"""
            Compare {skill} vs {compare_skill}:

            - Demand
            - Salary
            - Difficulty
            - Future scope
            """

            st.markdown(ask_ai(prompt))

# ================== PERSONAL FIT ==================
if generate:
    st.markdown("---")
    st.subheader("🧠 Is this right for you?")

    prompt = f"""
    User:
    Interests: {interests}
    Strengths: {strengths}

    Evaluate {skill}:
    - Good / Risky / Not Recommended
    - Reason
    """

    st.markdown(ask_ai(prompt))

# ================== SKILL TEST ==================
if generate:
    st.markdown("---")
    st.subheader("🧪 Skill Test Result")

    prompt = f"""
    Answers:
    Problem solving: {q1}
    Creativity: {q2}
    Math: {q3}

    Suggest best career path with reasoning.
    """

    st.markdown(ask_ai(prompt))

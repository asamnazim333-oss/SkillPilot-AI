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


# ================== SIDEBAR INPUT ==================
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

# ================== SKILL TEST (UPGRADED) ==================
st.sidebar.markdown("### 🧪 Skill Test")

q1 = st.sidebar.radio("Do you enjoy problem solving?", ["Yes", "No"])
q2 = st.sidebar.radio("Do you like creativity?", ["Yes", "No"])
q3 = st.sidebar.radio("Are you comfortable with math?", ["Yes", "No"])

generate = st.sidebar.button("🚀 Generate Analysis")
suggest = st.sidebar.button("🎯 Suggest Best Career")

compare_skill = st.sidebar.text_input("Compare Skill (optional)")

# ================== TABS ==================
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["🗺 Roadmap", "📊 Career Score", "📚 Resources", "🤖 Mentor", "🧠 Decision Mode"]
)

# ================== 1. ROADMAP ==================
with tab1:
    if generate:
        st.subheader("📍 Structured Roadmap")

        prompt = f"""
        Create structured roadmap for {skill}:

        Beginner:
        - topics

        Intermediate:
        - topics

        Advanced:
        - real projects

        Timeline: 3-6 months
        """

        st.markdown(ask_ai(prompt))

# ================== 2. CAREER SCORE ==================
with tab2:
    if generate:
        st.subheader("📊 Career Score System")

        prompt = f"""
        Evaluate {skill} and return:

        - Career Score (0-100)
        - Demand (High/Medium/Low)
        - Growth Level
        - Risk Level
        - Salary Range
        - Future Scope
        """

        st.markdown(ask_ai(prompt))

        st.markdown("---")
        st.subheader("⚠ Drawbacks")

        prompt2 = f"""
        Drawbacks of {skill}:
        - competition
        - difficulty
        - time required
        - common mistakes
        """

        st.markdown(ask_ai(prompt2))

# ================== 3. RESOURCES ==================
with tab3:
    if generate:
        st.subheader("📚 Learning Resources")

        st.markdown(
            f"👉 [Watch YouTube Courses](https://www.youtube.com/results?search_query={skill}+full+course)"
        )

# ================== 4. AI MENTOR ==================
with tab4:
    st.subheader("🤖 AI Mentor")

    question = st.text_input("Ask career question")

    if question:
        prompt = f"""
        User interests: {interests}
        User strengths: {strengths}

        Question: {question}
        """

        st.markdown(ask_ai(prompt))

# ================== 5. DECISION MODE ==================
with tab5:
    if generate:
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

    if suggest:
        st.subheader("🎯 Best Career Suggestions")

        prompt = f"""
        Based on:
        Interests: {interests}
        Strengths: {strengths}

        Suggest top 3 career paths with reasons.
        """

        st.markdown(ask_ai(prompt))

# ================== SKILL TEST RESULT ==================
if generate:
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

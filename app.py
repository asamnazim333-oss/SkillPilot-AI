import streamlit as st
from openai import OpenAI
from youtubesearchpython import VideosSearch

# ================== CONFIG ==================
st.set_page_config(page_title="SkillPilot AI", layout="wide")

st.title("🌍 SkillPilot AI")
st.markdown("AI-powered career roadmap & guidance platform")

# ================== API ==================
client = OpenAI(
    api_key=st.secrets["GROQ_API_KEY"],
    base_url="https://api.groq.com/openai/v1",
)

def ask_ai(prompt):
    try:
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
    ["🗺 Roadmap", "📊 Scope", "📚 Resources", "🤖 AI Mentor", "🆚 Compare"]
)

# ================== ROADMAP ==================
with tab1:
    if generate:
        st.subheader("📍 Learning Roadmap")

        with st.spinner("Generating roadmap..."):
            roadmap_prompt = f"""
            Create a CLEAN roadmap for {skill}:

            ## Beginner
            - topics
            - tools

            ## Intermediate
            - projects

            ## Advanced
            - real-world projects

            ## Timeline (3-6 months)
            """

            result = ask_ai(roadmap_prompt)
            st.markdown(result)

            st.download_button("📥 Download Roadmap", result)

# ================== CAREER SCOPE ==================
with tab2:
    if generate:
        st.subheader("📊 Career Analysis")

        with st.spinner("Analyzing career..."):
            scope_prompt = f"""
            Analyze {skill}:

            - Demand
            - Salary Range
            - Future Scope
            - Difficulty
            """

            result = ask_ai(scope_prompt)
            st.markdown(result)

        st.markdown("---")

        st.subheader("⚠ Drawbacks")

        drawback_prompt = f"""
        Drawbacks of {skill}:
        - competition
        - time required
        - mistakes
        """

        st.markdown(ask_ai(drawback_prompt))

# ================== RESOURCES ==================
with tab3:
    if generate:
        st.subheader("📚 Learning Resources")

        try:
            videos_search = VideosSearch(f"{skill} full course tutorial", limit=5)
            results = videos_search.result()

            if results and "result" in results:
                for video in results["result"]:
                    title = video.get("title", "No title")
                    link = video.get("link", "")

                    if link:
                        st.markdown(f"### 🎥 {title}")
                        st.video(link)
                        st.markdown("---")
            else:
                st.warning("No videos found")

        except Exception as e:
            st.error(f"Error: {e}")

# ================== AI MENTOR ==================
with tab4:
    st.subheader("🤖 AI Career Mentor")

    user_question = st.text_input("Ask anything...")

    if user_question:
        with st.spinner("Thinking..."):
            mentor_prompt = f"""
            You are a career mentor.

            Interests: {interests}
            Strengths: {strengths}

            Question: {user_question}

            Give clear and practical advice.
            """

            st.markdown(ask_ai(mentor_prompt))

# ================== COMPARISON ==================
with tab5:
    if generate and compare_skill:
        st.subheader("⚖ Skill Comparison")

        with st.spinner("Comparing skills..."):
            compare_prompt = f"""
            Compare {skill} vs {compare_skill}:

            - Demand
            - Salary
            - Difficulty
            - Future scope
            """

            st.markdown(ask_ai(compare_prompt))

# ================== PERSONAL FIT ==================
if generate:
    st.markdown("---")
    st.subheader("🧠 Is this right for you?")

    fit_prompt = f"""
    Interests: {interests}
    Strengths: {strengths}

    Evaluate {skill}:

    - Verdict (Good/Risky/Not Recommended)
    - Reason
    """

    st.markdown(ask_ai(fit_prompt))

# ================== SKILL TEST RESULT ==================
if generate:
    st.markdown("---")
    st.subheader("🧪 Skill Test Recommendation")

    test_prompt = f"""
    Answers:
    Problem solving: {q1}
    Creativity: {q2}
    Math: {q3}

    Suggest best career and explain.
    """

    st.markdown(ask_ai(test_prompt))

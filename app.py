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

interests = st.sidebar.multiselect(
    "Your Interests",
    ["Coding", "Design", "Math", "AI", "Security", "Creativity"]
)

strengths = st.sidebar.multiselect(
    "Your Strengths",
    ["Logic", "Problem Solving", "Communication", "Creativity"]
)

generate = st.sidebar.button("🚀 Generate")

# ================== TABS ==================
tab1, tab2, tab3, tab4 = st.tabs(
    ["🗺 Roadmap", "📊 Scope", "📚 Resources", "🤖 AI Mentor"]
)

# ================== ROADMAP ==================
with tab1:
    if generate:
        st.subheader("📍 Learning Roadmap")

        roadmap_prompt = f"""
        Create a CLEAN and STRUCTURED roadmap for {skill}.

        Format:
        ## Beginner
        - topics
        - tools

        ## Intermediate
        - topics
        - projects

        ## Advanced
        - topics
        - real-world projects

        ## Timeline
        (3-6 months plan)

        Keep it concise and readable.
        """

        result = ask_ai(roadmap_prompt)
        st.markdown(result)

# ================== CAREER SCOPE ==================
with tab2:
    if generate:
        st.subheader("📊 Career Analysis")

        scope_prompt = f"""
        Analyze {skill} career.

        Format:
        - Demand: High/Medium/Low
        - Salary Range:
        - Future Scope:
        - Top Countries:
        - Difficulty:
        """

        result = ask_ai(scope_prompt)
        st.markdown(result)

        st.markdown("---")

        st.subheader("⚠ Drawbacks")

        drawback_prompt = f"""
        List realistic drawbacks of {skill}:
        - Competition
        - Learning curve
        - Time required
        - Common mistakes
        """

        st.markdown(ask_ai(drawback_prompt))

# ================== RESOURCES ==================
with tab3:
    if generate:
        st.subheader("📚 Learning Resources")

        try:
            videos_search = VideosSearch(skill + " full course", limit=3)
            results = videos_search.result()

            for video in results["result"]:
                st.markdown(f"### 🎥 {video['title']}")
                st.write(video["link"])
                st.markdown("---")

        except:
            st.warning("Could not fetch videos")

# ================== AI MENTOR ==================
with tab4:
    st.subheader("🤖 AI Career Mentor")

    user_question = st.text_input("Ask anything...")

    if user_question:
        mentor_prompt = f"""
        You are a smart career mentor.

        User interests: {interests}
        User strengths: {strengths}

        Question: {user_question}

        Give practical, honest advice in simple words.
        """

        st.markdown(ask_ai(mentor_prompt))

# ================== PERSONAL FIT ==================
if generate:
    st.markdown("---")
    st.subheader("🧠 Is this right for you?")

    fit_prompt = f"""
    User interests: {interests}
    User strengths: {strengths}

    Evaluate if {skill} is suitable.

    Format:
    - Verdict: Good / Risky / Not Recommended
    - Reason:
    """

    st.markdown(ask_ai(fit_prompt))

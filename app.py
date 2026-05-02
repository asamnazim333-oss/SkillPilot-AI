import streamlit as st
from groq import Groq
from youtubesearchpython import VideosSearch

# ================== CONFIG ==================
st.set_page_config(page_title="SkillPilot AI", layout="wide")

st.title("🌍 SkillPilot AI")
st.markdown("AI-powered career roadmap & guidance platform")

# ================== API ==================
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=GROQ_API_KEY)

def ask_ai(prompt):
    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="mixtral-8x7b-32768"
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

# ================== SIDEBAR ==================
st.sidebar.header("Input")

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
tab1, tab2, tab3, tab4 = st.tabs(["🗺 Roadmap", "📊 Scope", "📚 Resources", "🤖 AI Mentor"])

# ================== ROADMAP ==================
with tab1:
    if generate:
        st.subheader("📍 Learning Roadmap")

        roadmap_prompt = f"""
        Create a complete roadmap for learning {skill}.
        Include:
        - Beginner to advanced steps
        - Timeline
        - Tools & technologies
        - Projects at each stage
        """

        result = ask_ai(roadmap_prompt)
        st.write(result)

# ================== CAREER SCOPE ==================
with tab2:
    if generate:
        st.subheader("📊 Career Analysis")

        scope_prompt = f"""
        Analyze career scope for {skill}.
        Include:
        - Demand level (High/Medium/Low)
        - Salary range
        - Future scope
        - Countries with high demand
        - Difficulty level
        """

        result = ask_ai(scope_prompt)
        st.write(result)

        st.subheader("⚠ Drawbacks")

        drawback_prompt = f"""
        List drawbacks of choosing {skill}:
        - competition
        - difficulty
        - time required
        - common mistakes
        """

        st.write(ask_ai(drawback_prompt))

# ================== RESOURCES ==================
with tab3:
    if generate:
        st.subheader("📚 Learning Resources")

        try:
            videos_search = VideosSearch(skill + " course", limit=3)
            results = videos_search.result()

            for video in results["result"]:
                st.markdown(f"### {video['title']}")
                st.write(video["link"])

        except:
            st.warning("Could not fetch videos")

# ================== AI MENTOR ==================
with tab4:
    st.subheader("🤖 Ask AI Mentor")

    user_question = st.text_input("Ask anything about your career")

    if user_question:
        mentor_prompt = f"""
        You are a career mentor.

        User interests: {interests}
        User strengths: {strengths}

        Question: {user_question}

        Give helpful and practical advice.
        """

        st.write(ask_ai(mentor_prompt))

# ================== PERSONAL FIT ==================
if generate:
    st.subheader("🧠 Is this right for you?")

    fit_prompt = f"""
    User interests: {interests}
    User strengths: {strengths}

    Is {skill} suitable?

    Give:
    - Verdict (Good / Risky / Not Recommended)
    - Reasoning
    """

    st.write(ask_ai(fit_prompt))

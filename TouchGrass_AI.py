
import requests
import streamlit as st

st.set_page_config(
    page_title="TouchGrass AI",
    page_icon="🌿",
    layout="centered",
)

st.title("🌿 TouchGrass AI")
st.subheader("Less scrolling. More exploring.")
st.write(
    "Generate a personalized outdoor adventure "
    "and take your screen break into the real world."
)

activity = st.selectbox(
    "What would you like to do?",
    ["Walking", "Running", "Nature observation", "Gardening"],
)

duration = st.selectbox(
    "How much time do you have?",
    [10, 20, 30],
    format_func=lambda x: f"{x} minutes",
)

energy = st.selectbox(
    "What's your energy level?",
    ["Relaxed", "Moderate", "Energetic"],
)

environment = st.selectbox(
    "Where will you go?",
    ["Park", "Garden", "Neighbourhood", "Trail"],
)

if st.button("Generate my outdoor quest", type="primary"):
    prompt = f"""
    Create a safe, practical outdoor quest.

    Activity: {activity}
    Duration: {duration} minutes
    Energy: {energy}
    Environment: {environment}

    Provide a short title, three achievable tasks,
    and one reflection question.

    Do not invent real locations or claim to identify
    wildlife species without evidence.
    Keep the response concise and accessible.
    """

    with st.spinner("Creating your outdoor quest..."):
        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "qwen2.5:3b",
                    "prompt": prompt,
                    "stream": False,
                },
                timeout=180,
            )
            response.raise_for_status()
            mission = response.json()["response"]

            st.success("Your quest is ready!")
            st.markdown(mission)
            st.info(
                "Save your mission, head outside, "
                "and put your phone away."
            )

        except requests.RequestException as error:
            st.error(
                "Could not reach Ollama. Check that "
                "Ollama is installed, running, and "
                "has qwen2.5:3b downloaded."
            )
            st.caption(str(error))

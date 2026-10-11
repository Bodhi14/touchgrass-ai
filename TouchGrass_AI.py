import requests
import streamlit as st

st.set_page_config(
    page_title="TouchGrass AI",
    page_icon="🌿",
    layout="centered",
)

API_URL = "https://router.huggingface.co/v1/chat/completions"
MODEL = "openai/gpt-oss-120b:fastest"

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


def generate_quest(prompt):
    token = st.secrets["hf_token"]

    response = requests.post(
        API_URL,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        json={
            "model": MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are TouchGrass AI, a friendly "
                        "outdoor adventure companion. "
                        "Create safe, practical, enjoyable "
                        "outdoor quests. Never invent real "
                        "locations or claim to identify "
                        "wildlife without evidence. "
                        "Keep the response concise."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            "max_tokens": 300,
            "stream": False,
        },
        timeout=120,
    )

    response.raise_for_status()
    result = response.json()

    return result["choices"][0]["message"]["content"]


if st.button("Generate my outdoor quest", type="primary"):
    prompt = f"""
Create a personalized outdoor quest using these details:

Activity: {activity}
Duration: {duration} minutes
Energy level: {energy}
Environment: {environment}

Format the quest with:
1. A creative title
2. A short description
3. Three achievable outdoor tasks
4. One reflection question

Make the quest practical for the selected environment.
Encourage the user to put their phone away after
reading the quest. Prioritize pedestrian and outdoor safety.
"""

    with st.spinner("Creating your outdoor quest..."):
        try:
            mission = generate_quest(prompt)

            st.success("Your quest is ready!")
            st.markdown(mission)

            st.info(
                "Your next mission: head outside, "
                "enjoy the moment, and put your phone away."
            )

        except KeyError:
            st.error(
                "HF_TOKEN is missing from Streamlit Secrets. "
                "Check the secret name and save your settings."
            )

        except requests.Timeout:
            st.error(
                "The AI service took too long to respond. "
                "Please try again."
            )

        except requests.HTTPError as error:
            status = error.response.status_code

            if status == 401 or status == 403:
                st.error(
                    "Authentication failed. Check your "
                    "Hugging Face token and permissions."
                )
            elif status == 402:
                st.error(
                    "The inference provider may require "
                    "additional credits or payment."
                )
            elif status == 429:
                st.error(
                    "The service is busy or rate-limited. "
                    "Please wait and try again."
                )
            else:
                st.error(
                    f"The AI service returned HTTP {status}."
                )

            st.caption(error.response.text[:1000])

        except requests.RequestException:
            st.error(
                "Could not connect to the hosted AI service. "
                "Check your connection and try again."
            )

        except (ValueError, KeyError, IndexError, TypeError):
            st.error(
                "The AI service returned an unexpected response. "
                "Please try again."
            )
import os
import base64
import streamlit as st
from dotenv import load_dotenv
from sarvamai import SarvamAI

load_dotenv()

st.set_page_config(
    page_title="PodGen AI",
    page_icon="🎙️",
    layout="centered"
)

st.title("🎙️ PodGen AI")
st.write("Turn any topic into a podcast with Sarvam AI.")

api_key = os.getenv("SARVAM_API_KEY")



api_key = os.getenv("SARVAM_API_KEY")

if not api_key:
    try:
        api_key = st.secrets["SARVAM_API_KEY"]
    except (KeyError, FileNotFoundError):
        api_key = None

if not api_key:
    st.error("Please configure SARVAM_API_KEY in Streamlit Secrets.")
    st.stop()

client = SarvamAI(api_subscription_key=api_key)

topic = st.text_input(
    "Podcast topic",
    placeholder="e.g. How artificial intelligence is changing education"
)

language = st.selectbox(
    "Podcast language",
    ["English", "Hindi", "Telugu"]
)
podcast_mode = st.selectbox(
    "🎙️ Podcast format",
    ["Solo Host", "Two Hosts"]
)
podcast_style = st.selectbox(
    "🎭 Podcast Style",
    [
        "Educational",
        "Funny & Casual",
        "News Briefing",
        "Storytelling",
        "Tech Talk"
    ]
)
duration = st.selectbox(
    "Podcast length",
    ["Short (30–45 seconds)", "Medium (1–2 minutes)"]
)

if st.button("🎧 Generate Podcast", type="primary"):
    if not topic.strip():
        st.warning("Please enter a topic.")
        st.stop()

    language_codes = {
        "English": "en-IN",
        "Hindi": "hi-IN",
        "Telugu": "te-IN"
    }

    word_limit = 100 if duration.startswith("Short") else 220
    if podcast_mode == "Two Hosts":
        host_instruction = """
        Create a natural conversation between two podcast hosts.

        Host 1: Curious, energetic, and asks interesting questions.
        Host 2: Knowledgeable, friendly, and explains concepts clearly.

        Requirements:
        - Label every spoken line as Host 1 or Host 2.
        - Start with an interesting hook.
        - Let the hosts ask questions and respond to each other.
        - Include relatable examples.
        - Keep the conversation engaging and natural.
        - End with a memorable takeaway.
        """
    else:
        host_instruction = """
        Create an engaging educational podcast with one host.
        Start with an interesting hook.
        Explain the topic conversationally.
        Include a relatable example.
        End with a memorable takeaway.
        """

    prompt = f"""
    Create an engaging podcast about: {topic}

    Language: {language}
    Maximum length: {word_limit} words.
    Podcast format: {podcast_mode}
    Podcast style: {podcast_style}

    Instructions:
    - For Two Hosts, create a natural conversation between Host 1 and Host 2.
    - For Solo Host, write for one narrator.
    - Educational: Explain concepts clearly with examples.
    - Funny & Casual: Use light humor and relatable situations.
    - News Briefing: Use a concise, informative news-anchor tone.
    - Storytelling: Use a compelling narrative and engaging progression.
    - Tech Talk: Discuss technology conversationally with useful insights.
    - Start with an interesting hook.
    - End with a memorable takeaway.
    - Return only the spoken script.
    - Do not include sound effects or stage directions.
    """

    try:
        with st.spinner("✍️ Writing your podcast script..."):
            response = client.chat.completions(
                model="sarvam-105b-conversations",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            script = response.choices[0].message.content.strip()

        st.subheader("📝 Your Podcast Script")
        st.write(script)

        with st.spinner("🎙️ Generating podcast audio..."):
            audio_response = client.text_to_speech.convert(
                text=script[:2400],
                model="bulbul:v4-flash",
                language_code=language_codes[language]
            )

            audio_bytes = base64.b64decode(
                audio_response.audios[0]
            )

        st.subheader("🎧 Listen to Your Podcast")
        st.audio(audio_bytes, format="audio/wav")

        st.download_button(
            label="⬇️ Download Podcast",
            data=audio_bytes,
            file_name="podcast.wav",
            mime="audio/wav"
        )

        st.success("Your podcast is ready!")

    except Exception as e:
        st.error(f"Something went wrong: {e}")

    try:
        with st.spinner("✍️ Writing your podcast script..."):
            response = client.chat.completions(
                model="sarvam-105b-conversations",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            script = response.choices[0].message.content.strip()

        st.subheader("📝 Your Podcast Script")
        st.write(script)

        with st.spinner("🎙️ Generating podcast audio..."):
            audio_response = client.text_to_speech.convert(
                text=script[:2400],
                model="bulbul:v4-flash",
                language_code=language_codes[language]
            )

            audio_bytes = base64.b64decode(
                audio_response.audios[0]
            )

        st.subheader("🎧 Listen to Your Podcast")
        st.audio(audio_bytes, format="audio/wav")

        st.download_button(
            label="⬇️ Download Podcast",
            data=audio_bytes,
            file_name="podcast.wav",
            mime="audio/wav"
        )

        st.success("Your podcast is ready!")

    except Exception as e:
        st.error(f"Something went wrong: {e}")
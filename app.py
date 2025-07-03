import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load the Gemini API key from .env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Error if key is missing
if not GEMINI_API_KEY:
    st.error("Gemini API key not found. Please set GEMINI_API_KEY in your .env file.")
    st.stop()

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

st.set_page_config(page_title="Today's Take", layout="centered")

# Session state to control page flow
if "entry_started" not in st.session_state:
    st.session_state.entry_started = False

# Landing Page
if not st.session_state.entry_started:
    st.markdown("<h1 style='text-align: center;'>🎬 Today’s Take</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center;'>Your day. Your story. Your soundtrack.</h4>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🎧 Write Today’s Take"):
        st.session_state.entry_started = True

# Journal Input Page
else:
    st.markdown("### 💭 Describe your day or a moment in 4–6 lines:")
    journal = st.text_area("Write your emotional scene here...", height=200)

    if st.button("🎬 Generate My Scene"):
        if journal.strip() == "":
            st.warning("Please enter your thoughts.")
        else:
            with st.spinner("Scoring your scene..."):
                prompt = f"""
                You are an emotional soundtrack assistant. Given a user's journal entry, return:

                1. 🎬 A short cinematic scene title (2–5 words)
                2. 🎭 A mood arc: start → middle → end
                3. 🎶 A fitting soundtrack (song title – artist)
                4. 💬 A 1-sentence reflection or prompt

                Entry: {journal}
                """

                try:
                    model = genai.GenerativeModel("gemini-1.5-flash")

                    response = model.generate_content(prompt)
                    output = response.text

                    st.success("Here’s your take 🎞️")
                    st.markdown("---")
                    st.markdown("### 🌟 Scene Breakdown:")
                    st.markdown(output)

                    # Extract and display song with Spotify link
                    for line in output.splitlines():
                        if line.startswith("🎶 Soundtrack:"):
                            song_line = line.replace("🎶 Soundtrack:", "").strip()
                            break
                    else:
                        song_line = ""

                    if "–" in song_line:
                        title, artist = [s.strip() for s in song_line.split("–", 1)]
                    else:
                        title, artist = song_line.strip(), ""

                    if title:
                        query = f"{title} {artist}".replace(" ", "+")
                        spotify_link = f"https://open.spotify.com/search/{query}"
                        st.markdown("### 🎧 Your Soundtrack")
                        st.markdown(f"**🎵 {title}**")
                        st.markdown(f"**👤 {artist}**")
                        st.markdown(f"[Listen on Spotify]({spotify_link})", unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"❌ An error occurred: {e}")

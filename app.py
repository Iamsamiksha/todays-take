import streamlit as st
import google.generativeai as genai
import os
import time
from dotenv import load_dotenv

# Load API key
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    st.error("Gemini API key not found. Please set GEMINI_API_KEY in your .env file.")
    st.stop()

genai.configure(api_key=GEMINI_API_KEY)

# Page config
st.set_page_config(page_title="Today's Take", layout="centered")

# Custom CSS Styling
st.markdown("""
   <style>
html, body, [class*="css"] {
    font-family: 'Quicksand', sans-serif;
    background: linear-gradient(to bottom right, #fdfbfb, #ebedee) !important;
    color: #2c3e50;
}

/* 📝 Textarea */
.stTextArea textarea {
    background-color: #ffffff;
    border-radius: 14px;
    padding: 12px;
    font-size: 16px;
    border: 1px solid #dfe6e9;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
}

/* 🎧 Button with MoodScale gradient */
.stButton > button {
    font-size: 1.2rem;
    padding: 0.9rem 2rem;
    background: linear-gradient(to right,
        #9b59b6,
        #3498db,
        #1abc9c,
        #2ecc71,
        #f1c40f,
        #f39c12,
        #e67e22,
        #e74c3c,
        #c0392b
    );
    color: white;
    font-weight: 600;
    border: none;
    border-radius: 14px;
    transition: all 0.3s ease;
    background-size: 400% 100%;
    animation: gradientFlow 8s ease infinite;
    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.1);
}

@keyframes gradientFlow {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.stButton > button:hover {
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
}

/* ✨ Fade In */
.fade-in {
    animation: fadeIn 1s ease-in-out;
}

@keyframes fadeIn {
    0% { opacity: 0; transform: translateY(15px); }
    100% { opacity: 1; transform: translateY(0); }
}
</style>
""", unsafe_allow_html=True)

# State initialization
for key in ["entry_started", "show_scene", "output", "song_title", "song_artist", "spotify_link"]:
    if key not in st.session_state:
        st.session_state[key] = False if "show" in key or "entry" in key else ""

# 🏠 Landing Page
if not st.session_state.entry_started and not st.session_state.show_scene:
    st.markdown("""
    <div class="fade-in" style="
        min-height: 40vh;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        padding: 2px;
    ">
        <div style="
            background: rgba(255, 255, 255, 0.6);
            padding: 3rem;
            border-radius: 20px;
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(8px);
            max-width: 700px;
            width: 100%;
        ">
            <h1 style="font-size: 3.2rem; font-weight: 800; margin-bottom: 0.4em; color: #2b9adf;">🎬Today’s Take</h1>
            <h4 style="font-style: italic; font-size: 1.4rem; margin-bottom: 1.5rem; color: #5f0f40;">
                Your day. Your story. Your soundtrack.
            </h4>
            <p style="font-size: 1.1rem; color: #2e2e2e; margin-bottom: 2rem;">
                ✨ Reflect on your day, and we’ll turn it into a cinematic moment with a fitting soundtrack to match your mood.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🎧 What's Your Take Today?"):
            st.session_state.entry_started = True
            st.rerun()

# ✍️ Journal Input Page
elif st.session_state.entry_started and not st.session_state.show_scene:
    st.markdown("### 💭 Describe the moment of the day :")
    mood = st.selectbox("🎭 How are you feeling?", ["Happy", "Sad", "Angry", "Calm", "Anxious", "Mixed"])
    journal = st.text_area("Narrate us your story here...", height=200)

    if st.button("🎬 Generate My Scene"):
        if journal.strip() == "":
            st.warning("Please enter your thoughts.")
        else:
            with st.spinner("Scoring your scene... 🎥"):
                try:
                    prompt = f"""
You are a creative emotional soundtrack assistant. 
Given a user's journal entry and selected mood, analyze the tone, themes, and emotional flow of their writing.
Respond strictly in the following format (with no extra lines, no explanations):

🎬 Scene Title: <A short, creative and cinematic title capturing the essence of the moment>
🎭 Mood Arc: <A three-part mood journey like calm → anxious → hopeful>
🎶 Soundtrack: <A matching song with same vibe – artist that fits the emotional tone and story>
💬 Reflection: <A single-sentence easily understandable  insight, question, or comforting message based on the entry>


Entry: {journal}
Mood: {mood}
"""

                    model = genai.GenerativeModel("gemini-1.5-flash")
                    response = model.generate_content(prompt)

                    output = response.text
                    st.session_state.output = output

                    song_line = ""
                    for line in output.splitlines():
                        if "🎶" in line:
                            song_line = line.replace("🎶", "").replace("Soundtrack:", "").strip()
                            break

                    if "–" in song_line:
                        title, artist = [s.strip() for s in song_line.split("–", 1)]
                    else:
                        title, artist = song_line.strip(), ""

                    st.session_state.song_title = title
                    st.session_state.song_artist = artist
                    st.session_state.spotify_link = f"https://open.spotify.com/search/{title.replace(' ', '+')}+{artist.replace(' ', '+')}"
                    st.session_state.show_scene = True

                    time.sleep(0.8)
                    st.rerun()

                except Exception as e:
                    st.error(f"❌ An error occurred while generating: {e}")

# 🎬 Scene Output Page
elif st.session_state.show_scene:
    scene_text = st.session_state.output
    song_title = st.session_state.song_title
    song_artist = st.session_state.song_artist
    spotify_link = st.session_state.spotify_link

    scene_title = mood_arc = reflection = "Not available"

    for line in scene_text.splitlines():
        if "🎬" in line:
            scene_title = line.replace("🎬", "").replace("Scene Title:", "").strip()
        elif "🎭" in line:
            mood_arc = line.replace("🎭", "").replace("Mood Arc:", "").strip()
        elif "💬" in line:
            reflection = line.replace("💬", "").replace("Reflection:", "").strip()

    st.markdown("### 🌟 Your Cinematic Take")
    st.markdown(f"""
    <div class="fade-in" style='
        background-color: #fefcff;
        padding: 0.5rem;
        border-radius: 9px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        font-size: 16px;
        line-height: 1.6;
        color: #2e2c52;
    '>
        <h3>🎬 <b>Scene Title:</b> {scene_title}</h3>
        <p>🎭 <b>Mood Arc:</b> {mood_arc}</p>
        <p>💬 <b>Reflection:</b> <i>{reflection}</i></p>
    </div>
    """, unsafe_allow_html=True)

    if song_title:
        st.markdown("### 🎧 Your Soundtrack")
        st.markdown(f"""
        <div class="fade-in" style='
            background-color: #e9ddff;
            padding: 1.2rem;
            border-radius: 10px;
            margin-top: 1rem;
            font-size: 16px;
            color: #1c1b3a;
        '>
            <h4>🎵 <b>{song_title}</b></h4>
            <p>👤 <i>{song_artist}</i></p>
            <a href='{spotify_link}' target='_blank' style='font-weight: bold; color: #3f37c9;'>▶️ Listen on Spotify</a>
            <p style='margin-top: 0.5rem; font-style: italic;'>Plug in. Close your eyes. Let this soothe your soul.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)

    if st.button("🔁 Try Another"):
        for key in st.session_state.keys():
            st.session_state[key] = False if isinstance(st.session_state[key], bool) else ""
        st.rerun()
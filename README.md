# 🎬 Today’s Take

**Your day. Your story. Your soundtrack.**

_What if your daily emotions were scenes in a movie? And every scene had the perfect soundtrack?_

**Today’s Take** is a fun and therapeutic Streamlit app that transforms your journal entry into a cinematic moment — complete with:

- 🎬 A movie-style **scene title**
- 🎭 An emotional **mood arc** (start → middle → end)
- 🎶 A matching **soundtrack** (with Spotify link)
- 💬 A thoughtful **reflection prompt**

---

## 🧠 How It Works

1. ✍️ You write a short journal entry (about your day, mood, or a moment).
2. 🤖 The app sends it to **Gemini 1.5 Flash** (Google’s LLM) with a custom prompt.
3. 📽️ It responds with your **scene title, mood arc, song, and reflection.**
4. 🎧 We extract the song and link it directly to **Spotify search**.

---

## 🛠 Built With

- [Streamlit](https://streamlit.io/) – front-end UI
- [Gemini Flash API](https://ai.google.dev/) – for scene + song generation
- [Spotify Search](https://open.spotify.com/) – for instant music link
- [Python dotenv](https://pypi.org/project/python-dotenv/) – for API key management

---

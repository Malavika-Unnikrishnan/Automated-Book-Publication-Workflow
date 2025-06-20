# 📖 Automated Book Publication Workflow 🚀  
*A modular, AI‑powered pipeline that turns any online chapter into polished, multi‑version text (and audio!) with human‑in‑the‑loop control, semantic search, RL‑style ranking, and visual diffing — all behind a friendly Streamlit interface.*

---

> 💡 **Demo video** ▶️ https://www.loom.com/share/9767e935e7cd4e38b8fd2497e8a92bdc?sid=543b2dcd-552d-48fa-ac76-13251830b276


![Screenshot 2025-06-20 225424](https://github.com/user-attachments/assets/1db93dd5-82cf-48ea-9cdc-da54c0ca074b)

## ✨ What this project does

| Stage                    | Key Magic                                                       |
|--------------------------|------------------------------------------------------------------|
| **1. Scrape & Screenshot** | Fetch chapter content + full‑page PNG using Playwright          |
| **2. AI Writer**           | Gemini  “spins” the text in your chosen style/tone      |
| **3. AI Reviewer**         | Second pass cleans grammar & flow                              |
| **4. Human Edit**          | Editable textbox for final tweaks                              |
| **5. Voice Narration**     | One‑click 🔊 TTS for every version (original → final)           |
| **6. Versioning**          | All drafts stored in ChromaDB with rich metadata               |
| **7. RL‑Style Search**     | Semantic retrieval + cosine‑reward ranking                     |
| **8. Diff Viewer**         | Unified `diff` of any two saved versions                       |
| **9. Agentic API**         | Clean Writer → Reviewer → Human agent flow                     |


---

## 🏗 Architecture at a Glance

| Section               | What to Do                                                     |
|------------------------|----------------------------------------------------------------|
| 🔍 **Scrape**          | Paste Wikisource URL, extract text and screenshot             |
| ✍️ **Rewrite**         | Select style and tone, generate spun version                  |
| 🧠 **Review**          | Proofread and polish using second agent pass                  |
| 🧑‍💻 **Final Edit**     | Human edits in editor box + 🔊 TTS narration                   |
| ✅ **Save**            | Push final & drafts into ChromaDB                             |
| 🔎 **RL‑Style Search** | Retrieve versions using cosine similarity ranking             |
| 🧬 **Diff Viewer**     | Pick 2 versions → view unified inline differences              |






## 🛠 Tech Stack

- **Python 3.11**
- **Streamlit** UI
- **Playwright** for scraping & screenshots
- **Gemini 2.5** (or OpenAI GPT‑4o fallback)
- **ChromaDB** vector store
- **Sentence-Transformers** (`all‑MiniLM‑L6‑v2`)
- **gTTS** for text-to-speech
- **difflib** for version diffs

---

## 🚀 Getting Started


git clone https://github.com/Malavika-Unnikrishnan/Automated-Book-Publication-Workflow.git
pip install -r requirements.txt

# One-time browser install
playwright install

## 🔐 Environment Variables

| Variable         | Description                               |
|------------------|-------------------------------------------|
| `GEMINI_API_KEY` | Your Google Generative AI key             |

🏃‍♂️ Run the App
streamlit run streamlit_app.py




## 🔬 How RL‑Style Search Works

- Embeds both the query and stored versions using `all-MiniLM-L6-v2`
- Calculates **cosine similarity** as a reward score (range: 0 to 1)
- Ranks and retrieves the **top‑k most relevant** past versions
- ⚠️ *Note:* This is not a trained RL policy — it simulates a **lightweight reward optimization** strategy

---

## 🧠 Diff Viewer

- Uses Python's `difflib.unified_diff` to compute inline differences
- Shows **inline, color-coded text changes** between two versions
- Pick any two versions from dropdowns → instantly compare them visually

---

## 🔊 Voice Narration

- Converts all text blocks (original → final) into `.mp3` files
- Uses `gTTS` and **caches audio** in the `data/audio/` directory
- Streamlit's built-in audio player is used to playback the narration seamlessly








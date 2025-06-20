# streamlit_app.py
import streamlit as st
from datetime import datetime
from scraper import get_chapter_text_and_image
from ai_writer import generate_ai_version, review_text
from db_handler import save_version, search_versions, reward_score,collection
from audio_utils import text_to_mp3  # ✅ NEW

# ---------------- BASIC PAGE CONFIG ----------------
st.set_page_config(page_title="AI Book Rewriter",
                   page_icon="📖",
                   layout="wide")
st.title("📖 Automated Book Publication Workflow")

# ---------------- AUDIO HELPER ---------------------
def audio_button(key_prefix: str, text: str):
    """Renders a 🔊 button and, if clicked, plays audio of `text`."""
    audio_key = f"{key_prefix}_audio"
    if st.button(f"🔊 Narrate", key=audio_key):
        try:
            mp3_path = text_to_mp3(text)
            st.audio(mp3_path)
        except Exception as e:
            st.error(f"Audio generation failed: {e}")

# -------------  INIT SESSION STATE -----------------
for key in ["chapter_text", "rewritten_text",
            "reviewed_text", "final_text",
            "title", "url"]:
    st.session_state.setdefault(key, "")

# ---------------- SIDEBAR INPUTS -------------------
st.sidebar.header("🔧 Rewrite Settings")

url = st.sidebar.text_input(
    "Enter Chapter URL",
    value=st.session_state.url or
          "https://en.wikisource.org/wiki/The_Gates_of_Morning/Book_1/Chapter_1"
)

style = st.sidebar.selectbox(
    "Select Rewrite Style",
    ["default", "formal", "creative"],
    index=0
)

tone = st.sidebar.text_input(
    "Optional Tone (e.g. 'mysterious', 'joyful')",
    value=""
)

auto_save_drafts = st.sidebar.checkbox(
    "Auto‑save original / rewritten / reviewed drafts to DB",
    value=False
)

# ---------------- ACTION BUTTONS -------------------
col_scrape, col_rewrite, col_review, col_reset = st.columns(4)

with col_scrape:
    if st.button("🔍 Scrape Chapter"):
        with st.spinner("Scraping content..."):
            text, title, screenshot_path = get_chapter_text_and_image(url)
            st.session_state.update({
                "chapter_text": text,
                "title": title,
                "url": url
            })
            st.success(f"✅ Chapter '{title}' scraped.")
            if auto_save_drafts:
                save_version("original", text, {
                    "title": title, "source_url": url
                })

with col_rewrite:
    if st.button("✍️ Rewrite with AI"):
        if st.session_state.chapter_text:
            with st.spinner("Generating rewritten text..."):
                st.session_state.rewritten_text = generate_ai_version(
                    st.session_state.chapter_text,
                    style=style,
                    tone=tone or None
                )
                st.success("✅ Rewritten text generated.")
                if auto_save_drafts:
                    save_version("rewritten", st.session_state.rewritten_text, {
                        "title": st.session_state.title,
                        "style": style,
                        "tone": tone,
                        "source_url": url
                    })
        else:
            st.warning("⚠️ Scrape a chapter first.")

with col_review:
    if st.button("🧠 Review & Refine"):
        if st.session_state.rewritten_text:
            with st.spinner("Reviewing text..."):
                st.session_state.reviewed_text = review_text(
                    st.session_state.rewritten_text
                )
                st.success("✅ Reviewed text ready.")
                if auto_save_drafts:
                    save_version("reviewed", st.session_state.reviewed_text, {
                        "title": st.session_state.title,
                        "style": style,
                        "tone": tone,
                        "source_url": url
                    })
        else:
            st.warning("⚠️ Generate rewritten text first.")

with col_reset:
    if st.button("♻️ Reset All"):
        for k in st.session_state.keys():
            st.session_state[k] = ""
        st.experimental_rerun()

# ---------------- DISPLAY THREE VERSIONS -----------
st.subheader("📚 Content Preview")
col_orig, col_spin, col_rev = st.columns(3)

with col_orig:
    st.markdown("### 📝 Original")
    st.text_area(
        "Original Text",
        value=st.session_state.chapter_text,
        height=350,
        key="ta_orig",
        disabled=True
    )
    audio_button("orig", st.session_state.chapter_text)  # 🔊

with col_spin:
    st.markdown("### ✍️ AI Rewritten")
    st.text_area(
        "Rewritten Text",
        value=st.session_state.rewritten_text,
        height=350,
        key="ta_spin",
        disabled=True
    )
    audio_button("spin", st.session_state.rewritten_text)  # 🔊

with col_rev:
    st.markdown("### 🧠 AI Reviewed")
    st.text_area(
        "Reviewed Text",
        value=st.session_state.reviewed_text,
        height=350,
        key="ta_rev",
        disabled=True
    )
    audio_button("rev", st.session_state.reviewed_text)  # 🔊

# ---------------- FINAL HUMAN EDIT -----------------
st.markdown("### 🧑‍💻 Final Human‑Editable Version")
st.session_state.final_text = st.text_area(
    "Edit and finalize here",
    value=(st.session_state.reviewed_text or
           st.session_state.rewritten_text),
    height=250
)
audio_button("final", st.session_state.final_text)  # 🔊

# ------------- SAVE FINAL TO CHROMADB --------------
if st.button("✅ Approve & Save Final Version"):
    if st.session_state.final_text.strip():
        save_version(
            "final",
            st.session_state.final_text,
            {
                "title": st.session_state.title,
                "style": style,
                "tone": tone,
                "source_url": url,
                "edited_by": "human",
                "approved_at": datetime.utcnow().isoformat()
            }
        )
        with open("data/final_output.txt", "w", encoding="utf-8") as f:
            f.write(st.session_state.final_text)
        st.success("🎉 Final version saved to ChromaDB and `data/final_output.txt`.")
    else:
        st.warning("⚠️ Final text is empty!")

# ------------------ RL‑STYLE SEARCH ----------------
st.markdown("---")
st.header("🔎 RL‑Style Version Search")

query = st.text_input(
    "Search for past versions (enter a phrase or sentence)",
    value=""
)
top_k = st.slider("Number of results", 1, 10, 3)

if st.button("🚀 Search Versions"):
    if not query.strip():
        st.warning("⚠️ Enter a query.")
    else:
        with st.spinner("Searching ChromaDB..."):
            results = search_versions(query, top_k=top_k)
        docs = results["documents"][0]
        metas = results["metadatas"][0]

        if not docs:
            st.info("No matches found yet.")
        else:
            for doc, meta in zip(docs, metas):
                reward = reward_score(doc, query)
                with st.expander(
                    f"📄 {meta['version_type'].upper()} "
                    f"• {meta.get('title','unknown')} "
                    f"• Similarity={reward:.3f}"
                ):
                    st.markdown(f"**Metadata:** {meta}")
                    st.write(doc)
                    audio_button(f"search_{meta.get('version_type','na')}_{meta.get('timestamp','')}", doc)  # 🔊


# ------------------ DIFF VIEWER ---------------------
# ------------------ DIFF VIEWER ---------------------
import difflib
st.markdown("---")
st.header("🧬 Version Difference Viewer")

# Fetch all saved versions
all_versions = collection.get()
version_text_map = {}
version_labels = []

for doc, meta in zip(all_versions["documents"], all_versions["metadatas"]):
    label = f"{meta.get('version_type','?').upper()} | {meta.get('title','?')} | {meta.get('timestamp','')[:19]}"
    version_labels.append(label)
    version_text_map[label] = doc

if len(version_labels) < 2:
    st.info("Need at least 2 saved versions to compare.")
else:
    col1, col2 = st.columns(2)
    with col1:
        version_a = st.selectbox("🔵 Version A", version_labels, key="va")
    with col2:
        version_b = st.selectbox("🟠 Version B", version_labels, key="vb", index=1)

    if st.button("🧪 Compare Versions"):
        text_a = version_text_map[version_a].splitlines()
        text_b = version_text_map[version_b].splitlines()
        diff = difflib.unified_diff(text_a, text_b, fromfile="Version A", tofile="Version B", lineterm="")
        diff_output = "\n".join(diff)

        if not diff_output.strip():
            st.success("✅ No differences found!")
        else:
            st.code(diff_output, language="diff")

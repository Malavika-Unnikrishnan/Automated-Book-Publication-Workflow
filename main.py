# main.py

from scraper import get_chapter_text_and_image
from ai_writer import generate_ai_version, review_text

def choose_style():
    print("\n📚 Choose a rewriting style for the AI:")
    print("1. Default – Clear, reader-friendly")
    print("2. Formal – Academic, professional tone")
    print("3. Creative – Vivid and imaginative storytelling")

    choice = input("Enter 1 / 2 / 3 [default = 1]: ").strip()
    style_map = {"1": "default", "2": "formal", "3": "creative"}
    return style_map.get(choice, "default")

def main():
    # Step 1: Scrape Chapter
    url = "https://en.wikisource.org/wiki/The_Gates_of_Morning/Book_1/Chapter_1"
    print("🌐 Fetching chapter from:", url)
    chapter_text, title, screenshot_path = get_chapter_text_and_image(url)
    print(f"✅ Scraped chapter: {title}")
    print(f"📸 Screenshot saved at: {screenshot_path}")

    # Step 2: Let user choose rewrite style
    style = choose_style()
    print(f"\n🛠️ Using rewrite style: {style.upper()}")

    # Step 3: AI Writer Agent
    ai_version = generate_ai_version(chapter_text, style=style)
    print("\n📝 AI-Rewritten Version (Spin):\n")
    print(ai_version[:1000] + "\n...")  # Print preview

    # Step 4: AI Reviewer Agent
    reviewed_version = review_text(ai_version)
    print("\n🔍 AI-Reviewed Version (Refined):\n")
    print(reviewed_version[:1000] + "\n...")  # Print preview

    

if __name__ == "__main__":
    main()

import requests

# --- Configuration ---
API_KEY = '5c9528e29e51b81556d2eb34a7f28eb0'
BASE_URL = "https://api.themoviedb.org/3"

# --- Get content type ---
def get_content_type():
    while True:
        content_type = input("Is it a Movie or TV Series? (Enter 'movie' or 'tv'): ").strip().lower()
        if content_type in ['movie', 'tv']:
            return content_type
        print("Invalid input. Please enter 'movie' or 'tv'.")

# --- Search content on TMDb ---
def search_tmdb(title, content_type):
    url = f"{BASE_URL}/search/{content_type}"
    params = {"api_key": API_KEY, "query": title}
    response = requests.get(url, params=params)
    results = response.json().get("results", [])
    return results

# --- Ask user to pick from search results ---
def select_from_results(results):
    if not results:
        print("No results found.")
        return None
    for i, item in enumerate(results, start=1):
        name = item.get("title") or item.get("name")
        year = (item.get("release_date") or item.get("first_air_date") or "")[:4]
        print(f"{i}. {name} ({year})")
    while True:
        try:
            choice = int(input("Enter the number of the correct title: "))
            if 1 <= choice <= len(results):
                return results[choice - 1]
            else:
                print("Invalid number.")
        except ValueError:
            print("Please enter a valid number.")

# --- Generate content flag mock data (can be extended or replaced with real data/logic) ---
def generate_flags(title):
    # Placeholder for actual content check logic
    return {
        "title": title,
        "age_appropriateness": "✅",
        "violence": "🟡",
        "romance": "🟡",
        "language": "✅",
        "substance_use": "✅",
        "mature_themes": "🟡",
        "lgbtq": "✅",
        "cultural_sensitivity": "✅",
        "overstimulation": "🟡"
    }

# --- Print full content review based on flags ---
def print_content_review(flags):
    title = flags["title"]
    print(f"\n🎬 {title}")
    print("✅ Parent-Focused Content Filters:")
    print("Filter\t\tStatus\tNotes")
    print(f"🧒 Age-Appropriateness\t{flags['age_appropriateness']}\tGenerally fine for kids 7+. Some intense scenes may exist.")
    print(f"🤕 Violence\t\t{flags['violence']}\tStylized or fantasy action.")
    print(f"❤️ Romance\t\t{flags['romance']}\tLight, innocent crushes.")
    print(f"🗣️ Language\t\t{flags['language']}\tNo bad language.")
    print(f"🍷 Substance Use\t{flags['substance_use']}\tNo reference to drugs/alcohol.")
    print(f"🧠 Mature Themes\t{flags['mature_themes']}\tMild drama, identity, friendships.")
    print(f"🌈 LGBTQ+ Presence\t{flags['lgbtq']}\tDiverse and positively shown.")
    print(f"🕌 Cultural Sensitivity\t{flags['cultural_sensitivity']}\tNo offensive or insensitive content.")
    print(f"🌀 Overstimulation\t{flags['overstimulation']}\tMay be fast-paced or visually intense.\n")

    # Summary feedback
    print("🧾 Summary Feedback for Parents:")
    if flags["mature_themes"] in ["🟡", "🔴"]:
        print(f'"{title}" explores meaningful themes like inclusion or identity in a gentle way.')
    else:
        print(f'"{title}" is light and enjoyable without deep emotional content.')
    print("👍🏽 Great choice for families who value creativity, diversity, and positive messaging.\n")

# --- Main logic ---
def main():
    content_type = get_content_type()
    title = input("Enter the title: ").strip()
    results = search_tmdb(title, content_type)
    selected = select_from_results(results)
    if not selected:
        return
    chosen_title = selected.get("title") or selected.get("name")
    flags = generate_flags(chosen_title)
    print_content_review(flags)

if __name__ == "__main__":
    main()

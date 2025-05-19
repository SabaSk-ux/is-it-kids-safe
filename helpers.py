import requests

API_KEY = '5c9528e29e51b81556d2eb34a7f28eb0'
BASE_URL = "https://api.themoviedb.org/3"

def search_tmdb(title, content_type):
    url = f"{BASE_URL}/search/{content_type}"
    params = {"api_key": API_KEY, "query": title}
    response = requests.get(url, params=params)
    results = response.json().get("results", [])
    return results

def generate_flags(title):
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

import requests
import os
from dotenv import load_dotenv
import openai

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
openai.api_key = os.getenv("OPENAI_API_KEY")

def search_tmdb(title, media_type):
    url = f"https://api.themoviedb.org/3/search/{media_type}"
    params = {"api_key": TMDB_API_KEY, "query": title}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        return []

def get_tmdb_overview(item_id, media_type):
    url = f"https://api.themoviedb.org/3/{media_type}/{item_id}"
    params = {"api_key": TMDB_API_KEY, "language": "en-US"}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("overview", "")
    return ""

def analyze_with_openai(title, overview):
    prompt = f"""
You are a parental content advisor. Based on the overview below of "{title}", provide a review focused on safety for children.

Overview:
"{overview}"

Respond ONLY in this JSON format:
{{
  "age_appropriateness": "✅ / 🟡 / 🔴",
  "violence": "✅ / 🟡 / 🔴",
  "romance": "✅ / 🟡 / 🔴",
  "language": "✅ / 🟡 / 🔴",
  "substance_use": "✅ / 🟡 / 🔴",
  "mature_themes": "✅ / 🟡 / 🔴",
  "lgbtq": "✅ / 🟡 / 🔴",
  "cultural_sensitivity": "✅ / 🟡 / 🔴",
  "overstimulation": "✅ / 🟡 / 🔴",
  "summary": "Short one-paragraph feedback for parents"
}}
    """.strip()

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=500
    )

    content = response.choices[0].message.content.strip()
    import json
    try:
        return json.loads(content)
    except:
        return None

import streamlit as st
from helpers import search_tmdb, generate_flags

def get_kids_safe_review(title, media_type):
    results = search_tmdb(title, media_type)
    if not results:
        st.warning("No results found.")
        return

    options = []
    for item in results:
        name = item.get("title") or item.get("name")
        year = (item.get("release_date") or item.get("first_air_date") or "")[:4]
        options.append(f"{name} ({year})")

    selected_option = st.selectbox("Select the correct title:", options)
    selected_index = options.index(selected_option)
    selected = results[selected_index]
    chosen_title = selected.get("title") or selected.get("name")

    flags = generate_flags(chosen_title)

    st.subheader(f"🎬 {chosen_title}")
    st.markdown("✅ **Parent-Focused Content Filters:**")
    st.write(f"🧒 Age-Appropriateness: {flags['age_appropriateness']}")
    st.write(f"🤕 Violence: {flags['violence']}")
    st.write(f"❤️ Romance: {flags['romance']}")
    st.write(f"🗣️ Language: {flags['language']}")
    st.write(f"🍷 Substance Use: {flags['substance_use']}")
    st.write(f"🧠 Mature Themes: {flags['mature_themes']}")
    st.write(f"🌈 LGBTQ+ Presence: {flags['lgbtq']}")
    st.write(f"🕌 Cultural Sensitivity: {flags['cultural_sensitivity']}")
    st.write(f"🌀 Overstimulation: {flags['overstimulation']}")

    st.markdown("### 🧾 Summary Feedback for Parents:")
    if flags["mature_themes"] in ["🟡", "🔴"]:
        st.write(f'"{chosen_title}" explores meaningful themes like inclusion or identity in a gentle way.')
    else:
        st.write(f'"{chosen_title}" is light and enjoyable without deep emotional content.')
    st.success("👍🏽 Great choice for families who value creativity, diversity, and positive messaging.")

# Streamlit UI
st.title("🎥 Is it Kid-Safe?")
title = st.text_input("Enter the movie or TV series title:")
media_type = st.selectbox("Select content type:", ["movie", "tv"])

if title and media_type:
    get_kids_safe_review(title, media_type)

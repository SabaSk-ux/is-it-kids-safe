import streamlit as st
from helpers import search_tmdb, get_tmdb_overview, analyze_with_openai

st.set_page_config(page_title="Is It Kid-Safe?", page_icon="🎬")

st.title("🎥 Is it Kid-Safe?")
st.markdown("Check if a movie or series is suitable for kids based on real content analysis.")

title = st.text_input("Enter the movie or TV series title:")
media_type = st.selectbox("Select content type:", ["movie", "tv"])

if title:
    results = search_tmdb(title, media_type)
    if results:
        options = []
        for item in results:
            name = item.get("title") or item.get("name")
            year = (item.get("release_date") or item.get("first_air_date") or "")[:4]
            options.append(f"{name} ({year})")

        selected_option = st.selectbox("Select the correct title:", options)
        selected_index = options.index(selected_option)
        selected_item = results[selected_index]

        if st.button("Check now"):
            with st.spinner("Analyzing..."):
                overview = get_tmdb_overview(selected_item["id"], media_type)
                if not overview:
                    st.error("No description available for analysis.")
                else:
                    result = analyze_with_openai(selected_option, overview)
                    if not result:
                        st.error("Failed to analyze content.")
                    else:
                        st.subheader(f"🎬 {selected_option}")
                        st.markdown("✅ **Parent-Focused Content Filters:**")
                        st.write(f"🧒 Age-Appropriateness: {result['age_appropriateness']}")
                        st.write(f"🤕 Violence: {result['violence']}")
                        st.write(f"❤️ Romance: {result['romance']}")
                        st.write(f"🗣️ Language: {result['language']}")
                        st.write(f"🍷 Substance Use: {result['substance_use']}")
                        st.write(f"🧠 Mature Themes: {result['mature_themes']}")
                        st.write(f"🌈 LGBTQ+ Presence: {result['lgbtq']}")
                        st.write(f"🕌 Cultural Sensitivity: {result['cultural_sensitivity']}")
                        st.write(f"🌀 Overstimulation: {result['overstimulation']}")

                        st.markdown("### 🧾 Summary Feedback for Parents:")
                        st.info(result["summary"])
    else:
        st.warning("No results found.")

import streamlit as st

from extractor import build_chain, extract_movie_info

st.set_page_config(
    page_title="Movie Information Extractor",
    page_icon="🎬",
    layout="centered",
)


@st.cache_resource
def get_chain():
    return build_chain()


st.title("🎬 Movie Information Extractor")
st.write("Enter a movie paragraph to extract structured information.")

paragraph = st.text_area(
    "Movie Paragraph",
    placeholder="Enter or paste a movie paragraph here...",
    height=200,
)

if st.button("Extract Information", use_container_width=True):
    if not paragraph.strip():
        st.warning("Please enter a movie paragraph.")
    else:
        with st.spinner("Extracting movie information..."):
            try:
                info = extract_movie_info(paragraph, chain=get_chain())
            except Exception as e:
                st.error(f"Error: {e}")
            else:
                st.subheader("Extracted Movie Information")
                st.write("**Movie Title:**", info.title)
                st.write("**Release Year:**", info.release_year or "Not mentioned")
                st.write("**Genre:**", ", ".join(info.genre) or "Not mentioned")
                st.write("**Director:**", info.director or "Not mentioned")
                st.write("**Cast:**", ", ".join(info.cast) or "Not mentioned")
                st.write(
                    "**Rating:**",
                    info.rating if info.rating is not None else "Not mentioned",
                )
                st.write("**Synopsis:**", info.synopsis)

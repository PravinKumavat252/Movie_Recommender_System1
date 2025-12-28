import pickle
import streamlit as st
import requests
from datetime import datetime

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="centered"   # 🔥 IMPORTANT FIX
)

# ---------------- FIXED CSS ----------------
st.markdown("""
<style>
/* Global */
.stApp {
    background: radial-gradient(circle at top, #151533, #0b0b1e);
    color: white;
    font-family: Inter, sans-serif;
}

/* Hide default UI */
#MainMenu, footer, header {visibility: hidden;}

/* App width control */
.block-container {
    max-width: 1100px;
    padding-top: 1.2rem;
}

/* Header */
.hero {
    text-align: center;
    margin-bottom: 1.2rem;
}
.hero h1 {
    font-size: 2.2rem;
    font-weight: 800;
    background: linear-gradient(90deg, #8b5cf6, #ec4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.2rem;
}
.hero p {
    color: #9ca3af;
    font-size: 0.95rem;
}

/* Button */
.stButton button {
    width: 100%;
    text-align: center;
    border-radius: 12px;
    font-weight: 600;
    background: linear-gradient(90deg, #8b5cf6, #ec4899);
    border: none;
}

/* Movie Card */
.movie-card {
    background: rgba(255,255,255,0.06);
    border-radius: 14px;
    padding: 0.7rem;
    text-align: center;
}

.movie-card img {
    width: 100%;
    height: 170px;        /* 🔥 FIXED HEIGHT */
    object-fit: cover;
    border-radius: 10px;
}

.movie-title {
    font-size: 0.9rem;
    font-weight: 600;
    margin-top: 0.5rem;
}

.movie-info {
    font-size: 0.75rem;
    color: #9ca3af;
}

.stars {
    color: #fbbf24;
    font-size: 0.8rem;
}

/* Footer */
.footer {
    text-align: center;
    font-size: 0.8rem;
    color: #9ca3af;
    margin-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

# ---------------- FUNCTIONS ----------------
def fetch_poster(movie_id):
    try:
        data = requests.get(
            f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8",
            timeout=5
        ).json()
        if data.get("poster_path"):
            return "https://image.tmdb.org/t/p/w500" + data["poster_path"]
    except:
        pass
    return "https://via.placeholder.com/300x450?text=No+Image"

def fetch_details(movie_id):
    try:
        data = requests.get(
            f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8",
            timeout=5
        ).json()
        return data.get("vote_average", 0), data.get("release_date", "")[:4]
    except:
        return 0, "N/A"

def stars(r):
    return "★" * int(r//2) + "☆" * (5-int(r//2))

def recommend(movie, movies, similarity, n):
    idx = movies[movies["title"] == movie].index[0]
    distances = sorted(enumerate(similarity[idx]), reverse=True, key=lambda x: x[1])
    recs = []
    for i in distances[1:n+1]:
        movie_id = movies.iloc[i[0]].movie_id
        rating, year = fetch_details(movie_id)
        recs.append({
            "title": movies.iloc[i[0]].title,
            "poster": fetch_poster(movie_id),
            "rating": rating,
            "year": year
        })
    return recs

def display_movies(movies):
    cols = st.columns(4)   # 🔥 PERFECT SIZE
    for i, movie in enumerate(movies):
        with cols[i % 4]:
            st.markdown("<div class='movie-card'>", unsafe_allow_html=True)
            st.image(movie["poster"])
            st.markdown(f"<div class='movie-title'>{movie['title']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='stars'>{stars(movie['rating'])}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='movie-info'>{movie['year']}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    movies = pickle.load(open(
        r"C:\Users\ACER\Desktop\PRAVIN\Deployment\Movie Recommender System\model\movie_list.pkl","rb"))
    similarity = pickle.load(open(
        r"C:\Users\ACER\Desktop\PRAVIN\Deployment\Movie Recommender System\model\similarity.pkl","rb"))
    return movies, similarity

movies, similarity = load_data()

# ---------------- UI ----------------
st.markdown("""
<div class="hero">
    <h1>🎬 Movie Recommendation System</h1>
    <p>Find movies similar to your favorites</p>
</div>
""", unsafe_allow_html=True)

selected_movie = st.selectbox("Select a movie", movies["title"].values)
num = st.slider("Recommendations", 4, 8, 4)

if st.button("🎥 Get Recommendations"):
    with st.spinner("Finding movies..."):
        recs = recommend(selected_movie, movies, similarity, num)
        st.markdown(f"### Because you liked **{selected_movie}**")
        display_movies(recs)

st.markdown(f"""
<div class="footer">
Built by <b>Pravin Kumavat</b> • BCA • Data Science <br>
© {datetime.now().year}
</div>
""", unsafe_allow_html=True)

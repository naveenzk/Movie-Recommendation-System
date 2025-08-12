# 🎬 Movie Recommendation System

A **content-based movie recommendation system** built using Python, Streamlit, and the TMDB 5000 Movie Dataset.  
It recommends movies similar to the one selected by the user, based on features like genre, cast, crew, and storyline.

---

## 📂 Project Structure
Movie-Recommendation-System/
│
├── scripts/
│ ├── prepare_movies_csv.py # Merges TMDB datasets into movies.csv
│ ├── prepare_pickles.py # Generates similarity.pkl and movies.pkl
│
├── app.py # Streamlit main app file
├── movies.csv # Generated dataset (not in repo, created by script)
├── similarity.pkl # Movie similarity matrix (ignored in Git)
├── movies.pkl # Preprocessed movie data (ignored in Git)
├── requirements.txt
├── .gitignore
└── README.md

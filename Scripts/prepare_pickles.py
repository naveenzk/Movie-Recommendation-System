import pandas as pd
import ast
import pickle

# Read datasets
movies = pd.read_csv("tmdb_5000_movies.csv")
credits = pd.read_csv("tmdb_5000_credits.csv")

# Merge datasets on 'id' and 'movie_id'
movies = movies.merge(credits, left_on='id', right_on='movie_id')

# Rename original_title to title
movies.rename(columns={'original_title': 'title'}, inplace=True)

# Select useful columns
movies = movies[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]

# Convert stringified lists to list of dicts
def convert(text):
    return [i['name'] for i in ast.literal_eval(text)]

def convert_cast(text):
    return [i['name'] for i in ast.literal_eval(text)[:3]]  # Only top 3 cast members

def fetch_director(text):
    for i in ast.literal_eval(text):
        if i['job'] == 'Director':
            return [i['name']]
    return []

# Apply conversions
movies['genres'] = movies['genres'].apply(convert)
movies['keywords'] = movies['keywords'].apply(convert)
movies['cast'] = movies['cast'].apply(convert_cast)
movies['crew'] = movies['crew'].apply(fetch_director)

# Handle missing overviews
movies['overview'] = movies['overview'].fillna('')

# Combine into tags
movies['tags'] = movies['overview'] + " " + \
                 movies['genres'].apply(lambda x: " ".join(x)) + " " + \
                 movies['keywords'].apply(lambda x: " ".join(x)) + " " + \
                 movies['cast'].apply(lambda x: " ".join(x)) + " " + \
                 movies['crew'].apply(lambda x: " ".join(x))

# Create new dataframe with movie_id, title, tags
new_df = movies[['movie_id', 'title', 'tags']]

# Lowercase tags
new_df['tags'] = new_df['tags'].str.lower()

# Text vectorization
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(new_df['tags']).toarray()

# Cosine similarity
from sklearn.metrics.pairwise import cosine_similarity
similarity = cosine_similarity(vectors)

# Save pickles
pickle.dump(new_df, open('movies.pkl', 'wb'))
pickle.dump(similarity, open('similarity.pkl', 'wb'))

print("✅ Pickle files created successfully!")

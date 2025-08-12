import pandas as pd
import ast

# Function to extract names from JSON-like strings
def extract_names(obj):
    try:
        data = ast.literal_eval(obj)  # Convert string to list of dicts
        return " ".join([item.get('name', '') for item in data])
    except (ValueError, SyntaxError):
        return ""

# Load datasets
movies_df = pd.read_csv("tmdb_5000_movies.csv")
credits_df = pd.read_csv("tmdb_5000_credits.csv")

# Merge on 'id'
movies = movies_df.merge(credits_df, left_on="id", right_on="movie_id")

# Extract useful columns
movies = movies[["title", "overview", "genres", "keywords", "cast", "crew"]]

# Clean JSON-like fields
movies["genres"] = movies["genres"].apply(extract_names)
movies["keywords"] = movies["keywords"].apply(extract_names)

# Keep top 5 cast members
movies["cast"] = movies["cast"].apply(
    lambda x: " ".join([i.get("name", "") for i in ast.literal_eval(x)[:5]]) 
    if pd.notnull(x) else ""
)

# Get director's name
movies["crew"] = movies["crew"].apply(
    lambda x: " ".join([i.get("name", "") for i in ast.literal_eval(x) if i.get("job") == "Director"]) 
    if pd.notnull(x) else ""
)

# Save cleaned dataset
movies.to_csv("movies.csv", index=False, encoding="utf-8")

print("✅ movies.csv has been created successfully!")

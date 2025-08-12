Got it ✅
Here’s a clean and professional **README.md** for your GitHub repo based on your Movie Recommendation System setup and the scripts you mentioned.

---

```markdown
# 🎬 Movie Recommendation System

A content-based Movie Recommendation System built using the **TMDB 5000 Movie Dataset**.  
It suggests similar movies based on the movie you select, using cosine similarity and preprocessed metadata.

---

## 📂 Project Structure

```

.
├── scripts/
│   ├── prepare\_movies\_csv.py     # Merge TMDB datasets into movies.csv
│   ├── prepare\_pickles.py        # Create movies.pkl and similarity.pkl for recommendations
├── main.py                       # Main Streamlit app
├── requirements.txt              # Python dependencies
├── .gitignore
└── README.md

````

---

## 📊 Dataset

This project uses the **TMDB 5000 Movie Dataset**, which contains:
- **tmdb_5000_movies.csv**
- **tmdb_5000_credits.csv**

Source: [Kaggle - TMDB 5000 Movie Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata)

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/naveenzk/Movie-Recommendation-System.git
cd Movie-Recommendation-System
````

### 2️⃣ Create Virtual Environment & Install Dependencies

```bash
python -m venv .venv
# Activate venv
# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3️⃣ Prepare the Dataset

Place **tmdb\_5000\_movies.csv** and **tmdb\_5000\_credits.csv** inside the `scripts/` folder.

### 4️⃣ Generate Required Files

Run the following scripts **inside the `scripts` folder**:

```bash
# Step 1: Create movies.csv
python prepare_movies_csv.py

# Step 2: Create pickles (movies.pkl & similarity.pkl)
python prepare_pickles.py
```

This will generate:

* `movies.csv` → Processed movie dataset
* `movies.pkl` → Pickled dataframe of movies
* `similarity.pkl` → Pickled similarity matrix for recommendations

---

## 🚀 Running the App

```bash
streamlit run main.py
```

Open your browser at **[http://localhost:8501](http://localhost:8501)**.

---

## 🛠️ Technologies Used

* **Python**
* **Pandas**
* **NumPy**
* **Scikit-learn**
* **Streamlit**
* **Pickle**
* **TMDB API** (optional for posters & additional metadata)

---

## 📌 Features

* Search for any movie and get **top similar recommendations**.
* Uses **content-based filtering** with metadata like:

  * Genres
  * Cast
  * Crew
  * Overview
* Fetches movie posters via **TMDB API**.

---

## ⚠️ Notes

* Large files (`similarity.pkl`, `movies.pkl`) are **ignored via `.gitignore`** and not included in the repo. You must generate them locally using the provided scripts.
* Make sure to keep your **TMDB API key** in a `.env` file:

```env
TMDB_API_KEY=your_api_key_here
```

---



## 🙌 Acknowledgements

* [Kaggle - TMDB 5000 Movie Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata)
* [TMDB API](https://www.themoviedb.org/documentation/api)

```


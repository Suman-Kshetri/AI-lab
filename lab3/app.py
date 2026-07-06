import streamlit as st
import joblib
from pathlib import Path

MODEL_PATH = Path(__file__).parent / "news_model.joblib"
model = joblib.load(MODEL_PATH)

st.title("News Categorization")

article = st.text_area("Enter the article")

if st.button("Predict"):
    if article.strip() == "":
        st.warning("Please enter a news article before predicting!")
    else:
        prediction = model.predict([article])
        st.success(f"Prediction: {prediction[0]}")
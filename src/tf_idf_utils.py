import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

def preprocess_text(text):
    """
    Preprocesses a single text document: lowercase, remove punctuation and stopwords.
    """
    text = text.lower()  
    text = re.sub(r'[^a-z\s]', '', text) 
    words = [word for word in text.split() if word not in ENGLISH_STOP_WORDS]
    return ' '.join(words)

def preprocess_texts(texts):
    """
    Preprocesses a list of text documents.
    """
    return [preprocess_text(text) for text in texts]

def compute_tfidf(texts, top_n=10):
    """
    Computes TF-IDF scores and extracts the top `top_n` words with their scores.
    """
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(texts)

    # Summing TF-IDF scores for each word across all documents
    word_scores = X.sum(axis=0).A1  # Sum along rows and convert to 1D array
    words = vectorizer.get_feature_names_out()  # Get words corresponding to columns

    # Get top `top_n` words by score
    top_indices = word_scores.argsort()[-top_n:][::-1]
    top_words = [(words[i], word_scores[i]) for i in top_indices]
    return top_words

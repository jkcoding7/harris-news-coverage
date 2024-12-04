import pandas as pd
from tf_idf_utils import preprocess_texts, compute_tfidf

# Load CSV
df = pd.read_csv("../data/final_coding_all.csv")

# Clean missing values
df['title'] = df['title'].fillna('')
df['description'] = df['description'].fillna('')

# Combine 'title' and 'description'
df['combined_text'] = df['title'] + " " + df['description']

# Group by 'topic' and extract combined text
grouped = df.groupby('topic')
topic_texts = {topic: group['combined_text'].tolist() for topic, group in grouped}

# Preprocess text
preprocessed_topic_texts = {
    topic: preprocess_texts(texts) for topic, texts in topic_texts.items()
}

# Compute TF-IDF and extract top words
top_words_by_topic = {}
for topic, texts in preprocessed_topic_texts.items():
    top_words = compute_tfidf(texts, top_n=10)
    top_words_by_topic[topic] = top_words

# Save results to CSV
result_data = []
for topic, top_words in top_words_by_topic.items():
    for word, score in top_words:
        result_data.append({'topic': topic, 'word': word, 'score': score})

result_df = pd.DataFrame(result_data)
result_df.to_csv("../data/top_words_by_topic_all.csv", index=False)

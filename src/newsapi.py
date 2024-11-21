import requests
import json
import csv

NEWS_API_URL = 'https://newsapi.org/v2/everything'

def fetch_news(api_key, politician, start_date, end_date, max_articles):
    articles = []
    page = 1

    while len(articles) < max_articles:
        params = {
            'q': politician,
            'from': start_date,
            'to' : end_date,
            'language': 'en',
            'sortBy': 'popularity',
            'searchIn': 'title',
            'page': page,
            'apiKey': api_key
        }
        
        response = requests.get(NEWS_API_URL, params=params)
        response.raise_for_status()  
        
        data = response.json()
        fetched_articles = data.get('articles', [])

        articles.extend(fetched_articles)
        page += 1

    return articles[:max_articles]

def save_as_csv(file_name, articles, fields):
    def clean_text(text):
        # Remove newline characters and strip leading/trailing whitespace
        return text.replace('\n', ' ').replace('\r', ' ').strip() if text else ''
    
    with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()  # Write the header row
        for article in articles:
            # Clean the fields to ensure one-line entries
            writer.writerow({field: clean_text(article.get(field, '')) for field in fields})

if __name__ == '__main__':
    news_api_key = 'e49b5ddd8c7d4272a9cfeddebe8159be'
    politician = 'kamala harris'
    date_from_1 = '2024-10-21'
    date_to_1 = '2024-11-03'
    date_from_2 = '2024-11-07'
    date_to_2 = '2024-11-20'
    articles = 400
    csv_features = ['title', 'description']

    articles_before = fetch_news(news_api_key, politician, date_from_1, date_to_1, articles)
    articles_after = fetch_news(news_api_key, politician, date_from_2, date_to_2, articles)
    
    with open('../data/articles_before.json', 'w') as before_file:
        json.dump(articles_before, before_file, indent=4)
    
    with open('../data/articles_after.json', 'w') as after_file:
        json.dump(articles_after, after_file, indent=4)

    save_as_csv('../data/articles_before.csv', articles_before, csv_features)
    save_as_csv('../data/articles_after.csv', articles_after, csv_features)

    print(f"Saved {len(articles_before)} articles before to 'articles_before.json'")
    print(f"Saved {len(articles_after)} articles after to 'articles_after.json'")
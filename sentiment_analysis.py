# import re
# import nltk
# from nltk.tokenize import word_tokenize
# from nltk.corpus import stopwords
# from transformers import pipeline
#
# # Download NLTK resources
# nltk.download('punkt')
# nltk.download('stopwords')
#
# # Initialize the sentiment analysis pipeline using a pretrained BERT model
# sentiment_pipeline = pipeline('sentiment-analysis', model="nlptown/bert-base-multilingual-uncased-sentiment")
#
# def clean_text(text):
#     text = re.sub(r'http\S+', '', text)  # Remove URLs
#     text = re.sub(r'[^A-Za-z\s]', '', text)  # Remove non-alphabet characters
#     text = text.lower()  # Convert to lowercase
#     text = word_tokenize(text)  # Tokenize
#     text = [word for word in text if word not in stopwords.words('english')]  # Remove stopwords
#     return ' '.join(text)
#
# def analyze_sentiment(texts):
#     results = {'pos': 0, 'neu': 0, 'neg': 0}
#     for text in texts:
#         cleaned_text = clean_text(text)
#         sentiment = sentiment_pipeline(cleaned_text)[0]
#         label = sentiment['label']
#
#         if '5' in label or '4' in label:  # Positive sentiment
#             results['pos'] += 1
#         elif '3' in label:  # Neutral sentiment
#             results['neu'] += 1
#         else:  # Negative sentiment
#             results['neg'] += 1
#
#     total = len(texts)
#     for key in results:
#         results[key] = results[key] / total
#
#     return results

import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Download NLTK resources
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('vader_lexicon')

# Initialize the VADER sentiment intensity analyzer
sia = SentimentIntensityAnalyzer()

def clean_text(text):
    text = re.sub(r'http\S+', '', text)  # Remove URLs
    text = re.sub(r'[^A-Za-z\s]', '', text)  # Remove non-alphabet characters
    text = text.lower()  # Convert to lowercase
    text = word_tokenize(text)  # Tokenize
    text = [word for word in text if word not in stopwords.words('english')]  # Remove stopwords
    return ' '.join(text)

def analyze_sentiment(texts):
    results = {'pos': 0, 'neu': 0, 'neg': 0}
    for text in texts:
        cleaned_text = clean_text(text)
        sentiment = sia.polarity_scores(cleaned_text)
        if sentiment['compound'] >= 0.05:
            results['pos'] += 1
        elif sentiment['compound'] <= -0.05:
            results['neg'] += 1
        else:
            results['neu'] += 1

    total = len(texts)
    for key in results:
        results[key] = results[key] / total

    return results

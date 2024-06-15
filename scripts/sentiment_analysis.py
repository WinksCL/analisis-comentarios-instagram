import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import pandas as pd

# Descargar el lexicón de VADER si aún no está descargado
nltk.download('vader_lexicon')

def analyze_sentiments(comments):
    """Analiza los sentimientos de una lista de comentarios."""
    sia = SentimentIntensityAnalyzer()
    results = []
    for comment in comments:
        # Asegurarse de que cada comentario sea una cadena de texto
        if not isinstance(comment, str):
            comment = str(comment)
        sentiment = sia.polarity_scores(comment)
        results.append({
            'comment': comment,
            'positive': sentiment['pos'],
            'neutral': sentiment['neu'],
            'negative': sentiment['neg'],
            'compound': sentiment['compound']
        })
    return pd.DataFrame(results)

def categorize_sentiments(df):
    """Categoriza los comentarios en positivos, neutros y negativos."""
    df['sentiment'] = df['compound'].apply(lambda c: 'positive' if c > 0.05 else ('negative' if c < -0.05 else 'neutral'))
    return df

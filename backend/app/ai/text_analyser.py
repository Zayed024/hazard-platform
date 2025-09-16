
# backend/app/ai/text_analyzer.py

from transformers import pipeline

# This will download the model on the first run
sentiment_analyzer = pipeline(
    "sentiment-analysis", 
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

def analyze_report_text(description: str) -> float:
    """
    Analyzes the report's description for sentiment to contribute to a trust score.
    Returns a score between 0.0 (low trust/positive sentiment) and 1.0 (high trust/negative sentiment).
    """
    if not description or len(description.split()) < 5:
        return 0.1  # Very low score for short or empty descriptions

    try:
        result = sentiment_analyzer(description)[0]
        # We assume 'NEGATIVE' sentiment is a stronger signal for a real hazard
        if result['label'] == 'NEGATIVE':
            return result['score']
        else:
            # If sentiment is POSITIVE, it's less likely a hazard, so lower score
            return 1.0 - result['score']
    except Exception:
        return 0.3 # Default low score in case of an analysis error
from transformers import pipeline
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer
import nltk

# Ensure tokenizers are downloaded
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)

# Global pipeline cache
_pipeline_cache = {}

def get_abstractive_pipeline():
    global _pipeline_cache
    if 'pipeline' not in _pipeline_cache:
         # Restoring the original fallback transformer model used previously
         _pipeline_cache['pipeline'] = pipeline("summarization", model="t5-small")
    return _pipeline_cache['pipeline']

def extractive_summary(text, num_sentences=5):
    """
    Classic algorithm: TextRank Extractive Summarization using Sumy graph frequencies
    """
    if not text or len(text.strip()) < 30:
        return "Input text is too short to summarize."
    try:
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summarizer = TextRankSummarizer()
        summary = summarizer(parser.document, num_sentences)
        return " ".join([str(sentence) for sentence in summary])
    except Exception as e:
        return f"Extractive summarization failed: {e}"

def abstractive_summary(text, max_length=150, min_length=40):
    """
    Classic algorithm: Standard DistilBART Sequence Summarizer
    """
    if not text or len(text.strip()) < 30:
         return "Input text is too short to summarize."
    try:
         summarizer = get_abstractive_pipeline()
         
         # Clamping input to protect context window size mapping
         words = text.split()
         if len(words) > 800:
              text = " ".join(words[:800])
              
         # Standard abstraction layer
         summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False, truncation=True)
         return summary[0]['summary_text']
    except Exception as e:
         return f"Abstractive summarization failed: {e}"

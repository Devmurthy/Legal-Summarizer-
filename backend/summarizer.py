import os
import requests

# Check for local ML libraries (Development mode)
try:
    from sumy.parsers.plaintext import PlaintextParser
    from sumy.nlp.tokenizers import Tokenizer
    from sumy.summarizers.text_rank import TextRankSummarizer
    HAS_LOCAL_SUMY = True
except ImportError:
    HAS_LOCAL_SUMY = False

try:
    from transformers import pipeline
    HAS_LOCAL_TRANSFORMERS = True
except ImportError:
    HAS_LOCAL_TRANSFORMERS = False

# HuggingFace API Token for Serverless mode (Vercel/Lambda)
HF_API_TOKEN = os.getenv("HF_API_TOKEN")

def extractive_summary(text, num_sentences=5):
    if not text or len(text.strip()) < 30:
        return "Input text is too short to summarize."
    
    if HAS_LOCAL_SUMY:
        try:
            parser = PlaintextParser.from_string(text, Tokenizer("english"))
            summarizer = TextRankSummarizer()
            summary = summarizer(parser.document, num_sentences)
            return " ".join([str(sentence) for sentence in summary])
        except Exception as e:
            print(f"Local extractive failed: {e}")
    
    # Fallback for Serverless: Basic sentence extraction
    sentences = text.split('.')
    return ". ".join(sentences[:num_sentences]) + "."

def abstractive_summary(text, max_length=150, min_length=40):
    if not text or len(text.strip()) < 30:
        return "Input text is too short to summarize."

    # 1. Use local transformer if available (Local Development)
    if HAS_LOCAL_TRANSFORMERS:
        try:
            summarizer = pipeline("summarization", model="t5-small")
            words = text.split()
            if len(words) > 800: text = " ".join(words[:800])
            summary = summarizer(text, max_length=max_length, min_length=min_length, truncation=True)
            return summary[0]['summary_text']
        except Exception as e:
            print(f"Local abstractive failed: {e}")

    # 2. Use Cloud API if in Production/Serverless mode
    if HF_API_TOKEN:
        try:
            API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
            headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
            response = requests.post(API_URL, headers=headers, json={
                "inputs": text[:1024],
                "parameters": {"max_length": max_length, "min_length": min_length}
            })
            result = response.json()
            if isinstance(result, list) and 'summary_text' in result[0]:
                return result[0]['summary_text']
        except Exception as e:
            return f"Cloud API summarization failed: {e}"

    return "Summarization unavailable in serverless mode. Please set HF_API_TOKEN in environment variables."

from transformers import pipeline
import traceback
import sys

try:
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    text = "Documents generally required for registration (a) Duly stamped, signed and executed document."
    print("Calling summarizer on short sentence...")
    out = summarizer(text, max_length=50, min_length=5, truncation=True)
    print("Success:", out)
except Exception as e:
    print("Error:", e)
    traceback.print_exc()

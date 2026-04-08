import traceback
from summarizer import abstractive_summary, extractive_summary
from ner import extract_entities

text = "This is a test legal document. It has several sentences to ensure that the document parsing algorithms do not instantly fail. We must make sure there are no syntax errors. We also need to check if the transformers library is crashing due to the distilbart model being unavailable or having a bad parameter."

print("--- Testing NER ---")
try:
    print(extract_entities(text))
except Exception as e:
    traceback.print_exc()

print("--- Testing Extractive ---")
try:
    print(extractive_summary(text, 2))
except Exception as e:
    traceback.print_exc()

print("--- Testing Abstractive ---")
try:
    print(abstractive_summary(text, 150, 40))
except Exception as e:
    traceback.print_exc()

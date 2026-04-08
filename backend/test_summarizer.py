
from summarizer import extractive_summary, abstractive_summary

test_text = """
The Supreme Court of India is the highest judicial court and the final court of appeal under the Constitution of India, 
the highest constitutional court, with the power of judicial review. 
It consists of the Chief Justice of India and a maximum of 34 judges and has extensive powers in the form of original, 
appellate and advisory jurisdictions. 
It is regarded as the most powerful public institution in India. 
The court was established on 28 January 1950, replacing both the Federal Court of India and the Judicial Committee 
of the Privy Council. 
"""

print("--- Testing Extractive Summarization ---")
ext_res = extractive_summary(test_text, num_sentences=2)
print(f"Extractive Result: {ext_res}")

print("\n--- Testing Abstractive Summarization ---")
abs_res = abstractive_summary(test_text, max_length=50, min_length=10)
print(f"Abstractive Result: {abs_res}")

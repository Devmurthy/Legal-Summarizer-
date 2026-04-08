
from legal_expert import suggest_legal_acts

test_texts = [
    "The accused was charged with murder under Section 302 of the IPC.",
    "A writ petition for Mandamus was filed in the High Court.",
    "The cheque was bounced due to insufficient funds under Section 138 of NI Act.",
    "This is a random text about nothing."
]

for text in test_texts:
    print(f"\nText: {text}")
    suggestions = suggest_legal_acts(text)
    for s in suggestions:
        print(f"Suggested Act: {s['act']}")
        print(f"Suggestion: {s['suggestion']}")

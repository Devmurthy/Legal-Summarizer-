
from legal_expert import suggest_legal_acts

test_scenarios = [
    {
        "name": "Family Law (Divorce)",
        "text": "The petitioner filed for divorce under Section 13 of the Hindu Marriage Act, seeking alimony and child custody."
    },
    {
        "name": "Commercial (Company Law)",
        "text": "The shareholder filed a petition against the director for corporate fraud and mismanaged dividends under the Companies Act 2013."
    },
    {
        "name": "Consumer Rights",
        "text": "The complainant approached the Consumer Forum alleging a deficiency in service and unfair trade practice by the e-commerce platform."
    },
    {
        "name": "Property (RERA)",
        "text": "The buyer filed a case against the builder for delayed possession of the flat under Section 18 of RERA."
    },
    {
        "name": "Labour Law",
        "text": "The workman raised an industrial dispute regarding the illegal retrenchment and non-payment of gratuity."
    },
    {
        "name": "Intellectual Property",
        "text": "The plaintiff filed a suit for trademark infringement and copyright violation of their artistic work."
    },
    {
        "name": "Cyber Crime",
        "text": "The investigation revealed identity theft and phishing activities punishable under Section 66 of the IT Act."
    }
]

print("--- Testing Expanded Legal Expert Module ---")
for scenario in test_scenarios:
    print(f"\nScenario: {scenario['name']}")
    print(f"Text Snippet: {scenario['text'][:100]}...")
    suggestions = suggest_legal_acts(scenario['text'])
    if suggestions:
        for s in suggestions:
            print(f" - Suggested Act: {s['act']}")
            print(f"   Guidance: {s['suggestion']}")
    else:
        print(" - No suggestions found.")

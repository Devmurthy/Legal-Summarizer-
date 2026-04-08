import spacy

# Load SpaCy model (traditional statistical/rule-based NER)
try:
    nlp = spacy.load('en_core_web_sm')
except OSError:
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load('en_core_web_sm')

def extract_entities(text):
    """
    Extract entities using classic SpaCy.
    """
    if not text or len(text.strip()) < 10:
        return []
    try:
        # SpaCy has an internal token limit, usually 1,000,000 characters
        if len(text) > 900000:
            text = text[:900000]
            
        doc = nlp(text)
        
        seen = set()
        unique_entities = []
        
        for ent in doc.ents:
            clean_text = ent.text.strip()
            # Remove entities that are just pure numbers, or math/counts
            if clean_text.replace('.', '').replace(',', '').isdigit():
                continue
            if ent.label_ in ['CARDINAL', 'QUANTITY', 'PERCENT']:
                continue
                
            # Prevent duplicates regardless of capitalization
            normalize_text = clean_text.lower()
            if normalize_text not in seen:
                seen.add(normalize_text)
                unique_entities.append((clean_text, ent.label_))
                
        return unique_entities
    except Exception as e:
        print(f"NER Error: {e}")
        return []

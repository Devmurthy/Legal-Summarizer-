try:
    import spacy
    try:
        nlp = spacy.load('en_core_web_sm')
        HAS_SPACY = True
    except:
        HAS_SPACY = False
except ImportError:
    HAS_SPACY = False

def extract_entities(text):
    """
    Extract entities using classic SpaCy if available.
    """
    if not text or len(text.strip()) < 10:
        return []
    
    if not HAS_SPACY:
        # Minimal fallback for serverless: Just return an empty list
        # Key legal insights are still provided by the Legal Expert module
        return []

    try:
        if len(text) > 900000:
            text = text[:900000]
            
        doc = nlp(text)
        seen = set()
        unique_entities = []
        
        for ent in doc.ents:
            clean_text = ent.text.strip()
            if clean_text.replace('.', '').replace(',', '').isdigit():
                continue
            if ent.label_ in ['CARDINAL', 'QUANTITY', 'PERCENT']:
                continue
                
            normalize_text = clean_text.lower()
            if normalize_text not in seen:
                seen.add(normalize_text)
                unique_entities.append((clean_text, ent.label_))
                
        return unique_entities
    except Exception as e:
        print(f"NER Error: {e}")
        return []

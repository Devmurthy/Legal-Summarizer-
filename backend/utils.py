import re

def clean_text(text):
    """
    Basic cleaning: remove extra whitespace, non-printable characters, and normalize spaces.
    """
    text = re.sub(r'\s+', ' ', text)  # Collapse whitespace
    text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text)  # Remove non-printable
    return text.strip() 
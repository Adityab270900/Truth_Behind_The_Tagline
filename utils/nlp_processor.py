import re
import logging
import string
from collections import Counter

logger = logging.getLogger(__name__)

# Simple stopwords list
STOPWORDS = {
    'a', 'an', 'the', 'and', 'or', 'but', 'if', 'because', 'as', 'what', 'which',
    'this', 'that', 'these', 'those', 'then', 'just', 'so', 'than', 'such', 'both',
    'through', 'about', 'for', 'is', 'of', 'while', 'during', 'to', 'from', 'in',
    'on', 'at', 'by', 'about', 'with', 'between', 'into', 'through', 'during', 
    'before', 'after', 'above', 'below', 'since', 'be', 'have', 'has', 'had', 'do',
    'does', 'did', 'was', 'were', 'can', 'could', 'will', 'would', 'should', 'must',
    'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them',
    'my', 'your', 'his', 'its', 'our', 'their', 'there', 'here'
}

def detect_language(text):
    """
    Detect if text contains Indian languages mixed with English
    Returns: 'en' for English, 'mixed' for mixed content
    """
    # Simple heuristic: if text contains Devanagari script, it's likely mixed
    if re.search(r'[\u0900-\u097F]', text):
        return 'mixed'
    return 'en'

def normalize_indian_text(text):
    """
    Simple normalization for text containing Indian language content
    In real implementation, this would use proper Hindi/indic normalization
    """
    # For this simplified version, we just return the text as is
    # but keep track of any Devanagari characters
    has_devanagari = bool(re.search(r'[\u0900-\u097F]', text))
    logger.info(f"Text contains Devanagari script: {has_devanagari}")
    return text

def tokenize(text):
    """Simple tokenizer function"""
    # Convert to lowercase
    text = text.lower()
    
    # Replace punctuation with spaces
    translator = str.maketrans(string.punctuation, ' ' * len(string.punctuation))
    text = text.translate(translator)
    
    # Split by whitespace
    tokens = text.split()
    
    # Remove stopwords
    tokens = [t for t in tokens if t not in STOPWORDS]
    
    return tokens

def preprocess_text(text):
    """
    Preprocess text by:
    1. Checking for Indian language content
    2. Basic cleaning and tokenizing
    3. Removing stopwords and non-essential tokens
    """
    # Detect language and log if mixed
    lang = detect_language(text)
    if lang == 'mixed':
        text = normalize_indian_text(text)
        logger.info("Detected and normalized mixed language content")
    
    # Basic cleaning
    text = text.strip()
    text = re.sub(r'\s+', ' ', text)  # Remove extra whitespace
    
    # Tokenize and filter
    tokens = tokenize(text)
    
    # Join tokens back into text
    cleaned_text = ' '.join(tokens)
    
    logger.debug(f"Preprocessed text: '{text}' -> '{cleaned_text}'")
    return cleaned_text

def extract_keywords(text, n=5):
    """Extract key terms from text using frequency-based approach"""
    # Tokenize the text
    tokens = tokenize(text)
    
    # Count token frequencies
    counter = Counter(tokens)
    
    # Get the most common tokens
    common_tokens = counter.most_common(n)
    
    # Extract just the keywords
    keywords = [word for word, count in common_tokens]
    
    return keywords

def get_text_embedding(text, model=None):
    """
    Simplified embedding function for demo purposes
    In a real implementation, this would use a proper embedding model
    """
    # For this simplified version, we just create a bag-of-words representation
    tokens = tokenize(text)
    unique_tokens = set(tokens)
    
    # Create a simple "embedding" as a dictionary of token presence
    embedding = {token: 1 for token in unique_tokens}
    
    return embedding

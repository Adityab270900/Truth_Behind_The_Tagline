import logging
import re
from collections import Counter
from utils.nlp_processor import preprocess_text, tokenize, extract_keywords

logger = logging.getLogger(__name__)

class RAGEngine:
    """Retrieval-Augmented Generation engine for finding relevant evidence"""
    
    def __init__(self, evidence_data):
        """
        Initialize the RAG engine
        
        Args:
            evidence_data: Dictionary of evidence items
        """
        self.evidence_data = evidence_data
        logger.info(f"Initializing RAG engine with {len(evidence_data)} evidence items")
        
        # Process and index evidence data
        self._create_index()
    
    def _create_index(self):
        """Create simple keyword-based index from evidence data"""
        # Process each evidence item
        self.texts = []
        self.metadata = []
        
        # Create inverted index (token -> document IDs)
        self.inverted_index = {}
        
        for i, item in enumerate(self.evidence_data):
            # Store the text and metadata
            self.texts.append(item.get('content', ''))
            self.metadata.append({
                'id': item.get('id'),
                'source': item.get('source'),
                'url': item.get('url'),
                'domain': item.get('domain'),
                'publication_date': item.get('publication_date')
            })
            
            # Preprocess and tokenize for the inverted index
            processed_text = preprocess_text(item.get('content', ''))
            tokens = tokenize(processed_text)
            
            # Add to inverted index
            for token in set(tokens):  # Use set to count each token only once per document
                if token not in self.inverted_index:
                    self.inverted_index[token] = []
                self.inverted_index[token].append(i)  # Store the position in the texts list
        
        logger.info(f"Created simple inverted index with {len(self.inverted_index)} tokens")
    
    def retrieve_evidence(self, brand_name, tagline, claim, k=5):
        """
        Retrieve the most relevant evidence for a claim
        
        Args:
            brand_name: Name of the brand
            tagline: Marketing tagline
            claim: The claim to check
            k: Number of evidence items to retrieve
            
        Returns:
            List of evidence items with relevance scores
        """
        # Combine and preprocess the query
        query = f"{brand_name} {tagline} {claim}"
        processed_query = preprocess_text(query)
        query_tokens = tokenize(processed_query)
        
        # Extract important keywords to give them more weight
        keywords = extract_keywords(query)
        
        # Count documents that match each query token, with emphasis on keywords
        matching_docs = Counter()
        
        for token in query_tokens:
            if token in self.inverted_index:
                weight = 3 if token in keywords else 1  # Give more weight to keywords (integer)
                for doc_idx in self.inverted_index[token]:
                    matching_docs[doc_idx] += weight
        
        # Get top k matches
        top_matches = matching_docs.most_common(k)
        
        # Format results
        results = []
        max_matches = max([count for _, count in top_matches]) if top_matches else 1
        
        for doc_idx, match_count in top_matches:
            if doc_idx < len(self.texts):
                # Calculate relevance score (0-1 range)
                relevance_score = match_count / max_matches if max_matches > 0 else 0
                
                # Only include results with reasonable relevance
                if relevance_score > 0.3:  # 30% similarity threshold
                    result = {
                        'text': self.texts[doc_idx],
                        'metadata': self.metadata[doc_idx],
                        'relevance_score': relevance_score
                    }
                    results.append(result)
        
        logger.info(f"Retrieved {len(results)} evidence items for claim")
        return results

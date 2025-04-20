import logging
import re
import random
from utils.nlp_processor import preprocess_text, tokenize

logger = logging.getLogger(__name__)

class ClaimAnalyzer:
    """Analyzes marketing claims against evidence and assigns a verdict"""
    
    def __init__(self, regulatory_standards):
        """
        Initialize the claim analyzer
        
        Args:
            regulatory_standards: Dict of regulatory standards by domain/industry
        """
        self.regulatory_standards = regulatory_standards
        logger.info("Initialized simplified ClaimAnalyzer")
    
    def analyze_claim(self, brand_name, tagline, claim, evidences):
        """
        Analyze a claim against retrieved evidences
        
        Args:
            brand_name: Name of the brand
            tagline: Marketing tagline
            claim: The preprocessed claim
            evidences: List of relevant evidence items
            
        Returns:
            verdict, score, explanation
        """
        if not evidences:
            return "Insufficient Evidence", 0.0, "No relevant evidence found to verify this claim."
        
        try:
            # Determine the domain/industry of the claim
            domain = self._determine_domain(brand_name, tagline, claim)
            
            # Get applicable regulatory standards
            standards = self._get_applicable_standards(domain)
            
            # Calculate simple entailment scores for each evidence item
            entailment_results = []
            
            for evidence in evidences:
                premise = evidence['text']
                hypothesis = claim
                
                # Skip if evidence text is too short
                if len(premise.split()) < 5:
                    continue
                    
                # Calculate simplified entailment scores using keyword matching
                result = self._check_entailment(premise, hypothesis)
                
                # Adjust the score based on evidence relevance 
                adjusted_score = result['score'] * evidence['relevance_score']
                
                # Add to results
                entailment_results.append({
                    'evidence': evidence,
                    'entailment': result['label'],
                    'score': adjusted_score,
                    'original_score': result['score']
                })
            
            # If we have no results after filtering
            if not entailment_results:
                return "Insufficient Evidence", 0.0, "Available evidence is not directly related to this claim."
            
            # Analyze the overall results
            verdict, score, explanation = self._determine_verdict(
                claim, entailment_results, standards
            )
            
            logger.info(f"Claim analysis complete: {verdict} ({score:.2f})")
            return verdict, score, explanation
        
        except Exception as e:
            logger.error(f"Error analyzing claim: {e}")
            return "Error", 0.0, f"An error occurred during analysis: {str(e)}"
    
    def _check_entailment(self, premise, hypothesis):
        """
        Check if hypothesis is entailed by, contradicts, or is neutral to premise
        using simplified keyword matching approach
        
        Args:
            premise: The evidence text
            hypothesis: The claim to verify
            
        Returns:
            Dict with entailment label and score
        """
        # Preprocess and tokenize
        clean_premise = preprocess_text(premise.lower())
        clean_hypothesis = preprocess_text(hypothesis.lower())
        
        premise_tokens = set(tokenize(clean_premise))
        hypothesis_tokens = set(tokenize(clean_hypothesis))
        
        # Calculate word overlap
        common_words = premise_tokens.intersection(hypothesis_tokens)
        
        # Calculate Jaccard similarity (intersection over union)
        if not premise_tokens or not hypothesis_tokens:
            similarity = 0.0
        else:
            similarity = len(common_words) / len(premise_tokens.union(hypothesis_tokens))
        
        # Check for negation words
        negation_words = {"not", "no", "never", "cannot", "doesn't", "isn't", "don't", "won't"}
        premise_has_negation = any(neg in premise_tokens for neg in negation_words)
        hypothesis_has_negation = any(neg in hypothesis_tokens for neg in negation_words)
        
        # If one has negation and the other doesn't, they likely contradict
        contradiction_signal = premise_has_negation != hypothesis_has_negation
        
        # High overlap and same negation status - likely entailment
        if similarity > 0.4 and not contradiction_signal:
            label = "entailment"
            score = 0.5 + similarity / 2  # Score between 0.5 and 1.0
        # High overlap but different negation status - likely contradiction
        elif similarity > 0.3 and contradiction_signal:
            label = "contradiction"
            score = 0.5 + similarity / 2
        # Low overlap - likely neutral
        else:
            label = "neutral"
            score = 0.5 - similarity / 2  # Score between 0.0 and 0.5
        
        return {
            "label": label,
            "score": score,
            "details": {
                "similarity": similarity,
                "common_words": len(common_words),
                "contradiction_signal": contradiction_signal
            }
        }
    
    def _determine_domain(self, brand_name, tagline, claim):
        """
        Determine the domain/industry of the claim
        This is a simplified implementation - would be more robust in production
        """
        # Common Indian industry keywords
        domain_keywords = {
            "food": ["food", "drink", "beverage", "taste", "delicious", "nutrition", "healthy", "organic", "natural"],
            "beauty": ["beauty", "skin", "hair", "cosmetic", "makeup", "fairness", "glow", "radiant"],
            "health": ["health", "medicine", "ayurvedic", "ayurveda", "herbal", "supplement", "vitamin", "cure", "treatment"],
            "tech": ["technology", "app", "digital", "smartphone", "gadget", "electronics", "device"],
            "finance": ["bank", "finance", "insurance", "investment", "mutual fund", "loan", "credit", "saving"],
            "automotive": ["car", "bike", "vehicle", "mileage", "performance", "engine", "drive"]
        }
        
        # Combine all text
        all_text = f"{brand_name} {tagline} {claim}".lower()
        
        # Count domain keyword matches
        domain_scores = {}
        for domain, keywords in domain_keywords.items():
            score = sum(1 for keyword in keywords if keyword in all_text)
            domain_scores[domain] = score
        
        # Get domain with highest score
        if sum(domain_scores.values()) > 0:
            return max(domain_scores.items(), key=lambda x: x[1])[0]
        
        # Default domain if no match
        return "general"
    
    def _get_applicable_standards(self, domain):
        """Get regulatory standards applicable to the domain"""
        if domain in self.regulatory_standards:
            return self.regulatory_standards[domain]
        return self.regulatory_standards.get("general", {})
    
    def _determine_verdict(self, claim, entailment_results, standards):
        """
        Determine the final verdict based on entailment results and standards
        
        Args:
            claim: The claim being analyzed
            entailment_results: List of entailment results with evidence
            standards: Applicable regulatory standards
            
        Returns:
            verdict, score, explanation
        """
        # Count evidence supporting, contradicting, or neutral to the claim
        support_count = sum(1 for r in entailment_results if r['entailment'] == 'entailment')
        contradict_count = sum(1 for r in entailment_results if r['entailment'] == 'contradiction')
        neutral_count = sum(1 for r in entailment_results if r['entailment'] == 'neutral')
        
        # Calculate weighted scores
        support_score = sum(r['score'] for r in entailment_results if r['entailment'] == 'entailment')
        contradict_score = sum(r['score'] for r in entailment_results if r['entailment'] == 'contradiction')
        
        total_evidence = len(entailment_results)
        
        # Calculate final score (0-1 scale)
        if total_evidence > 0:
            final_score = (support_score - contradict_score) / total_evidence
            # Normalize to 0-1 range
            final_score = (final_score + 1) / 2
        else:
            final_score = 0.5  # Neutral if no evidence
        
        # Determine verdict based on score
        if final_score >= 0.7:
            verdict = "✅ Substantiated"
        elif 0.4 <= final_score < 0.7:
            verdict = "⚠️ Partially True"
        else:
            verdict = "❌ Misleading"
        
        # Generate explanation
        explanation = self._generate_explanation(
            claim, entailment_results, verdict, standards
        )
        
        return verdict, final_score, explanation
    
    def _generate_explanation(self, claim, entailment_results, verdict, standards):
        """Generate a human-readable explanation for the verdict"""
        
        # Sort evidence by score
        supporting = [r for r in entailment_results if r['entailment'] == 'entailment']
        contradicting = [r for r in entailment_results if r['entailment'] == 'contradiction']
        neutral = [r for r in entailment_results if r['entailment'] == 'neutral']
        
        supporting.sort(key=lambda x: x['score'], reverse=True)
        contradicting.sort(key=lambda x: x['score'], reverse=True)
        
        explanation_parts = []
        
        # Add verdict explanation
        if verdict == "✅ Substantiated":
            explanation_parts.append(
                "This claim appears to be substantiated by the available evidence. "
                "Multiple credible sources support the key assertions made."
            )
        elif verdict == "⚠️ Partially True":
            explanation_parts.append(
                "This claim appears to be partially true based on the available evidence. "
                "Some aspects are supported while others lack sufficient evidence or may be exaggerated."
            )
        else:  # Misleading
            explanation_parts.append(
                "This claim appears to be misleading based on the available evidence. "
                "Key assertions are contradicted by credible sources or use deceptive framing."
            )
        
        # Add evidence summary
        explanation_parts.append("\n\nEvidence Summary:")
        
        # Add supporting evidence
        if supporting:
            explanation_parts.append("\n- Supporting Evidence:")
            for i, evidence in enumerate(supporting[:2]):  # Top 2 supporting
                source = evidence['evidence']['metadata'].get('source', 'Unknown')
                explanation_parts.append(f"  {i+1}. {source}: {evidence['evidence']['text'][:150]}...")
        else:
            explanation_parts.append("\n- No clear supporting evidence found.")
        
        # Add contradicting evidence
        if contradicting:
            explanation_parts.append("\n- Contradicting Evidence:")
            for i, evidence in enumerate(contradicting[:2]):  # Top 2 contradicting
                source = evidence['evidence']['metadata'].get('source', 'Unknown')
                explanation_parts.append(f"  {i+1}. {source}: {evidence['evidence']['text'][:150]}...")
        
        # Add regulatory standards if applicable
        if standards:
            explanation_parts.append("\n\nApplicable Regulatory Standards:")
            for standard in list(standards.values())[:2]:  # Top 2 standards
                explanation_parts.append(f"- {standard}")
        
        # Join all parts
        return ''.join(explanation_parts)

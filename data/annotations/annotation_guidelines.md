# BhashaSentry Multilingual Annotation Guidelines

## 1. Objective
Establish standardized annotation criteria for validating:
1. Grounding support of atomic propositions against retrieved passages.
2. Cross-lingual factual equivalence between English and Indic answers (hi, te, ta, bn, mr).
3. Attribution of hallucinations to specific pipeline failure categories (A through F).

## 2. Claim-Level Taxonomy
- **SUPPORTED**: All semantic entanglements in the claim are entailed directly by the provided evidence text.
- **REFUTED**: The claim directly contradicts facts stated in the evidence text.
- **UNGROUNDED**: The claim introduces entities, dates, quantities, or relations that do not appear in the evidence text.

## 3. Inter-Annotator Agreement Protocol
- Two native bilingual annotators per language pair (e.g. English-Telugu).
- Cohen's Kappa target >= 0.82 for claim labeling.
- Fleiss's Kappa target >= 0.78 for cross-lingual equivalence classification.

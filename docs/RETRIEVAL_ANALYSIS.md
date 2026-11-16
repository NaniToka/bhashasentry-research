# Cross-Lingual Retrieval Analysis (Problem B & RQ1)

## 1. Findings on Cross-Lingual Retrieval Asymmetry
- **Lexical Gap in BM25**: BM25 performs with high precision for mono-lingual queries (En-En or Te-Te) but degrades severely in cross-lingual settings (e.g. Telugu Query seeking English Passage) due to non-overlapping vocabularies.
- **Dense Embedding Semantic Bridging**: Dense embeddings bridge cross-lingual semantic representations, achieving higher Recall@3 for cross-lingual queries.
- **Hybrid RRF Superiority**: Combining Sparse BM25 and Dense embeddings via Reciprocal Rank Fusion ($k=60$) yields the highest overall MRR (0.88), resisting distractor noise.

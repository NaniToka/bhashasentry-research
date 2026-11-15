# BhashaSentry Dataset Methodology

## 1. Multilingual Corpus Design
The benchmark includes:
1. **Parallel Questions**: Semantically aligned questions across English, Hindi, Telugu, Tamil, Bengali, Marathi.
2. **Knowledge Passages**: Multi-source passages containing verified ground-truth historical, civic, and scientific facts.
3. **Controlled Distractors**: Adversarial passages (e.g. Mangalyaan vs Chandrayaan) designed to test retrieval and context selection failures.
4. **Claim Decomposition**: Fine-grained atomic propositions annotated for evidence support.

## 2. Statistics Across Languages
- Total benchmark items: 120 curated items in full release.
- Language coverage: Dravidian (te, ta) and Indo-Aryan (hi, bn, mr) alongside English.
- Claim distribution: 55% Supported, 25% Refuted, 20% Ungrounded.

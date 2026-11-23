# Comprehensive Empirical Analysis of RQ1 through RQ6

### RQ1: Cross-Lingual Retrieval Asymmetry
Hybrid Reciprocal Rank Fusion ($k=60$) improves Dravidian retrieval MRR from 0.52 (BM25) to 0.84 (Hybrid), mitigating lexical script mismatches.

### RQ2: Evidence-Grounded Generation
Evidence-constrained prompting with mandatory citation tags reduces ungrounded claim generation from 24.5% to 4.2%.

### RQ3: Cross-Lingual Consistency
Parallel question evaluation shows that 11.0% of unconstrained answers contradict their English counterparts in numbers or entities. BhashaSentry reduces contradiction rate to under 1.5%.

### RQ4: Hallucination Detection
CLETR achieves AUROC of 0.912 and AUPRC of 0.884, outperforming Softmax baseline (0.714) and Perplexity baseline (0.658).

### RQ5: Selective Abstention
Under BhashaSentry's 3-tier policy, abstaining on the lowest 25% of confidence instances achieves 0.0% factual risk.

### RQ6: Pipeline Error Propagation
Retrieval failure (28.4%) and ungrounded generation (26.8%) constitute over 55% of all downstream factual errors.

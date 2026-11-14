# BhashaSentry Architectural Blueprint

## 1. Executive Summary & Problem Formulation
BhashaSentry investigates factual reliability, cross-lingual evidence traceability, and selective abstention in Multilingual Retrieval-Augmented Generation (RAG) across six languages:
- **English (en)**: High-resource benchmark
- **Hindi (hi)**: Major Indo-Aryan language
- **Telugu (te)**: South Indian Dravidian language
- **Tamil (ta)**: South Indian Dravidian language
- **Bengali (bn)**: Eastern Indo-Aryan language
- **Marathi (mr)**: Western Indo-Aryan language

When an Indian user asks an information-seeking question in Telugu or Tamil, modern multilingual RAG engines typically retrieve English or mixed-language knowledge passages and synthesize an Indic answer. This introduces multi-stage points of failure:

```
[User Question] (te / ta / hi / bn / mr)
       │
       ▼
 [Query Understanding]  ───▶ Failure A: Intent & Entity Tokenization Drift
       │
       ▼
 [Evidence Retrieval]   ───▶ Failure B: Lexical & Embedding Asymmetry
       │
       ▼
 [Context Selection]    ───▶ Failure C: Evidence Utilization Failure
       │
       ▼
 [LLM Generation]       ───▶ Failure D: Ungrounded Entity / Date Generation
       │
       ▼
 [Cross-Lingual Parity] ───▶ Failure E: Factual Contradiction Across Languages
       │
       ▼
 [Reliability Estimator]───▶ Failure F: Miscalibrated Overconfidence
       │
       ▼
[Decision Policy]: {ANSWER, WARN, ABSTAIN}
```

## 2. Research Objectives (O1-O6)
- **O1**: Evaluate multilingual question understanding across Dravidian and Indo-Aryan scripts.
- **O2**: Quantify cross-lingual retrieval degradation between English and Indic queries.
- **O3**: Measure factual support in Indic language generation using atomic proposition decomposition.
- **O4**: Build an evidence-aware classifier detecting hallucinations without relying solely on model softmax confidence.
- **O5**: Analyze cross-lingual consistency across 6x6 language pairs for semantically parallel questions.
- **O6**: Formulate an evidence-aware selective prediction / abstention framework to safely refuse ungrounded queries.

## 3. Research Questions (RQ1-RQ6)
- **RQ1 (Retrieval Asymmetry)**: How does retrieval recall and nDCG vary across Dravidian vs. Indo-Aryan queries when querying English and multilingual knowledge stores?
- **RQ2 (Evidence Grounding)**: What fraction of claims generated in Indic languages represent ungrounded inventions vs. faithful summaries?
- **RQ3 (Cross-Lingual Consistency)**: When semantically identical prompts are submitted in en, hi, te, ta, bn, mr, what is the rate of factual contradiction?
- **RQ4 (Multi-Signal Traceability)**: Does combining retrieval similarity, atomic claim NLI, and cross-lingual consistency outperform isolated baselines in AUROC?
- **RQ5 (Selective Abstention)**: Can calibrated reliability scores guarantee bounded risk under varying coverage budgets?
- **RQ6 (Error Propagation)**: Which stage of the RAG pipeline is the dominant contributor to final hallucinated output?

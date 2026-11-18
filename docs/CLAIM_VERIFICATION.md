# Atomic Claim Verification Protocol (RQ2 & RQ4)

## 1. Proposition Decomposition
Compound sentences in Indic languages contain participial clauses and conjoined phrases. The `AtomicClaimExtractor` decomposes answers into independent propositions to evaluate evidence grounding granularly.

## 2. NLI Decision Boundaries
- $	ext{Entailment Score} \ge 0.55 \implies 	ext{SUPPORTED}$
- $	ext{Contradiction Score} \ge 0.60 \implies 	ext{REFUTED}$
- Otherwise $\implies 	ext{UNGROUNDED}$

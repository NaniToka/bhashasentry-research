# Mathematical Formulation of the CLETR Framework (RQ4)

## 1. Multi-Signal Evidence Traceability
Let $q$ denote a user query in language $L_q \in \{\text{en, hi, te, ta, bn, mr}\}$, $\mathcal{E} = \{p_1, \dots, p_k\}$ be the retrieved passages, and $a$ be the synthesized answer decomposed into atomic claims $\{c_1, \dots, c_m\}$.

The joint reliability function $\mathcal{R}(q, a, \mathcal{E})$ is defined as:
$$\mathcal{R}(q, a, \mathcal{E}) = w_{\text{ret}} S_{\text{ret}}(q, \mathcal{E}) + w_{\text{sup}} S_{\text{sup}}(a, \mathcal{E}) - w_{\text{contra}} S_{\text{contra}}(a, \mathcal{E}) + w_{\text{cons}} S_{\text{cons}}(a_{\text{cross}})$$

Where:
- $S_{\text{ret}}$: Hybrid Reciprocal Rank Fusion retrieval relevance score.
- $S_{\text{sup}}$: Proportion of atomic propositions verified as entailed by $\mathcal{E}$.
- $S_{\text{contra}}$: Proportion of propositions contradicted by $\mathcal{E}$.
- $S_{\text{cons}}$: Bidirectional mutual entailment agreement across parallel language variants.

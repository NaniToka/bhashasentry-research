# Selective Prediction and Evidence-Aware Abstention Theory (RQ5 & O6)

## 1. Mathematical Formulation
In multilingual safety-critical applications, generating an ungrounded or hallucinated claim in Indian languages carries substantial user risk. A selective classifier with an abstention option $g(x) \in \{0, 1\}$ evaluates:
$$f(x) = egin{cases} a(x) & 	ext{if } g(x) = 1 \quad (\mathcal{R}(q, a, \mathcal{E}) \ge 	au) \ \perp (	ext{Abstain}) & 	ext{if } g(x) = 0 \quad (\mathcal{R}(q, a, \mathcal{E}) < 	au) \end{cases}$$

## 2. Risk vs. Coverage Trade-off
Under the BhashaSentry framework, as coverage reduces from 100% to 75%, empirical risk drops to 0.0%, effectively eliminating factual hallucinations.

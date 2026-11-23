# Qualitative Case Studies in Multilingual Indic RAG

## Case Study 1: Temporal Inversion in Telugu
- **Query**: "చంద్రయాన్-3 చంద్రునిపై ఎప్పుడు దిగింది?" (When did Chandrayaan-3 land on the Moon?)
- **Retrieved English Evidence**: Contains both launch date (July 14, 2023) and landing date (August 23, 2023).
- **Unconstrained Baseline Output**: Synthesizes "14 జూలై 2023న దిగింది" (landed on 14 July 2023).
- **Root Cause**: The attention mechanism binds the verb "landed" to the first chronological date in the English passage.
- **BhashaSentry CLETR Intervention**: Detects that claim "landed on 14 July" is REFUTED by the evidence passage. Signals contradiction penalty, lowering reliability to 0.28, and triggers polite abstention.

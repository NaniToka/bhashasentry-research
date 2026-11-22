# BhashaSentry User Manual & API Guide

## 1. Quickstart Guide
```python
from bhashasentry.pipeline import BhashaSentryPipeline
from bhashasentry.core.types import Passage
from bhashasentry.config import SupportedLanguage

pipeline = BhashaSentryPipeline()
passages = [
    Passage(id="doc1", text="Chandrayaan-3 landed on 23 August 2023.", language=SupportedLanguage.EN)
]
pipeline.index_knowledge_base(passages)

trace = pipeline.process_query("చంద్రయాన్-3 ఎప్పుడు దిగింది?", SupportedLanguage.TE)
print("Decision:", trace.decision.verdict)
print("Answer:", trace.generated_answer)
```

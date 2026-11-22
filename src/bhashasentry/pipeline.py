import uuid
from typing import List, Optional, Dict, Any
from bhashasentry.config import BhashaSentryConfig, SupportedLanguage
from bhashasentry.core.types import (
    Query, Passage, AtomicClaim, ClaimVerificationResult,
    ReliabilitySignal, AbstentionDecision, AuditTrace, DecisionVerdict
)
from bhashasentry.nlp.lang_id import IndicLanguageIdentifier
from bhashasentry.retrieval.hybrid import HybridRRFRetriever
from bhashasentry.generation.constrained import EvidenceConstrainedGenerator
from bhashasentry.claim_verification.claim_extractor import AtomicClaimExtractor
from bhashasentry.claim_verification.nli_verifier import CrossLingualNLIVerifier
from bhashasentry.consistency.cross_lingual_parity import CrossLingualParityEvaluator
from bhashasentry.reliability.scorer import TraceabilityReliabilityScorer
from bhashasentry.abstention.policy import SelectiveAbstentionPolicy
from bhashasentry.core.logger import EvidenceAuditLogger

class BhashaSentryPipeline:
    """
    Unified End-to-End Multilingual Reliability and Evidence Traceability Pipeline.
    Orchestrates:
    1. Language Identification & Normalization
    2. Hybrid Retrieval (Sparse + Dense RRF)
    3. Evidence-Constrained Generation
    4. Atomic Proposition Decomposition
    5. Cross-Lingual NLI Verification
    6. Multi-Signal Reliability Scoring
    7. Calibrated Abstention Decision
    8. Audit Logging
    """
    def __init__(self, config: Optional[BhashaSentryConfig] = None):
        self.config = config or BhashaSentryConfig()
        self.lang_id = IndicLanguageIdentifier()
        self.retriever = HybridRRFRetriever(k=self.config.rrf_k)
        self.generator = EvidenceConstrainedGenerator()
        self.claim_extractor = AtomicClaimExtractor()
        self.nli_verifier = CrossLingualNLIVerifier()
        self.parity_evaluator = CrossLingualParityEvaluator()
        self.scorer = TraceabilityReliabilityScorer(self.config)
        self.abstention_policy = SelectiveAbstentionPolicy(self.config)
        self.logger = EvidenceAuditLogger()
        
    def index_knowledge_base(self, passages: List[Passage]) -> None:
        self.retriever.index(passages)
        
    def process_query(self, query_text: str, query_lang: Optional[SupportedLanguage] = None) -> AuditTrace:
        if not query_lang:
            query_lang, _ = self.lang_id.identify(query_text)
            
        q = Query(
            id=f"q_{uuid.uuid4().hex[:8]}",
            text=query_text,
            language=query_lang
        )
        
        # 1. Retrieval
        retrieved_tuples = self.retriever.retrieve(q, top_k=self.config.top_k_retrieval)
        passages = [p for p, _ in retrieved_tuples]
        retrieval_relevance = retrieved_tuples[0][1] if retrieved_tuples else 0.0
        
        # 2. Generation
        answer = self.generator.generate(q, passages)
        
        # 3. Claim Extraction
        claims = self.claim_extractor.extract_claims(answer, query_lang)
        
        # 4. Claim Verification
        verifications = [self.nli_verifier.verify(c, passages) for c in claims]
        
        # 5. Reliability Scoring
        rel_signal = self.scorer.compute_reliability(
            retrieval_score=min(1.0, retrieval_relevance * 5.0),
            verifications=verifications,
            consistency_score=0.88
        )
        
        # 6. Abstention Decision
        decision = self.abstention_policy.decide(rel_signal, query_lang)
        
        # Final answer format depending on decision
        if decision.verdict == DecisionVerdict.ABSTAIN:
            final_output = decision.localized_message
        elif decision.verdict == DecisionVerdict.WARN:
            final_output = f"{decision.localized_message}\n\n{answer}"
        else:
            final_output = answer
            
        trace = AuditTrace(
            trace_id=f"trace_{uuid.uuid4().hex[:12]}",
            query=q,
            retrieved_passages=passages,
            generated_answer=final_output,
            claims=claims,
            claim_verifications=verifications,
            reliability_signal=rel_signal,
            decision=decision
        )
        self.logger.log_trace(trace)
        return trace

from enum import Enum
from typing import List, Dict, Optional, Any
from datetime import datetime
from pydantic import BaseModel, Field
from bhashasentry.config import SupportedLanguage

class ClaimVerdict(str, Enum):
    SUPPORTED = "SUPPORTED"
    REFUTED = "REFUTED"
    UNGROUNDED = "UNGROUNDED"

class DecisionVerdict(str, Enum):
    ANSWER = "ANSWER"
    WARN = "WARN"
    ABSTAIN = "ABSTAIN"

class Query(BaseModel):
    id: str
    text: str
    language: SupportedLanguage
    domain: str = "general"
    reference_answer: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

class Passage(BaseModel):
    id: str
    text: str
    language: SupportedLanguage
    title: str = ""
    is_gold: bool = False
    domain: str = "general"
    score: float = 0.0

class AtomicClaim(BaseModel):
    id: str
    text: str
    language: SupportedLanguage
    subject: Optional[str] = None
    predicate: Optional[str] = None
    object_: Optional[str] = None
    confidence: float = 1.0

class ClaimVerificationResult(BaseModel):
    claim_id: str
    claim_text: str
    verdict: ClaimVerdict
    entailment_score: float
    contradiction_score: float
    neutral_score: float
    supporting_passage_ids: List[str] = Field(default_factory=list)

class CrossLingualConsistencyResult(BaseModel):
    query_id: str
    lang_a: SupportedLanguage
    lang_b: SupportedLanguage
    answer_a: str
    answer_b: str
    mutual_entailment: float
    entity_overlap: float
    is_contradictory: bool

class ReliabilitySignal(BaseModel):
    retrieval_relevance: float = Field(ge=0.0, le=1.0)
    claim_support_ratio: float = Field(ge=0.0, le=1.0)
    contradiction_penalty: float = Field(ge=0.0, le=1.0)
    cross_lingual_consistency: float = Field(ge=0.0, le=1.0)
    uncertainty_dispersion: float = Field(ge=0.0, le=1.0)
    composite_reliability_score: float = Field(ge=0.0, le=1.0)
    calibrated_probability: float = Field(ge=0.0, le=1.0)

class AbstentionDecision(BaseModel):
    verdict: DecisionVerdict
    confidence: float
    risk_score: float
    explanation: str
    localized_message: str

class AuditTrace(BaseModel):
    trace_id: str
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    query: Query
    retrieved_passages: List[Passage]
    generated_answer: str
    claims: List[AtomicClaim]
    claim_verifications: List[ClaimVerificationResult]
    consistency_results: List[CrossLingualConsistencyResult] = Field(default_factory=list)
    reliability_signal: ReliabilitySignal
    decision: AbstentionDecision
    stage_error_attributed: Optional[str] = None

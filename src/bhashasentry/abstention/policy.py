from typing import Optional
from bhashasentry.core.types import AbstentionDecision, DecisionVerdict, ReliabilitySignal
from bhashasentry.config import BhashaSentryConfig, SupportedLanguage
from bhashasentry.abstention.refusal_generator import MultilingualRefusalEngine

class SelectiveAbstentionPolicy:
    """
    Three-Tier Selective Prediction Policy:
    - If composite_reliability >= tau_answer: ANSWER
    - If tau_warn <= composite_reliability < tau_answer: WARN
    - If composite_reliability < tau_warn: ABSTAIN
    """
    def __init__(self, config: Optional[BhashaSentryConfig] = None):
        self.config = config or BhashaSentryConfig()
        self.refusal_engine = MultilingualRefusalEngine()
        
    def decide(self, signal: ReliabilitySignal, lang: SupportedLanguage) -> AbstentionDecision:
        score = signal.composite_reliability_score
        risk = 1.0 - signal.calibrated_probability
        
        if score >= self.config.tau_answer:
            verdict = DecisionVerdict.ANSWER
            explanation = "Sufficient verified supporting evidence found across retrieved context."
            msg = ""
        elif score >= self.config.tau_warn:
            verdict = DecisionVerdict.WARN
            explanation = "Partial supporting evidence. Low cross-lingual confidence or partial claim support."
            msg = self.refusal_engine.get_warning_message(lang)
        else:
            verdict = DecisionVerdict.ABSTAIN
            explanation = "Insufficient or contradictory evidence. Refusing answer generation to prevent hallucination."
            msg = self.refusal_engine.get_refusal_message(lang)
            
        return AbstentionDecision(
            verdict=verdict,
            confidence=signal.composite_reliability_score,
            risk_score=round(risk, 4),
            explanation=explanation,
            localized_message=msg
        )

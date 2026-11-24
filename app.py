import sys
from pathlib import Path

# Add src to python path
REPO_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(REPO_ROOT / "src"))

import streamlit as st
import pandas as pd
import json

from bhashasentry.config import SupportedLanguage, BhashaSentryConfig
from bhashasentry.pipeline import BhashaSentryPipeline
from bhashasentry.data.dataset_loader import DatasetLoader
from bhashasentry.consistency.agreement_matrix import PairwiseConsistencyMatrix

st.set_page_config(
    page_title="BhashaSentry | Multilingual RAG Reliability",
    page_icon="🛡️",
    layout="wide"
)

# Custom CSS for research styling
st.markdown("""
<style>
    .main-header { font-size: 2.2rem; font-weight: 700; color: #1e293b; margin-bottom: 0.2rem; }
    .sub-header { font-size: 1.05rem; color: #64748b; margin-bottom: 1.5rem; }
    .metric-card { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 12px; }
    .badge-supported { background: #dcfce7; color: #166534; padding: 4px 8px; border-radius: 4px; font-weight: 600; font-size: 0.85rem; }
    .badge-refuted { background: #fee2e2; color: #991b1b; padding: 4px 8px; border-radius: 4px; font-weight: 600; font-size: 0.85rem; }
    .badge-ungrounded { background: #fef3c7; color: #92400e; padding: 4px 8px; border-radius: 4px; font-weight: 600; font-size: 0.85rem; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🛡️ BhashaSentry: Multilingual RAG Reliability Engine</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Cross-Lingual Evidence Traceability & Hallucination Detection across Indian Languages</div>', unsafe_allow_html=True)

# Initialize pipeline in cache
@st.cache_resource
def get_pipeline():
    pipe = BhashaSentryPipeline()
    loader = DatasetLoader()
    passages = loader.load_passages()
    pipe.index_knowledge_base(passages)
    return pipe

pipeline = get_pipeline()

# Sidebar controls
st.sidebar.header("⚙️ Query Configuration")

lang_options = {
    "Auto-Detect": None,
    "Telugu (తెలుగు)": SupportedLanguage.TE,
    "Tamil (தமிழ்)": SupportedLanguage.TA,
    "Hindi (हिन्दी)": SupportedLanguage.HI,
    "Bengali (বাংলা)": SupportedLanguage.BN,
    "Marathi (मराठी)": SupportedLanguage.MR,
    "English": SupportedLanguage.EN
}

selected_lang_label = st.sidebar.selectbox("Query Language", list(lang_options.keys()))
selected_lang = lang_options[selected_lang_label]

st.sidebar.subheader("Presets / Examples")
sample_queries = {
    "Custom Query": "",
    "Telugu: చంద్రయాన్-3 ల్యాండింగ్ ఎప్పుడు?": "చంద్రయాన్-3 చంద్రునిపై ఎప్పుడు దిగింది?",
    "Tamil: பிரகதீஸ்வரர் கோவில் யார் கட்டியது?": "தஞ்சாவூர் பிரகதீஸ்வரர் கோவில் யாரால் கட்டப்பட்டது?",
    "Hindi: चंद्रयान-3 कब और कहां उतरा था?": "चंद्रयान-3 चंद्रमा पर कब और कहां उतरा था?",
    "Bengali: চন্দ্রযান-৩ অভিযান": "চন্দ্রযান-৩ চাঁদে কখন অবতরণ করেছিল?",
    "Marathi: चांद्रयान-३ मोहीम": "चांद्रयान-३ चंद्रावर कधी उतरले?",
    "English: Chandrayaan-3 Landing": "When did Chandrayaan-3 land on the Moon?"
}

preset_choice = st.sidebar.selectbox("Choose a sample question", list(sample_queries.keys()))

st.sidebar.subheader("Reliability Thresholds")
tau_ans = st.sidebar.slider("τ Answer (Confident Answer)", 0.50, 0.95, 0.72, 0.01)
tau_warn = st.sidebar.slider("τ Warn (Answer with Warning)", 0.20, 0.70, 0.45, 0.01)

pipeline.config.tau_answer = tau_ans
pipeline.config.tau_warn = tau_warn
pipeline.abstention_policy.config.tau_answer = tau_ans
pipeline.abstention_policy.config.tau_warn = tau_warn

# Main input box
default_text = sample_queries[preset_choice] if preset_choice != "Custom Query" else ""
user_query = st.text_input("Enter question in Telugu, Tamil, Hindi, Bengali, Marathi, or English:", value=default_text, placeholder="e.g. చంద్రయాన్-3 ఎప్పుడు దిగింది?")

col_btn1, col_btn2 = st.columns([1, 5])
with col_btn1:
    run_btn = st.button("🚀 Analyze & Generate", type="primary", use_container_width=True)

if run_btn and user_query.strip():
    with st.spinner("Processing through 6-Stage BhashaSentry Pipeline..."):
        trace = pipeline.process_query(user_query, selected_lang)
        
    st.markdown("---")
    
    # 1. Decision Banner
    verdict = trace.decision.verdict.value
    if verdict == "ANSWER":
        st.success(f"### ✅ Decision: ANSWER (Reliable & Evidence-Supported)\\n**Confidence**: `{trace.decision.confidence:.2%}` | **Risk**: `{trace.decision.risk_score:.2%}`\\n\\n**Generated Response**:\\n\\n{trace.generated_answer}")
    elif verdict == "WARN":
        st.warning(f"### ⚠️ Decision: WARN (Partial Support / Cross-Lingual Caution)\\n**Confidence**: `{trace.decision.confidence:.2%}` | **Risk**: `{trace.decision.risk_score:.2%}`\\n\\n**Generated Response with Warning**:\\n\\n{trace.generated_answer}")
    else:
        st.error(f"### 🛑 Decision: ABSTAIN (Refusing to Answer to Prevent Hallucination)\\n**Confidence**: `{trace.decision.confidence:.2%}` | **Risk**: `{trace.decision.risk_score:.2%}`\\n\\n**Localized Refusal Message**:\\n\\n> *\"{trace.decision.localized_message}\"*\\n\\n*(Explanation: {trace.decision.explanation})*")
        
    # 2. Metric Cards
    st.markdown("### 📊 CLETR Multi-Signal Reliability Breakdown")
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Composite Reliability", f"{trace.reliability_signal.composite_reliability_score:.3f}")
    with m2:
        st.metric("Claim Support Ratio", f"{trace.reliability_signal.claim_support_ratio:.1%}")
    with m3:
        st.metric("Contradiction Penalty", f"{trace.reliability_signal.contradiction_penalty:.1%}")
    with m4:
        st.metric("Calibrated Probability", f"{trace.reliability_signal.calibrated_probability:.1%}")

    # Tabs for in-depth inspection
    tab_claims, tab_evidence, tab_matrix, tab_trace = st.tabs([
        "🔬 Atomic Claims & NLI",
        "📚 Retrieved Passages",
        "🌐 Cross-Lingual Consistency Matrix",
        "📜 Audit Trace (JSON)"
    ])
    
    with tab_claims:
        st.subheader("Decomposed Atomic Propositions")
        if trace.claim_verifications:
            claim_rows = []
            for cv in trace.claim_verifications:
                claim_rows.append({
                    "Claim ID": cv.claim_id,
                    "Proposition Text": cv.claim_text,
                    "Verdict": cv.verdict.value,
                    "Entailment Score": f"{cv.entailment_score:.3f}",
                    "Contradiction Score": f"{cv.contradiction_score:.3f}",
                    "Supporting Docs": ", ".join(cv.supporting_passage_ids) if cv.supporting_passage_ids else "None"
                })
            df_claims = pd.DataFrame(claim_rows)
            st.dataframe(df_claims, use_container_width=True)
        else:
            st.info("No atomic claims extracted (e.g. system abstained or refusal triggered).")

    with tab_evidence:
        st.subheader("Retrieved Context Passages (Hybrid RRF)")
        for idx, p in enumerate(trace.retrieved_passages):
            with st.expander(f"Passage {idx+1}: [{p.id}] - Language: {p.language.upper()} (RRF Score: {p.score:.4f})"):
                st.write(p.text)
                st.caption(f"Domain: {p.domain} | Gold Passage: {p.is_gold}")

    with tab_matrix:
        st.subheader("6x6 Pairwise Factual Agreement Matrix")
        st.write("Cross-lingual mutual entailment across English, Hindi, Telugu, Tamil, Bengali, and Marathi:")
        matrix_gen = PairwiseConsistencyMatrix()
        sample_parallel = {
            SupportedLanguage.EN: "Chandrayaan-3 landed on 23 August 2023.",
            SupportedLanguage.HI: "चंद्रयान-3 23 अगस्त 2023 को उतरा।",
            SupportedLanguage.TE: "చంద్రయాన్-3 23 ఆగస్టు 2023న దిగింది.",
            SupportedLanguage.TA: "சந்திரயான்-3 2023 ஆகஸ்ட் 23 அன்று தரையிறங்கியது.",
            SupportedLanguage.BN: "চন্দ্রযান-৩ ২৩ আগস্ট ২০২৩ তারিখে অবতরণ করেছিল।",
            SupportedLanguage.MR: "चांद्रयान-३ २३ ऑगस्ट २०२३ रोजी उतरले."
        }
        matrix = matrix_gen.compute_matrix(sample_parallel)
        df_matrix = pd.DataFrame(matrix, index=["EN", "HI", "TE", "TA", "BN", "MR"], columns=["EN", "HI", "TE", "TA", "BN", "MR"])
        st.dataframe(df_matrix.style.background_gradient(cmap="Greens", vmin=0.5, vmax=1.0), use_container_width=True)

    with tab_trace:
        st.subheader("Raw Audit Log Trace")
        st.json(trace.model_dump())

st.markdown("---")
st.caption("BhashaSentry Research Framework | Developed by Nani Toka (2026)")

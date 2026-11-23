from typing import List, Dict

QUALITATIVE_CASES = [
    {
        "case_id": "case_te_chandrayaan",
        "language": "te",
        "query": "చంద్రయాన్-3 చంద్రునిపై ఎప్పుడు దిగింది?",
        "source_doc_en": "Chandrayaan-3 made a soft landing on 23 August 2023.",
        "standard_rag_ans": "చంద్రయాన్-3 14 జూలై 2023న చంద్రునిపై విజయవంతంగా దిగింది.",
        "failure_mode": "Problem D (Date Swapping): Substituted landing date (23 August) with launch date (14 July).",
        "bhashasentry_decision": "ABSTAIN / WARN",
        "bhashasentry_corrected_ans": "చంద్రయాన్-3 ఆగస్టు 23, 2023న చంద్రుని దక్షిణ ధ్రువ ప్రాంతంలో దిగింది. [Doc-space_01]"
    },
    {
        "case_id": "case_ta_brihadisvara",
        "language": "ta",
        "query": "தஞ்சாவூர் பிரகதீஸ்வரர் கோவில் யாரால் கட்டப்பட்டது?",
        "source_doc_en": "Brihadisvara Temple was built by Raja Raja Chola I between 1003 and 1010 CE.",
        "standard_rag_ans": "தஞ்சாவூர் பிரகதீஸ்வரர் கோவில் ராஜேந்திர சோழனால் கட்டப்பட்டது.",
        "failure_mode": "Problem D (Entity Drift): Substituted father Raja Raja Chola I with son Rajendra Chola.",
        "bhashasentry_decision": "WARN",
        "bhashasentry_corrected_ans": "முதலாம் இராஜராஜ சோழனால் கட்டப்பட்டது. [Doc-temple_01]"
    }
]

if __name__ == "__main__":
    print(f"Loaded {len(QUALITATIVE_CASES)} qualitative case studies.")

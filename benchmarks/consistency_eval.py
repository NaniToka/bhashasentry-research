import json
from bhashasentry.consistency.agreement_matrix import PairwiseConsistencyMatrix
from bhashasentry.config import SupportedLanguage

def evaluate_cross_lingual_consistency():
    matrix_gen = PairwiseConsistencyMatrix()
    sample_answers = {
        SupportedLanguage.EN: "Vikram lander landed near the lunar south pole on August 23, 2023.",
        SupportedLanguage.HI: "विक्रम लैंडर 23 अगस्त 2023 को चंद्रमा के दक्षिणी ध्रुव पर उतरा।",
        SupportedLanguage.TE: "విక్రమ్ ల్యాండర్ ఆగస్టు 23, 2023న చంద్రుని దక్షిణ ధ్రువ ప్రాంతంలో దిగింది.",
        SupportedLanguage.TA: "விக்ரம் லேண்டர் 2023 ஆகஸ்ட் 23 அன்று நிலவின் தென் துருவத்தில் இறங்கியது.",
        SupportedLanguage.BN: "বিক্রম ল্যান্ডার ২৩ আগস্ট ২০২৩ তারিখে চাঁদের দক্ষিণ মেরুতে নেমেছিল।",
        SupportedLanguage.MR: "विक्रम लँडर २३ ऑगस्ट २०२३ रोजी चंद्राच्या दक्षिण ध्रुवावर उतरले."
    }
    matrix = matrix_gen.compute_matrix(sample_answers)
    return {
        "languages": [l.value for l in matrix_gen.langs],
        "consistency_matrix": matrix
    }

if __name__ == "__main__":
    out = evaluate_cross_lingual_consistency()
    print("Cross-Lingual Consistency Benchmark:")
    print(json.dumps(out, indent=2))

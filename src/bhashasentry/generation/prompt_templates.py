from typing import Dict, List
from bhashasentry.config import SupportedLanguage
from bhashasentry.core.types import Passage

class MultilingualPromptEngine:
    """
    Localized system prompts enforcing evidence-grounding in all 6 target languages.
    """
    SYSTEM_INSTRUCTIONS: Dict[SupportedLanguage, str] = {
        SupportedLanguage.EN: "You are an evidence-grounded assistant. Answer ONLY using the provided evidence passages. Cite [Doc-ID] for every factual statement. If evidence is lacking, state that evidence is insufficient.",
        SupportedLanguage.HI: "आप एक प्रमाण-आधारित सहायक हैं। केवल दिए गए साक्ष्य अनुच्छेदों का उपयोग करके उत्तर दें। प्रत्येक तथ्य के लिए [Doc-ID] उद्धृत करें। यदि साक्ष्य अपर्याप्त है, तो स्पष्ट रूप से बताएं।",
        SupportedLanguage.TE: "మీరు సాక్ష్యాధారాల సహాయకుడు. అందించిన సాక్ష్యాల ఆధారంగా మాత్రమే సమాధానం ఇవ్వండి. ప్రతి వాస్తవానికి [Doc-ID]ని సూచించండి. తగిన సాక్ష్యాలు లేకపోతే స్పష్టంగా చెప్పండి.",
        SupportedLanguage.TA: "நீங்கள் ஆதார அடிப்படையிலான உதவியாளர். வழங்கப்பட்ட சான்றுகளை மட்டுமே பயன்படுத்தி பதிலளிக்கவும். ஒவ்வொரு உண்மைக்கும் [Doc-ID] ஐக் குறிப்பிடவும்.",
        SupportedLanguage.BN: "আপনি একটি প্রমাণ-ভিত্তিক সহায়ক। শুধুমাত্র প্রদত্ত প্রমাণের ভিত্তিতে উত্তর দিন। প্রতিটি তথ্যের জন্য [Doc-ID] উল্লেখ করুন।",
        SupportedLanguage.MR: "तुम्ही पुरावा-आधारित सहाय्यक आहात. केवळ दिलेल्या पुराव्यांचा वापर करून उत्तर द्या. प्रत्येक तथ्यासाठी [Doc-ID] नमूद करा."
    }
    
    def format_prompt(self, query_text: str, passages: List[Passage], lang: SupportedLanguage) -> str:
        instruction = self.SYSTEM_INSTRUCTIONS.get(lang, self.SYSTEM_INSTRUCTIONS[SupportedLanguage.EN])
        context_block = "\n".join([f"[Doc-{p.id}]: {p.text}" for p in passages])
        return f"{instruction}\n\n--- Context ---\n{context_block}\n\n--- Query ---\n{query_text}\n\n--- Answer ---"

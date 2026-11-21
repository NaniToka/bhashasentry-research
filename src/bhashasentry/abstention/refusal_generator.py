from typing import Dict
from bhashasentry.config import SupportedLanguage

class MultilingualRefusalEngine:
    """
    Generates culturally fluent, polite, and precise refusal and warning messages
    across all 6 target languages: en, hi, te, ta, bn, mr.
    """
    REFUSALS: Dict[SupportedLanguage, str] = {
        SupportedLanguage.EN: "I cannot answer this question reliably because the available evidence is insufficient.",
        SupportedLanguage.HI: "मैं इस प्रश्न का उत्तर प्रमाणिकता से नहीं दे सकता क्योंकि उपलब्ध साक्ष्य अपर्याप्त हैं।",
        SupportedLanguage.TE: "అందుబాటులో ఉన్న ఆధారాలు సరిపోనందున నేను ఈ ప్రశ్నకు నమ్మదగిన సమాధానం ఇవ్వలేను.",
        SupportedLanguage.TA: "கிடைக்கக்கூடிய ஆதாரங்கள் போதுமானதாக இல்லாததால் என்னால் இந்த கேள்விக்கு நம்பகமான பதிலை அளிக்க முடியவில்லை.",
        SupportedLanguage.BN: "উপলব্ধ প্রমাণ পর্যাপ্ত না হওয়ায় আমি এই প্রশ্নের একটি নির্ভরযোগ্য উত্তর দিতে পারছি না।",
        SupportedLanguage.MR: "उपलब्ध पुरावे अपुरे असल्याने मी या प्रश्नाचे विश्वासार्ह उत्तर देऊ शकत नाही."
    }
    
    WARNINGS: Dict[SupportedLanguage, str] = {
        SupportedLanguage.EN: "Warning: Supporting evidence for this answer is partial and may contain inaccuracies.",
        SupportedLanguage.HI: "चेतावनी: इस उत्तर के लिए साक्ष्य आंशिक हैं और इसमें अशुद्धियां हो सकती हैं।",
        SupportedLanguage.TE: "హెచ్చరిక: ఈ సమాధానానికి ఆధారాలు పాక్షికంగా మాత్రమే ఉన్నాయి, ఇందులో లోపాలు ఉండవచ్చు.",
        SupportedLanguage.TA: "எச்சரிக்கை: இந்த பதிலுக்கான சான்றுகள் பகுதியளவு மட்டுமே உள்ளன.",
        SupportedLanguage.BN: "সতর্কতা: এই উত্তরের প্রমাণ আংশিক এবং এতে ত্রুটি থাকতে পারে।",
        SupportedLanguage.MR: "इशारा: या उत्तरासाठीचे पुरावे अंशतः आहेत आणि त्यात त्रुटी असू शकतात."
    }
    
    def get_refusal_message(self, lang: SupportedLanguage) -> str:
        return self.REFUSALS.get(lang, self.REFUSALS[SupportedLanguage.EN])
        
    def get_warning_message(self, lang: SupportedLanguage) -> str:
        return self.WARNINGS.get(lang, self.WARNINGS[SupportedLanguage.EN])

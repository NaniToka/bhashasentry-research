import unittest
from bhashasentry.config import SupportedLanguage
from bhashasentry.nlp.normalizer import IndicNormalizer
from bhashasentry.nlp.lang_id import IndicLanguageIdentifier
from bhashasentry.nlp.tokenizer import IndicTokenizer

class TestIndicNLP(unittest.TestCase):
    def setUp(self):
        self.normalizer = IndicNormalizer()
        self.lang_id = IndicLanguageIdentifier()
        self.tokenizer = IndicTokenizer()
        
    def test_telugu_lang_id(self):
        text = "ఇస్రో చంద్రయాన్-3 మిషన్ విజయవంతంగా చంద్రుని దక్షిణ ధ్రువంపై దిగింది."
        lang, conf = self.lang_id.identify(text)
        self.assertEqual(lang, SupportedLanguage.TE)
        self.assertGreater(conf, 0.5)

    def test_hindi_lang_id(self):
        text = "भारतीय अंतरिक्ष अनुसंधान संगठन ने चंद्रयान-3 का सफल प्रक्षेपण किया।"
        lang, conf = self.lang_id.identify(text)
        self.assertEqual(lang, SupportedLanguage.HI)

    def test_tamil_lang_id(self):
        text = "சந்திரயான் 3 விண்கலம் நிலவின் தென் துருவத்தில் வெற்றிகரமாக தரையிறங்கியது."
        lang, conf = self.lang_id.identify(text)
        self.assertEqual(lang, SupportedLanguage.TA)

    def test_bengali_lang_id(self):
        text = "চন্দ্রযান-৩ সফলভাবে চাঁদের দক্ষিণ মেরুতে অবতরণ করেছে।"
        lang, conf = self.lang_id.identify(text)
        self.assertEqual(lang, SupportedLanguage.BN)

    def test_english_lang_id(self):
        text = "ISRO successfully landed Chandrayaan-3 on the lunar south pole."
        lang, conf = self.lang_id.identify(text)
        self.assertEqual(lang, SupportedLanguage.EN)

    def test_sentence_tokenization(self):
        text = "చంద్రయాన్ 3 విజయం సాధించింది. ఇది భారతీయ విజ్ఞాన ఘనత! అద్భుతం."
        sents = self.tokenizer.split_sentences(text)
        self.assertEqual(len(sents), 3)

if __name__ == "__main__":
    unittest.main()

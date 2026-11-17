import unittest
from bhashasentry.config import SupportedLanguage
from bhashasentry.core.types import Query, Passage
from bhashasentry.generation.prompt_templates import MultilingualPromptEngine
from bhashasentry.generation.constrained import EvidenceConstrainedGenerator
from bhashasentry.generation.perturbations import HallucinationPerturber

class TestGeneration(unittest.TestCase):
    def setUp(self):
        self.engine = MultilingualPromptEngine()
        self.generator = EvidenceConstrainedGenerator()
        self.perturber = HallucinationPerturber()
        self.passages = [
            Passage(id="doc_1", text="ISRO launched Chandrayaan-3 on 14 July 2023.", language=SupportedLanguage.EN, is_gold=True)
        ]
        
    def test_telugu_prompt(self):
        prompt = self.engine.format_prompt("చంద్రయాన్ ఎప్పుడు ప్రయోగించారు?", self.passages, SupportedLanguage.TE)
        self.assertIn("సాక్ష్యాధారాల సహాయకుడు", prompt)
        self.assertIn("[Doc-doc_1]", prompt)

    def test_constrained_generator(self):
        q = Query(id="q1", text="When was Chandrayaan-3 launched?", language=SupportedLanguage.EN)
        ans = self.generator.generate(q, self.passages)
        self.assertIn("[Doc-doc_1]", ans)

    def test_number_perturbation(self):
        orig = "Launched in 2023 on day 14."
        pert, changed = self.perturber.perturb_numbers(orig)
        self.assertTrue(changed)
        self.assertNotEqual(orig, pert)

if __name__ == "__main__":
    unittest.main()

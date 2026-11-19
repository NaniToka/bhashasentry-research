import unittest
from bhashasentry.config import SupportedLanguage
from bhashasentry.consistency.cross_lingual_parity import CrossLingualParityEvaluator
from bhashasentry.consistency.agreement_matrix import PairwiseConsistencyMatrix

class TestConsistency(unittest.TestCase):
    def setUp(self):
        self.parity = CrossLingualParityEvaluator()
        self.matrix_gen = PairwiseConsistencyMatrix()
        
    def test_consistent_answers(self):
        en_ans = "Chandrayaan-3 landed on 23 August 2023."
        te_ans = "చంద్రయాన్-3 23 ఆగస్టు 2023న దిగింది."
        res = self.parity.evaluate_pair("q1", en_ans, SupportedLanguage.EN, te_ans, SupportedLanguage.TE)
        self.assertFalse(res.is_contradictory)
        self.assertGreater(res.mutual_entailment, 0.7)

    def test_inconsistent_answers(self):
        en_ans = "Chandrayaan-3 landed on 23 August 2023."
        te_ans = "చంద్రయాన్-3 15 జూలై 2019న దిగింది."
        res = self.parity.evaluate_pair("q2", en_ans, SupportedLanguage.EN, te_ans, SupportedLanguage.TE)
        self.assertTrue(res.is_contradictory)
        self.assertLess(res.mutual_entailment, 0.5)

    def test_agreement_matrix(self):
        answers = {
            SupportedLanguage.EN: "2023",
            SupportedLanguage.HI: "2023",
            SupportedLanguage.TE: "2023",
            SupportedLanguage.TA: "2023",
            SupportedLanguage.BN: "2023",
            SupportedLanguage.MR: "2023"
        }
        matrix = self.matrix_gen.compute_matrix(answers)
        self.assertEqual(len(matrix), 6)
        self.assertEqual(matrix[0][0], 1.0)

if __name__ == "__main__":
    unittest.main()

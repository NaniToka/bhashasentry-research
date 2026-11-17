import re
import random
from typing import Tuple

class HallucinationPerturber:
    """
    Systematically injects synthetic hallucinations (Problem D) into text
    by perturbing dates, numerical quantities, and named entities.
    """
    def perturb_numbers(self, text: str) -> Tuple[str, bool]:
        numbers = re.findall(r"\b\d{4}\b|\b\d{1,3}\b", text)
        if not numbers:
            return text, False
            
        target = random.choice(numbers)
        if len(target) == 4:
            # Shift year by 3 to 5 years
            replacement = str(int(target) - 4)
        else:
            replacement = str(int(target) + 12)
            
        perturbed = re.sub(rf"\b{target}\b", replacement, text, count=1)
        return perturbed, True

    def inject_false_negation(self, text: str) -> str:
        if "was" in text:
            return text.replace("was", "was not", 1)
        elif "is" in text:
            return text.replace("is", "is not", 1)
        elif "దిగింది" in text:
            return text.replace("దిగింది", "దిగలేదు", 1)
        elif "था" in text:
            return text.replace("था", "नहीं था", 1)
        return text + " [NEGATED]"

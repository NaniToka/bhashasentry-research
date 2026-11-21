from typing import List, Dict

class CoverageRiskVisualizer:
    """
    Generates text and ASCII summaries of the Coverage-Risk curve.
    """
    def format_ascii_table(self, curve_data: List[Dict[str, float]]) -> str:
        lines = ["Threshold | Coverage | Risk"]
        lines.append("----------|----------|------")
        for row in curve_data:
            lines.append(f"  {row['threshold']:.2f}    |  {row['coverage']*100:5.1f}%  | {row['risk']*100:4.1f}%")
        return "\n".join(lines)

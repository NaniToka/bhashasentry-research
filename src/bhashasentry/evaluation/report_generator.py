import json
from typing import Dict, Any

class HTMLReportGenerator:
    """
    Generates rich HTML reports summarizing reliability audits,
    evidence citations, and cross-lingual consistency.
    """
    def generate_html(self, report_data: Dict[str, Any]) -> str:
        return f"""<!DOCTYPE html>
<html>
<head><title>BhashaSentry Audit Report</title></head>
<body>
<h1>BhashaSentry Reliability Audit Report</h1>
<pre>{json.dumps(report_data, indent=2)}</pre>
</body>
</html>"""

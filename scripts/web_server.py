#!/usr/bin/env python3
"""
BhashaSentry Standalone Localhost Web Server (Flask)
Serves interactive web dashboard on http://localhost:8000
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from flask import Flask, request, jsonify, render_template_string
from bhashasentry.pipeline import BhashaSentryPipeline
from bhashasentry.data.dataset_loader import DatasetLoader
from bhashasentry.config import SupportedLanguage

app = Flask(__name__)

# Initialize pipeline
pipeline = BhashaSentryPipeline()
loader = DatasetLoader()
passages = loader.load_passages()
pipeline.index_knowledge_base(passages)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>BhashaSentry | Multilingual RAG Dashboard</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    body { background-color: #f8fafc; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
    .header-box { background: white; border-bottom: 1px solid #e2e8f0; padding: 24px 0; margin-bottom: 24px; }
    .card { border-radius: 8px; border: 1px solid #e2e8f0; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
    .decision-ANSWER { background: #dcfce7; color: #166534; border: 1px solid #bbf7d0; }
    .decision-WARN { background: #fef3c7; color: #92400e; border: 1px solid #fde68a; }
    .decision-ABSTAIN { background: #fee2e2; color: #991b1b; border: 1px solid #fecaca; }
  </style>
</head>
<body>
  <div class="header-box">
    <div class="container">
      <h2 class="fw-bold mb-1">🛡️ BhashaSentry</h2>
      <p class="text-muted mb-0">Multilingual Evidence Reliability and Cross-Lingual Hallucination Detection Engine in RAG</p>
    </div>
  </div>

  <div class="container mb-5">
    <div class="row">
      <div class="col-lg-4 mb-4">
        <div class="card p-4">
          <h5 class="fw-bold mb-3">Query Settings</h5>
          <div class="mb-3">
            <label class="form-label">Select Sample Question:</label>
            <select class="form-select" id="sampleSelect" onchange="applySample()">
              <option value="">-- Choose Preset --</option>
              <option value="చంద్రయాన్-3 చంద్రునిపై ఎప్పుడు దిగింది?">Telugu: చంద్రయాన్-3 ల్యాండింగ్ ఎప్పుడు?</option>
              <option value="தஞ்சாவூர் பிரகதீஸ்வரர் கோவில் யாரால் கட்டப்பட்டது?">Tamil: பிரகதீஸ்வரர் கோவில் யார் கட்டியது?</option>
              <option value="चंद्रयान-3 चंद्रमा पर कब और कहां उतरा था?">Hindi: चंद्रयान-3 कब और कहां उतरा था?</option>
              <option value="চন্দ্রযান-৩ চাঁদে কখন অবতরণ করেছিল?">Bengali: চন্দ্রযান-৩ অভিযান</option>
              <option value="चांद्रयान-३ चंद्रावर कधी उतरले?">Marathi: चांद्रयान-३ मोहीम</option>
              <option value="When did Chandrayaan-3 land on the Moon?">English: Chandrayaan-3 Landing</option>
            </select>
          </div>
          <div class="mb-3">
            <label class="form-label">Language:</label>
            <select class="form-select" id="langSelect">
              <option value="">Auto-Detect</option>
              <option value="te">Telugu (తెలుగు)</option>
              <option value="ta">Tamil (தமிழ்)</option>
              <option value="hi">Hindi (हिन्दी)</option>
              <option value="bn">Bengali (বাংলা)</option>
              <option value="mr">Marathi (मराठी)</option>
              <option value="en">English</option>
            </select>
          </div>
          <button class="btn btn-primary w-100 py-2 fw-semibold" onclick="runAudit()">Run Pipeline Audit 🚀</button>
        </div>
      </div>

      <div class="col-lg-8">
        <div class="card p-4 mb-4">
          <h5 class="fw-bold mb-3">Input Question</h5>
          <textarea class="form-control mb-3" id="queryInput" rows="3" placeholder="Enter question in Telugu, Tamil, Hindi, Bengali, Marathi, or English..."></textarea>
          <div id="loading" class="text-center py-4" style="display:none;">
            <div class="spinner-border text-primary" role="status"></div>
            <p class="mt-2 text-muted">Running 6-Stage Evidence Audit...</p>
          </div>
          <div id="resultsArea" style="display:none;">
            <div id="decisionBanner" class="p-3 rounded mb-3"></div>
            
            <div class="row text-center mb-4">
              <div class="col-3">
                <div class="p-2 border rounded bg-light">
                  <small class="text-muted d-block">Reliability</small>
                  <strong class="fs-5" id="valRel">-</strong>
                </div>
              </div>
              <div class="col-3">
                <div class="p-2 border rounded bg-light">
                  <small class="text-muted d-block">Claim Support</small>
                  <strong class="fs-5" id="valSup">-</strong>
                </div>
              </div>
              <div class="col-3">
                <div class="p-2 border rounded bg-light">
                  <small class="text-muted d-block">Contradiction</small>
                  <strong class="fs-5" id="valContra">-</strong>
                </div>
              </div>
              <div class="col-3">
                <div class="p-2 border rounded bg-light">
                  <small class="text-muted d-block">Confidence</small>
                  <strong class="fs-5" id="valConf">-</strong>
                </div>
              </div>
            </div>

            <h6 class="fw-bold">Generated Answer / Decision:</h6>
            <div class="p-3 bg-white border rounded mb-3" id="answerText"></div>

            <h6 class="fw-bold">Atomic Proposition Verification (NLI):</h6>
            <div class="table-responsive">
              <table class="table table-sm table-bordered">
                <thead class="table-light">
                  <tr><th>Proposition</th><th>Verdict</th><th>Entailment</th><th>Contradiction</th></tr>
                </thead>
                <tbody id="claimsTable"></tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <script>
    function applySample() {
      const val = document.getElementById('sampleSelect').value;
      if (val) document.getElementById('queryInput').value = val;
    }

    async function runAudit() {
      const q = document.getElementById('queryInput').value.trim();
      const l = document.getElementById('langSelect').value;
      if (!q) return alert('Please enter a query.');
      
      document.getElementById('loading').style.display = 'block';
      document.getElementById('resultsArea').style.display = 'none';

      try {
        const res = await fetch('/api/query', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({query: q, language: l})
        });
        const data = await res.json();
        
        document.getElementById('loading').style.display = 'none';
        document.getElementById('resultsArea').style.display = 'block';

        const dec = data.decision;
        const banner = document.getElementById('decisionBanner');
        banner.className = 'p-3 rounded mb-3 decision-' + dec.verdict;
        banner.innerHTML = '<strong>Decision: ' + dec.verdict + '</strong> &bull; ' + dec.explanation;

        document.getElementById('valRel').innerText = data.reliability_signal.composite_reliability_score.toFixed(3);
        document.getElementById('valSup').innerText = (data.reliability_signal.claim_support_ratio * 100).toFixed(0) + '%';
        document.getElementById('valContra').innerText = (data.reliability_signal.contradiction_penalty * 100).toFixed(0) + '%';
        document.getElementById('valConf').innerText = (data.reliability_signal.calibrated_probability * 100).toFixed(0) + '%';

        document.getElementById('answerText').innerText = data.generated_answer;

        const tbody = document.getElementById('claimsTable');
        tbody.innerHTML = '';
        if (data.claim_verifications && data.claim_verifications.length > 0) {
          data.claim_verifications.forEach(c => {
            const tr = document.createElement('tr');
            tr.innerHTML = '<td>' + c.claim_text + '</td><td><span class="badge bg-' + (c.verdict === 'SUPPORTED' ? 'success' : (c.verdict === 'REFUTED' ? 'danger' : 'warning text-dark')) + '">' + c.verdict + '</span></td><td>' + c.entailment_score.toFixed(2) + '</td><td>' + c.contradiction_score.toFixed(2) + '</td>';
            tbody.appendChild(tr);
          });
        } else {
          tbody.innerHTML = '<tr><td colspan="4" class="text-muted text-center">No atomic claims extracted (Abstained).</td></tr>';
        }
      } catch (err) {
        document.getElementById('loading').style.display = 'none';
        alert('Audit request failed: ' + err);
      }
    }
  </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route("/api/query", methods=["POST"])
def query_endpoint():
    data = request.json or {}
    q_text = data.get("query", "")
    q_lang_str = data.get("language", "")
    q_lang = SupportedLanguage(q_lang_str) if q_lang_str else None
    
    trace = pipeline.process_query(q_text, q_lang)
    return jsonify(trace.model_dump())

if __name__ == "__main__":
    port = 8000
    print(f"Starting BhashaSentry Dashboard on http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=False)

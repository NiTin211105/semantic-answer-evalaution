import os
import tempfile
from flask import Flask, request, render_template_string

from question_loader import load_questions

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  # 10 MB

HTML = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>AI Answer Evaluation System</title>
  <style>
    body { font-family: Arial, sans-serif; max-width: 850px; margin: 40px auto; padding: 0 18px; background:#f5f7fb; }
    .card { background:white; padding:28px; border-radius:14px; box-shadow:0 2px 12px #0001; margin-bottom:20px; }
    h1 { margin-top:0; }
    label { font-weight:600; display:block; margin:15px 0 7px; }
    input, select, button { width:100%; box-sizing:border-box; padding:11px; border-radius:8px; border:1px solid #ccc; }
    button { margin-top:20px; cursor:pointer; font-weight:700; }
    .marks { font-size:28px; font-weight:700; }
    .good { color:#16803c; } .bad { color:#b42318; }
    pre { white-space:pre-wrap; background:#f3f4f6; padding:15px; border-radius:8px; }
    table { width:100%; border-collapse:collapse; margin-top:12px; }
    th,td { padding:10px; border-bottom:1px solid #ddd; text-align:left; vertical-align:top; }
    .error { background:#fee4e2; padding:12px; border-radius:8px; color:#8a1c13; }
    .note { color:#555; font-size:14px; }
  </style>
</head>
<body>
<div class="card">
  <h1>AI-Based Short Answer Evaluation</h1>
  <p>Upload a student's answer image. The system uses OCR and semantic similarity to evaluate key-point coverage.</p>
  {% if error %}<div class="error">{{ error }}</div>{% endif %}
  <form method="post" enctype="multipart/form-data">
    <label for="question_id">Question</label>
    <select name="question_id" id="question_id" required>
      {% for q in questions %}
        <option value="{{ q.question_id }}">{{ q.question_id }} — {{ q.question_text }}</option>
      {% endfor %}
    </select>
    <label for="image">Answer image</label>
    <input type="file" name="image" id="image" accept="image/*" required>
    <button type="submit">Evaluate Answer</button>
  </form>
  <p class="note">Tip: use a clear, well-lit image with the answer visible.</p>
</div>

{% if result %}
<div class="card">
  <h2>Evaluation Result</h2>
  <div class="marks">{{ result.marks_result.awarded_marks }} / {{ result.marks_result.total_marks }}</div>
  <p>{{ result.marks_result.points_covered }} / {{ result.marks_result.points_total }} key points covered.</p>

  {% if not result.quality_check.is_likely_valid %}
    <div class="error">
      <strong>OCR Quality Warning:</strong> {{ result.quality_check.reason }}
      <ul>{% for w in result.quality_check.warnings %}<li>{{ w }}</li>{% endfor %}</ul>
    </div>
  {% endif %}

  <h3>Question</h3>
  <p>{{ result.question_text }}</p>

  <h3>Extracted Answer</h3>
  <pre>{{ result.cleaned_text }}</pre>

  <h3>Key Point Coverage</h3>
  <table>
    <tr><th>Status</th><th>Key Point</th><th>Score</th></tr>
    {% for r in result.coverage_results %}
    <tr>
      <td class="{{ 'good' if r.covered else 'bad' }}">{{ 'Covered' if r.covered else 'Missing' }}</td>
      <td>{{ r.point_text }}</td>
      <td>{{ r.score }}</td>
    </tr>
    {% endfor %}
  </table>

  <h3>Feedback</h3>
  <pre>{{ result.feedback }}</pre>
</div>
{% endif %}
</body>
</html>
"""

QUESTIONS = load_questions()

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None

    if request.method == "POST":
      from main import evaluate_answer
        uploaded = request.files.get("image")
        question_id = request.form.get("question_id")

        if not uploaded or not uploaded.filename:
            error = "Please upload an answer image."
        elif not question_id:
            error = "Please select a question."
        else:
          from main import evaluate_answer
            suffix = os.path.splitext(uploaded.filename)[1].lower() or ".jpg"
            fd, path = tempfile.mkstemp(suffix=suffix)
            os.close(fd)
            try:
                uploaded.save(path)
                result = evaluate_answer(path, question_id)
            except Exception as exc:
                error = f"Evaluation failed: {exc}"
            finally:
                # main.py creates a *_cleaned.jpg beside the uploaded file
                for p in (path, os.path.splitext(path)[0] + "_cleaned.jpg"):
                    try:
                        os.remove(p)
                    except OSError:
                        pass

    return render_template_string(HTML, questions=QUESTIONS, result=result, error=error)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

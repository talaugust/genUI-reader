from flask import Flask, render_template, jsonify, send_file, request
import json
import os
import re
import requests

app = Flask(__name__)

# --- CONFIGURATION ---
# Lumen is UIUC's OpenAI-compatible LLM gateway: https://lumen.ncsa.illinois.edu/help/api
# Set your key in the terminal first:  export LUMEN_API_KEY="sk_..."
API_KEY = os.getenv("LUMEN_API_KEY", "")
LUMEN_URL = os.getenv("LUMEN_BASE_URL", "https://lumen.ncsa.illinois.edu/v1") + "/chat/completions"

# Run `python example_call.py` to list the exact model IDs your key can use.
MODEL = "gemma-4-31b-it"

# Passages longer than this are cut off before being sent to the model.
MAX_PASSAGE_CHARS = 2000


# --- THE COMPONENT CATALOG ---
# Every component the model is allowed to choose from. The model sees this
# catalog in its prompt (see catalog_text below) and must answer with JSON like:
#   {"component": "step_list", "props": {"title": "...", "steps": ["...", "..."]}}
#
# Each component here needs a matching renderer in static/components.js.
COMPONENTS = {
    "definition_card": {
        "use_when": "the passage hinges on one technical term or unfamiliar concept",
        "props": {
            "term": "string - the term being defined",
            "definition": "string - one or two plain-language sentences",
            "example": "string - a short everyday example (optional)",
        },
    },
    "step_list": {
        "use_when": "the passage describes a process, method, or sequence of events",
        "props": {
            "title": "string - what the steps accomplish",
            "steps": "list of strings - each step in order, one short sentence each",
        },
    },
    "comparison_table": {
        "use_when": "the passage compares two or more things (conditions, systems, groups, results)",
        "props": {
            "title": "string - what is being compared",
            "columns": "list of strings - column headers, first column names the rows",
            "rows": "list of lists of strings - one list per row, same length as columns",
        },
    },
    # =========================================================
    # YOUR TASK (Part 2, step 2 of 2): Add your new component here,
    # using the same shape as the entries above. The name must
    # match the renderer you add in static/components.js.
    # =========================================================
}


def catalog_text():
    """Turns COMPONENTS into a plain-text description to paste into a prompt."""
    lines = []
    for name, info in COMPONENTS.items():
        lines.append(f'- "{name}": use when {info["use_when"]}.')
        for prop, desc in info["props"].items():
            lines.append(f'    "{prop}": {desc}')
    return "\n".join(lines)


def extract_json(text):
    """
    Models often wrap JSON in ```json fences or add a sentence before it.
    This pulls out the first {...} object and parses it.
    Returns a dict, or None if no valid JSON was found.
    """
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        return None
    try:
        return json.loads(match.group(0))
    except json.JSONDecodeError:
        return None


def extract_html(text):
    """Strips ```html fences if the model added them."""
    match = re.search(r"```(?:html)?\s*(.*?)```", text, re.DOTALL)
    return match.group(1).strip() if match else text.strip()


def call_lumen(prompt):
    # =========================================================
    # YOUR TASK (Part 1, step 1 of 3): Send `prompt` to the model
    # and return the text of its reply as a string.
    #
    # Use requests.post(LUMEN_URL, headers=..., json=...)
    #
    # HEADERS:
    #   {"Authorization": f"Bearer {API_KEY}"}
    #
    # REQUEST BODY:
    #   {"model": MODEL, "messages": [{"role": "user", "content": prompt}]}
    #
    # EXTRACTING THE RESPONSE TEXT:
    #   response.raise_for_status()   # turns HTTP errors into a readable exception
    #   data = response.json()
    #   text = data["choices"][0]["message"]["content"]
    #
    # HINT: example_call.py makes this exact request. Get it working first.
    # =========================================================
    return "call_lumen() is not implemented yet."


def build_catalog_prompt(passage):
    # =========================================================
    # YOUR TASK (Part 1, step 2 of 3): Write the prompt that asks the
    # model to pick ONE component from the catalog for this passage.
    #
    # A good prompt tells the model:
    #   - who the reader is and what the widget is for
    #   - the catalog of components (catalog_text() writes this for you)
    #   - the exact JSON shape to answer with, and to answer with ONLY JSON
    #   - the passage itself
    #
    # Test it on several passages. Expect to rewrite it a few times.
    # =========================================================
    return f"""TODO: write your instructions here.

Components:
{catalog_text()}

Passage:
\"\"\"{passage}\"\"\"
"""


def build_freeform_prompt(passage):
    # =========================================================
    # YOUR TASK (Part 3): Write a prompt that asks the model to create
    # a self-contained HTML widget (inline <style> and <script>, no
    # external files) that helps a reader understand this passage.
    #
    # The page shows the result inside a sandboxed iframe about 400px
    # wide. Tell the model to answer with ONLY the HTML.
    # =========================================================
    return f"""TODO: write your instructions here.

Passage:
\"\"\"{passage}\"\"\"
"""


# Saves model replies so re-selecting the same passage doesn't spend more of
# your Lumen budget. Restarting the app clears it.
cache = {}


@app.route('/generate', methods=['POST'])
def generate():
    """Catalog mode: the model picks a component and fills in its props."""
    passage = request.json["passage"][:MAX_PASSAGE_CHARS]
    if ("catalog", passage) in cache:
        return jsonify(cache[("catalog", passage)])

    try:
        raw = call_lumen(build_catalog_prompt(passage))
    except Exception as e:
        return jsonify({"error": str(e)}), 502

    spec = extract_json(raw)

    # =========================================================
    # YOUR TASK (Part 1, step 3 of 3): Check the model's answer.
    #
    # `spec` is the parsed JSON (a dict), or None if parsing failed.
    # If spec is None, OR it has no "component" key, OR that component
    # is not in COMPONENTS, replace spec with the fallback below so the
    # reader still sees something:
    #
    #   spec = {"component": "text_card", "props": {"text": raw}}
    # =========================================================

    result = {"spec": spec, "raw": raw}
    cache[("catalog", passage)] = result
    return jsonify(result)


@app.route('/generate_html', methods=['POST'])
def generate_html():
    """Freeform mode: the model writes the whole widget as HTML."""
    passage = request.json["passage"][:MAX_PASSAGE_CHARS]
    if ("freeform", passage) in cache:
        return jsonify(cache[("freeform", passage)])

    try:
        raw = call_lumen(build_freeform_prompt(passage))
    except Exception as e:
        return jsonify({"error": str(e)}), 502

    result = {"html": extract_html(raw), "raw": raw}
    cache[("freeform", passage)] = result
    return jsonify(result)


@app.route('/pdf')
def serve_pdf():
    """Serves the raw PDF file so PDF.js can render it in the browser."""
    return send_file('sample.pdf', mimetype='application/pdf')


@app.route('/')
def home():
    return render_template('reader.html')


if __name__ == '__main__':
    # host='0.0.0.0' allows external access in Codespaces
    app.run(host='0.0.0.0', port=3000, debug=True)

# Generative Reader — Assignment

A Flask web app that shows a PDF and lets you select any passage. A language model then decides **what interface to show** for that passage, in one of two ways:

- **Catalog mode:** the model picks a component from a fixed list (definition card, step list, comparison table, ...) and fills in its data as JSON. Your code draws it.
- **Freeform mode:** the model writes the whole widget as HTML, which runs in a sandboxed iframe.

Full instructions and submission details are in the class assignment doc, **GenUI for augmenting your reading**. This README covers setup and how the code fits together.

---

## What You'll Build

All the places to edit are marked with `YOUR TASK` comments.

| Part | File | What you do |
| --- | --- | --- |
| 1 | `app.py` | Write `call_lumen()`, write the catalog prompt, and check the model's JSON |
| 2 | `static/components.js` + `app.py` | Add one new component: a renderer and its catalog entry |
| 3 | `app.py` | Write the freeform HTML prompt, then compare the two modes |

---

## Initial Setup

### 1. Open the project

**GitHub Codespaces (recommended):** on the repository page, click the green **Code** button → **Codespaces** → **Create codespace on main**. You must be logged into GitHub, and the first launch can take a minute. Dependencies are installed for you, so skip to step 2.

**Local (only if Codespaces is too slow):** clone the repo, then set up a virtual environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

You might have to use `pip3` / `python3` depending on your Python setup. On Windows, activate with `.venv\Scripts\activate`.

### 2. Get a Lumen API key

[Lumen](https://lumen.ncsa.illinois.edu) is UIUC's LLM gateway. Use your Illinois account.

1. Sign in at [lumen.ncsa.illinois.edu](https://lumen.ncsa.illinois.edu).
2. Open the **Gemma 4 31B** model page and click **Acknowledge & Enable Access** if it asks. Your API key can't use the model until you do.
3. Go to **Profile → API Keys** and create a key. It starts with `sk_`. Copy it.

### 3. Set your API key as an environment variable

**Mac / Linux / GitHub Codespaces terminal:**
```bash
export LUMEN_API_KEY="sk_paste-your-key-here"
```

**Windows (PowerShell):**
```powershell
$env:LUMEN_API_KEY="sk_paste-your-key-here"
```

You need to do this again in every new terminal.

> **GitHub Codespaces:** you can store the key as a Codespaces secret named `LUMEN_API_KEY` instead:
> Repository → Settings → Secrets and variables → Codespaces → New repository secret
>
> A secret only reaches codespaces started after you add it, so restart your codespace afterward.

### 4. Check your key and model

```bash
python example_call.py
```

This lists the models your key can use and sends one test message. If the model ID `gemma-4-31b-it` isn't in the list, copy the correct Gemma ID into `MODEL` in **both** `example_call.py` and `app.py`.

### 5. Run the app

```bash
python app.py
```

Open [http://localhost:3000](http://localhost:3000). Select a sentence in the PDF and click **Generate**. Before you start Part 1 you'll see a gray card saying `call_lumen() is not implemented yet.` That means the app is working.

**GitHub Codespaces:** the Ports tab (bottom panel) shows port 3000 with a forwarded URL. Click the globe icon to open it.

### Using your own paper

The app shows `sample.pdf` from the project root. For the assignment, replace it with the paper you picked and **keep the file name `sample.pdf`**. In Codespaces, drag the file into the Explorer sidebar to upload it.

- A short paper (or just a page or two) makes everything run faster.
- Scanned PDFs without real text won't be selectable.

Refresh the browser to see the new PDF.

---

## Seeing Your Changes

Flask runs in **debug mode**, so it restarts by itself whenever you save `app.py`. Refresh the browser after it restarts.

For changes to `templates/`, `static/components.js` or `static/components.css`, just refresh the browser. If a change to a `static/` file doesn't show up, do a hard refresh (Cmd+Shift+R / Ctrl+Shift+R).

**Debugging tips**

- Every card has a **Raw model output** section. Open it to see exactly what the model said.
- Errors from Python show up in the terminal running `app.py`.
- Errors from JavaScript show up in the browser console (right-click → Inspect → Console).
- Replies are cached per passage, so selecting the same passage again won't show a new answer after you change a prompt. Saving `app.py` clears the cache (Flask restarts), and so does restarting the app (Ctrl+C, then `python app.py`).

---

## Project Structure

```
├── app.py                 # Flask backend: Parts 1, 2 and 3
├── example_call.py        # Run first: checks your key, lists models
├── templates/
│   └── reader.html        # The reader page (no changes needed)
├── static/
│   ├── components.js      # Component renderers: Part 2
│   └── components.css     # Component styles (optional for Part 2)
├── requirements.txt
└── sample.pdf
```

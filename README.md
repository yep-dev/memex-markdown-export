# Memex to markdown export tool

Designed to be read with Obsidian, but other readers will work too

## Usage

1. Run `poetry install`
2. Customize the `output_folder` in the `main.py`
3. Run `uvicorn main:app --reload`
4. Paste the contents of `export.js` into the chrome console in the memex extension page
# Rebuild the pitch and walkthrough

The application itself has no package dependencies. The optional submission-artifact tools require Python, `reportlab`, FFmpeg via `imageio-ffmpeg`, Windows Segoe UI fonts, Windows System.Speech, and Poppler's `pdftoppm`. They were built with the Codex bundled Python runtime on Windows.

1. Run `node tools/export-sample.mjs` to regenerate `app/dist/sample.csv` and `tmp/demo-results.json` from the application engine.
2. Install `reportlab` in your Python environment. Run `python tools/build-pitch.py` to generate the pitch, narration text, and demo script.
3. Render the pitch with `pdftoppm -scale-to 1280 -png submission/NxtGen-Pitch.pdf tmp/pitch`.
4. Run `tools/narrate.ps1` in PowerShell to create seven local WAV narration tracks. The voice is the installed Windows default.
5. Install the encoder helper with `python -m pip install --target tmp/video-deps imageio-ffmpeg`.
6. Run `python tools/build-video.py`. It creates a 1280x720 MP4 with AAC narration, an embedded English subtitle track, and a separate SRT. It rejects a total runtime of three minutes or longer.

Generated temporary audio, frames, and encoder dependencies live under ignored `tmp/`. The delivered MP4 is a narrated product walkthrough of actual synthetic-data outputs. It does not claim to record interaction with the application UI.

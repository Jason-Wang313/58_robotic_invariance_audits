# Reproducibility Checklist

- Run `python v2_measurement_control.py` to regenerate the v2 CSV, JSON, and LaTeX table.
- Run `powershell -ExecutionPolicy Bypass -File build_pdf.ps1` to rebuild the canonical PDF.
- The canonical artifact is `C:/Users/wangz/Downloads/58.pdf`.
- `paper/main.pdf` is generated during compilation and removed after the canonical copy is made.
- `data/build_status.json` records the local build status and is intentionally ignored.

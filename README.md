# SOMSETU

SOMSETU is a Streamlit-based lunar image registration and XML sidecar analysis dashboard for the SETU project.

## Features
- Upload lunar image pairs and XML metadata
- Inspect mission metadata and XML sidecar details
- Run image registration workflows
- Export generated reports in PDF format

## Requirements
- Python 3.10+
- Streamlit
- OpenCV
- Pillow
- NumPy
- Pandas
- ReportLab

## Run locally
From the project folder:

```powershell
python -m streamlit run "SETU_XML_Sidecar (10).py" --server.headless true
```

Then open the local URL shown in the terminal, usually:

```text
http://localhost:8501
```

## Project files
- `SETU_XML_Sidecar (10).py` — main Streamlit application
- `requirements.txt` — Python dependencies

## Notes
This project is configured for Windows paths and works best when the app file remains in the project root.

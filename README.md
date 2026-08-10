# AI-Based Short Answer Evaluation System

A Python application that evaluates student answer images using:
- Image preprocessing
- EasyOCR
- Text cleaning
- Sentence-BERT semantic similarity
- Key-point based marking
- Automated feedback
- OCR quality checking

## Run locally

```bash
pip install -r requirements.txt
python app.py
```

Open http://localhost:10000

## Deployment

Configured for deployment on Render as a Python web service.

Build command:
`pip install -r requirements.txt`

Start command:
`gunicorn app:app`

# Semantic AI-Based Short Answer Evaluation

An AI-assisted system for evaluating handwritten or typed student answers. The system uses image preprocessing, OCR, text cleaning, semantic similarity, key-point coverage, marks calculation, and automated feedback.

## Project Pipeline

**Answer Image → Preprocessing → OCR → Text Cleaning → Semantic Matching → Marks → Feedback**

## Features

- Extracts text from answer images using EasyOCR
- Preprocesses images to improve OCR quality
- Cleans OCR-generated text
- Checks OCR quality before grading
- Compares answers with question key points using semantic similarity
- Calculates marks based on key-point coverage
- Generates feedback for the student

## Project Structure

- `main.py` — main evaluation pipeline
- `preprocessing.py` — image preprocessing
- `ocr_module.py` — OCR text extraction
- `ocr_quality_check.py` — OCR quality validation
- `text_cleaning.py` — OCR text cleaning
- `answer_matching_v2.py` — semantic/key-point matching
- `similarity_matching.py` — similarity utilities
- `marks_calculator.py` — marks calculation
- `feedback_generator.py` — feedback generation
- `question_loader.py` — question and key-point loading
- `sample_data/` — sample question/key-point data
- `sample_images/` — sample answer images

## Installation

1. Clone or download this repository.
2. Create and activate a Python virtual environment (recommended).
3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Current Pipeline

Run the main test pipeline with:

```bash
python main.py
```

The default test uses `sample_images/q1_demo.jpg` and question ID `Q1`.

## Important Note

This repository contains the current development version of the project. Model dependencies such as EasyOCR, PyTorch, and Sentence Transformers may take some time and disk space to install.

## Future Scope

- Add a web-based interface for image upload
- Deploy the application online
- Add support for multiple questions and answer sheets
- Improve OCR accuracy for different handwriting styles
- Add teacher/admin result dashboards

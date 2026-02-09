# AI Job Matcher

A simple, beginner-friendly Python tool that compares your resume with a job description and provides a compatibility score along with matched and missing skills.

## Project Overview

This tool helps job seekers quickly assess how well their resume matches a job posting. It uses simple Natural Language Processing (NLP) techniques to:

- Extract key skills and keywords from both resume and job description
- Calculate a match score using TF-IDF and cosine similarity
- Identify which skills you have that match the job requirements
- Highlight skills you're missing from the job posting

## Features

✓ **Simple and Readable Code** - Designed for beginners to understand and modify  
✓ **No Complex Dependencies** - Uses only scikit-learn and NLTK  
✓ **Fast Processing** - Analyzes documents in seconds  
✓ **Clear Output** - Easy-to-read match results with percentage score  
✓ **Example Files** - Includes sample resume and job description

## Project Structure

```
ai-job-matcher/
├── job_matcher.py              # Main Python script
├── requirements.txt             # Project dependencies
├── README.md                    # This file
├── .gitignore                   # Git ignore rules
└── data/
    ├── sample_resume.txt        # Example resume
    └── sample_job_description.txt # Example job description
```

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Step 1: Clone or Download the Project

```bash
cd ai-job-matcher
```

### Step 2: Create a Virtual Environment (Optional but Recommended)

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- **scikit-learn** - For TF-IDF vectorization and cosine similarity
- **nltk** - For stopwords and text processing

**Note:** The first time you run the script, it will automatically download the required NLTK data.

## Usage

### Quick Start with Sample Files

```bash
python job_matcher.py
```

When prompted, enter:
- Resume file path: `data/sample_resume.txt`
- Job description file path: `data/sample_job_description.txt`

### Using Your Own Files

1. Create or prepare your resume as a plain text file (`.txt`)
2. Create or prepare your job description as a plain text file (`.txt`)
3. Run the script:
   ```bash
   python job_matcher.py
   ```
4. Enter the file paths when prompted

### Example Output

```
============================================================
JOB MATCHING RESULTS
============================================================

Match Score: 72.5%
Status: GOOD MATCH ✓

Matched Skills (8):
  ✓ python
  ✓ rest
  ✓ database
  ✓ git
  ✓ docker
  ✓ agile
  ✓ apis
  ✓ development

Missing Skills (5):
  ✗ kubernetes
  ✗ azure
  ✗ nosql
  ✗ mongodb
  ✗ cicd

============================================================
```

## How It Works

### 1. **Text Preprocessing**
   - Converts text to lowercase
   - Removes punctuation
   - Removes common stopwords (the, a, an, etc.)
   - Keeps meaningful words for analysis

### 2. **Keyword Extraction**
   - Identifies the top 30 keywords from resume
   - Identifies the top 30 keywords from job description
   - Uses word frequency as the extraction metric

### 3. **Match Score Calculation**
   - Uses TF-IDF (Term Frequency-Inverse Document Frequency) vectorization
   - Calculates cosine similarity between normalized document vectors
   - Returns a score between 0 and 1 (displayed as a percentage)
   - **Score interpretation:**
     - 80%+: Excellent match
     - 60-79%: Good match
     - 40-59%: Moderate match
     - Below 40%: Weak match

### 4. **Skill Analysis**
   - **Matched Skills**: Keywords that appear in both documents
   - **Missing Skills**: Keywords from job description not in resume

## Code Structure

The main script contains a `JobMatcher` class with these key methods:

- `load_file(file_path)` - Reads a text file
- `preprocess_text(text)` - Cleans and normalizes text
- `extract_keywords(text, num_keywords)` - Extracts top keywords
- `calculate_match_score(resume_text, job_text)` - Computes similarity score
- `find_matched_skills(resume_keywords, job_keywords)` - Finds overlapping skills
- `find_missing_skills(resume_keywords, job_keywords)` - Identifies missing skills
- `match(resume_path, job_path)` - Runs the complete analysis

## Customization

You can easily modify the script for your needs:

### Change Number of Keywords Extracted
In `job_matcher.py`, modify the `num_keywords` parameter:
```python
resume_keywords = self.extract_keywords(resume_processed, num_keywords=50)  # Changed from 30
job_keywords = self.extract_keywords(job_processed, num_keywords=50)
```

### Add More Stopwords
Add domain-specific words to ignore in the `__init__` method:
```python
self.stop_words.update(['javascript', 'nodejs', 'react'])  # Add custom stopwords
```

### Change Match Score Interpretation
Modify the thresholds in the `display_results()` function:
```python
if match_pct >= 90:  # Changed from 80
    print("Status: EXCELLENT MATCH ✓")
```

## Technical Details

### Libraries Used

| Library | Purpose | Why Simple? |
|---------|---------|-----------|
| **scikit-learn** | TF-IDF, vectorization, cosine similarity | Industry standard, well-documented |
| **nltk** | Stopwords database | Lightweight, no heavy dependencies |
| **Python Standard Library** | File I/O, text processing, regex | Built-in, no external dependencies |

### Algorithm Explanation

**TF-IDF + Cosine Similarity:**
- Converts text documents into numerical vectors
- TF-IDF weighs important words higher than common words
- Cosine similarity measures the angle between vectors (0 = no similarity, 1 = identical)
- Result: A robust, proven method for document comparison

## Limitations and Future Improvements

### Current Limitations
- Simple keyword matching (doesn't understand context)
- No handling of synonyms (e.g., "Python" and "Py" treated as different)
- No consideration of required vs. nice-to-have skills
- No weight given to important skills

### Future Enhancements (for learning)
- Add synonym detection (e.g., recognize "ML" and "Machine Learning")
- Implement skill weighting (some skills more important than others)
- Add ability to mark certain skills as required vs. optional
- Create a GUI version using tkinter

## Troubleshooting

### "Microsoft Visual C++ 14.0 or greater is required" (Windows)
**Issue:** This error occurs when scikit-learn tries to compile C code on Windows without the necessary build tools.

**Solution Options:**
1. **Quick Fix (Recommended):** Install from a pre-built wheel:
   ```bash
   pip install scikit-learn --only-binary :all:
   pip install nltk
   ```

2. **Alternative:** Create a virtual environment (ensures clean installation):
   ```bash
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **For Permanent Solution:** Download and install [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)

### "ModuleNotFoundError: No module named 'sklearn'"
**Solution:** Install dependencies with `pip install -r requirements.txt`

### "No such file or directory"
**Solution:** Use absolute paths or ensure files are in the `data/` folder. Example:
```
c:\Users\username\Wind-Tempo\ai-job-matcher\data\sample_resume.txt
```

### "LookupError" for stopwords
**Solution:** The script auto-downloads required NLTK data on first run. Ensure internet connection is available.

## Git Workflow

### Initialize Git Repository
```bash
cd ai-job-matcher
git init
git add .
git commit -m "Initial commit: Basic job matcher project structure"
```

### Make Changes and Commit
```bash
# Make your changes
git add job_matcher.py
git commit -m "Improve keyword extraction algorithm"

# Push to GitHub
git remote add origin https://github.com/yourusername/ai-job-matcher.git
git branch -M main
git push -u origin main
```

## Learning Resources

To understand the concepts used in this project:

- **TF-IDF Concept:** https://en.wikipedia.org/wiki/Tf%E2%80%93idf
- **Cosine Similarity:** https://en.wikipedia.org/wiki/Cosine_similarity
- **NLTK Stopwords:** https://www.nltk.org/
- **scikit-learn Documentation:** https://scikit-learn.org/

## License

This project is open source and available for educational and personal use.

## Author

Created as a beginner-friendly project for learning Python and NLP concepts.

## Questions or Issues?

If you encounter any issues or have suggestions for improvement, feel free to:
1. Check the Troubleshooting section
2. Review the code comments
3. Modify and experiment with the code!

---

**Happy Job Hunting! 🚀**

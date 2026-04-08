from flask import Flask, render_template, request
from job_matcher import JobMatcher

app = Flask(__name__)
matcher = JobMatcher()

@app.route('/', methods=['GET', 'POST'])
def index():
    results = None
    error = None
    resume_text = ''
    job_text = ''

    if request.method == 'POST':
        resume_text = request.form.get('resume_text', '').strip()
        job_text = request.form.get('job_text', '').strip()

        resume_file = request.files.get('resume_file')
        job_file = request.files.get('job_file')

        if resume_file and resume_file.filename:
            resume_text = resume_file.read().decode('utf-8', errors='ignore')

        if job_file and job_file.filename:
            job_text = job_file.read().decode('utf-8', errors='ignore')

        if not resume_text or not job_text:
            error = 'Please provide both resume and job description text or upload both files.'
        else:
            results = matcher.match_texts(resume_text, job_text)

    return render_template(
        'index.html',
        results=results,
        error=error,
        resume_text=resume_text,
        job_text=job_text,
    )

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)

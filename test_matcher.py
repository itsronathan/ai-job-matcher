"""
Simple test script to verify the job matcher works correctly.
This runs the matcher with predefined file paths.
"""

from job_matcher import JobMatcher, display_results

# Test the job matcher with sample files
matcher = JobMatcher()
print("Testing Job Matcher with sample files...\n")

# use class directly
results = matcher.match('data/sample_resume.txt', 'data/sample_job_description.txt')
display_results(results)

# invocation via main() with arguments
print("\nTesting CLI argument support...")
import sys
_backup = sys.argv
sys.argv = ['job_matcher.py', 'data/sample_resume.txt', 'data/sample_job_description.txt']
from job_matcher import main
main()
sys.argv = _backup

# Print additional debug info
if results:
    print("\nDebug Information:")
    print(f"Resume Keywords: {results['resume_keywords'][:10]}...")
    print(f"Job Keywords: {results['job_keywords'][:10]}...")
    print(f"Match Score (raw): {results['match_score']:.4f}")

# extra checks: synonyms / fuzzy
print("\nRunning a quick synonym/fuzzy check...")
from tempfile import NamedTemporaryFile
with NamedTemporaryFile('w+', delete=False) as rfile, NamedTemporaryFile('w+', delete=False) as jfile:
    rfile.write("experience with aws and docker containers")
    jfile.write("looking for amazon web services engineer familiar with docker")
    rfile.flush(); jfile.flush()
    syn_res = matcher.match(rfile.name, jfile.name)
    display_results(syn_res)
    print(f"Matched skills in synonym test: {syn_res['matched_skills']}")

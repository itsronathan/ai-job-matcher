"""
Simple test script to verify the job matcher works correctly.
This runs the matcher with predefined file paths.
"""

from job_matcher import JobMatcher, display_results

# Test the job matcher with sample files
matcher = JobMatcher()
print("Testing Job Matcher with sample files...\n")

results = matcher.match('data/sample_resume.txt', 'data/sample_job_description.txt')
display_results(results)

# Print additional debug info
if results:
    print("\nDebug Information:")
    print(f"Resume Keywords: {results['resume_keywords'][:10]}...")
    print(f"Job Keywords: {results['job_keywords'][:10]}...")
    print(f"Match Score (raw): {results['match_score']:.4f}")

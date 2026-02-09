"""
AI Job Matcher - Simple Resume to Job Description Matcher

This script compares a resume against a job description and calculates
a compatibility score along with matched and missing skills.
"""

import re
import string
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords

# Download required NLTK data (run once)
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    print("Downloading NLTK stopwords data...")
    nltk.download('stopwords')


class JobMatcher:
    """
    A simple job matcher that compares a resume with a job description.
    
    This class handles:
    - Loading and preprocessing text files
    - Extracting keywords and skills
    - Calculating match scores
    - Identifying matched and missing skills
    """
    
    def __init__(self):
        """Initialize the job matcher with common stopwords."""
        self.stop_words = set(stopwords.words('english'))
        # Add domain-specific words to ignore
        self.stop_words.update(['job', 'role', 'position', 'company', 'team', 'work'])
    
    def load_file(self, file_path):
        """
        Load text from a file.
        
        Args:
            file_path (str): Path to the text file
            
        Returns:
            str: Content of the file, or empty string if file not found
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
            return ""
    
    def preprocess_text(self, text):
        """
        Preprocess text by lowercasing, removing punctuation and stopwords.
        
        Args:
            text (str): Raw text to preprocess
            
        Returns:
            str: Cleaned text
        """
        # Convert to lowercase
        text = text.lower()
        
        # Remove punctuation
        text = text.translate(str.maketrans('', '', string.punctuation))
        
        # Split into words and remove stopwords
        words = text.split()
        words = [word for word in words if word not in self.stop_words and len(word) > 2]
        
        # Join words back together
        return ' '.join(words)
    
    def extract_keywords(self, text, num_keywords=20):
        """
        Extract top keywords from text using TF-IDF.
        
        Args:
            text (str): Preprocessed text
            num_keywords (int): Number of top keywords to extract
            
        Returns:
            list: Top keywords/skills
        """
        # Split into words
        words = text.split()
        
        # Count word frequency
        word_freq = {}
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        # Sort by frequency and return top keywords
        sorted_keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return [keyword for keyword, freq in sorted_keywords[:num_keywords]]
    
    def calculate_match_score(self, resume_text, job_text):
        """
        Calculate similarity score between resume and job description using TF-IDF.
        
        Args:
            resume_text (str): Preprocessed resume text
            job_text (str): Preprocessed job description text
            
        Returns:
            float: Similarity score between 0 and 1
        """
        # Create TF-IDF vectorizer
        vectorizer = TfidfVectorizer(stop_words='english', max_features=100)
        
        # Fit and transform both texts
        try:
            tfidf_matrix = vectorizer.fit_transform([resume_text, job_text])
            
            # Calculate cosine similarity
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            return similarity
        except ValueError:
            # Handle case where texts are too short or empty
            return 0.0
    
    def find_matched_skills(self, resume_keywords, job_keywords):
        """
        Find the intersection of keywords between resume and job description.
        
        Args:
            resume_keywords (list): Keywords from resume
            job_keywords (list): Keywords from job description
            
        Returns:
            list: Skills that appear in both
        """
        resume_set = set(resume_keywords)
        job_set = set(job_keywords)
        return list(resume_set.intersection(job_set))
    
    def find_missing_skills(self, resume_keywords, job_keywords):
        """
        Find skills from job description that are missing in resume.
        
        Args:
            resume_keywords (list): Keywords from resume
            job_keywords (list): Keywords from job description
            
        Returns:
            list: Skills required but not in resume
        """
        resume_set = set(resume_keywords)
        job_set = set(job_keywords)
        return list(job_set - resume_set)
    
    def match(self, resume_path, job_path):
        """
        Perform full job matching analysis.
        
        Args:
            resume_path (str): Path to resume text file
            job_path (str): Path to job description text file
            
        Returns:
            dict: Results including match score, matched skills, and missing skills
        """
        # Load files
        resume_text = self.load_file(resume_path)
        job_text = self.load_file(job_path)
        
        if not resume_text or not job_text:
            return None
        
        # Preprocess texts
        resume_processed = self.preprocess_text(resume_text)
        job_processed = self.preprocess_text(job_text)
        
        # Extract keywords
        resume_keywords = self.extract_keywords(resume_processed, num_keywords=30)
        job_keywords = self.extract_keywords(job_processed, num_keywords=30)
        
        # Calculate match score
        match_score = self.calculate_match_score(resume_processed, job_processed)
        
        # Find matched and missing skills
        matched_skills = self.find_matched_skills(resume_keywords, job_keywords)
        missing_skills = self.find_missing_skills(resume_keywords, job_keywords)
        
        return {
            'match_score': match_score,
            'match_percentage': match_score * 100,
            'matched_skills': matched_skills,
            'missing_skills': missing_skills,
            'resume_keywords': resume_keywords,
            'job_keywords': job_keywords
        }


def display_results(results):
    """
    Display job matching results in a formatted way.
    
    Args:
        results (dict): Results from the match() method
    """
    if results is None:
        print("Error: Could not process files.")
        return
    
    print("\n" + "="*60)
    print("JOB MATCHING RESULTS")
    print("="*60)
    
    # Display match score
    match_pct = results['match_percentage']
    print(f"\nMatch Score: {match_pct:.1f}%")
    
    # Display interpretation
    if match_pct >= 80:
        print("Status: EXCELLENT MATCH ✓")
    elif match_pct >= 60:
        print("Status: GOOD MATCH ✓")
    elif match_pct >= 40:
        print("Status: MODERATE MATCH")
    else:
        print("Status: WEAK MATCH")
    
    # Display matched skills
    print(f"\nMatched Skills ({len(results['matched_skills'])}):")
    if results['matched_skills']:
        for skill in sorted(results['matched_skills']):
            print(f"  ✓ {skill}")
    else:
        print("  (No overlapping skills found)")
    
    # Display missing skills
    print(f"\nMissing Skills ({len(results['missing_skills'])}):")
    if results['missing_skills']:
        for skill in sorted(results['missing_skills'])[:10]:  # Show top 10
            print(f"  ✗ {skill}")
        if len(results['missing_skills']) > 10:
            print(f"  ... and {len(results['missing_skills']) - 10} more")
    else:
        print("  (All job skills are present in resume)")
    
    print("\n" + "="*60)


def main():
    """Main function to run the job matcher."""
    print("Welcome to AI Job Matcher!")
    print("This tool compares your resume with a job description.\n")
    
    # Get file paths from user
    resume_path = input("Enter the path to your resume file: ").strip()
    job_path = input("Enter the path to the job description file: ").strip()
    
    # Create matcher and run analysis
    matcher = JobMatcher()
    results = matcher.match(resume_path, job_path)
    
    # Display results
    display_results(results)


if __name__ == "__main__":
    main()

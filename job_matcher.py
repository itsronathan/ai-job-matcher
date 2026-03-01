"""
AI Job Matcher - Simple Resume to Job Description Matcher

This script compares a resume against a job description and calculates
a compatibility score along with matched and missing skills.
"""

import re
import string
from pathlib import Path
from difflib import SequenceMatcher
import sys

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer

# Download required NLTK data (run once)
for pkg in ('stopwords', 'wordnet', 'omw-1.4'):
    try:
        nltk.data.find(f'corpora/{pkg}')
    except LookupError:
        print(f"Downloading NLTK {pkg} data...")
        nltk.download(pkg)


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
        """Initialize the job matcher with common stopwords and NLP helpers."""
        self.stop_words = set(stopwords.words('english'))
        # Add domain-specific words to ignore
        self.stop_words.update(['job', 'role', 'position', 'company', 'team', 'work'])
        # generic terms commonly found in descriptions but not skills
        self.stop_words.update([
            'currently', 'requires', 'require', 'ability', 'minimum', 'complete',
            'pursuing', 'student', 'intern', 'internship', 'experience', 'apply',
            'match', 'detail'
        ])

        # lemmatizer for reducing words to base form
        self.lemmatizer = WordNetLemmatizer()

        # fuzzy match threshold for approximate matches
        self.fuzzy_threshold = 0.8

        # manual alias map to normalize common skill synonyms (domain-specific)
        self.skill_aliases = {
            'amazon web services': 'aws',
            'amazon': 'aws',
            'gcp': 'google cloud',
            'google cloud platform': 'google cloud',
            'sql': 'sql',
            'structured query language': 'sql',
            'db': 'database',
            'docker container': 'docker',
            # education/field equivalences
            'computer science': 'engineering',
            'bachelors': 'engineering',
            'b.s.': 'engineering',
            'bs': 'engineering'
        }
    
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

        # Split into words
        words = text.split()

        # Remove stopwords and very short tokens
        words = [word for word in words if word not in self.stop_words and len(word) > 2]

        # Lemmatize each word to its base form
        words = [self.lemmatizer.lemmatize(word) for word in words]

        # Join words back together
        return ' '.join(words)
    
    def extract_keywords(self, text, num_keywords=20):
        """
        Extract top keywords from text using TF-IDF vectorization.
        n‑grams are included to capture multi-word skills like "rest api".
        
        Args:
            text (str): Preprocessed text
            num_keywords (int): Number of top keywords to extract
            
        Returns:
            list: Top keywords/skills
        """
        # sklearn expects a list (or "english").
        stop_list = list(self.stop_words)
        vectorizer = TfidfVectorizer(
            stop_words=stop_list,
            ngram_range=(1, 2),
            max_features=1000
        )
        tfidf = vectorizer.fit_transform([text])

        # get feature names and sort by score
        features = np.array(vectorizer.get_feature_names_out())
        scores = tfidf.toarray().flatten()
        if scores.size == 0:
            return []
        ranked_indices = np.argsort(scores)[::-1]
        top_features = features[ranked_indices][:num_keywords]
        return top_features.tolist()
    
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
    
    def get_synonyms(self, word):
        """Return a set of synonyms (WordNet) for a word."""
        syns = set()
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                syns.add(lemma.name().replace('_', ' '))
        return syns

    def fuzzy_match(self, a, b):
        """Return True if two strings are similar above the fuzzy threshold."""
        return SequenceMatcher(None, a, b).ratio() >= self.fuzzy_threshold

    def find_matched_skills(self, resume_keywords, job_keywords):
        """
        Find matched skills between resume and job description.
        This method considers direct matches, synonyms, and fuzzy similarities.
        """
        matched = []
        resume_set = set(resume_keywords)
        for jk in job_keywords:
            if jk in resume_set:
                matched.append(jk)
                continue
            # check synonyms of job keyword
            for syn in self.get_synonyms(jk):
                if syn in resume_set:
                    matched.append(jk)
                    break
            else:
                # fuzzy compare against each resume keyword
                for rk in resume_set:
                    if self.fuzzy_match(jk, rk):
                        matched.append(jk)
                        break
        return matched
    
    def find_missing_skills(self, resume_keywords, job_keywords):
        """
        Identify job skills that were not matched (after synonyms/fuzzy).
        """
        matched = set(self.find_matched_skills(resume_keywords, job_keywords))
        return [jk for jk in job_keywords if jk not in matched]
    
    def extract_qualification_section(self, text):
        """Return text from the most relevant qualifications/requirements section.

        The algorithm scans for a heading using a prioritized list: we want the "Minimum
        Knowledge" block if present, otherwise fall back to "Required Qualifications",
        "Qualifications", then "Key Attributes". Once the start is located it grabs all
        following non-blank lines until the next heading or an empty line after content.
        """
        lines = text.splitlines()
        priority = ['minimum knowledge', 'required qualifications',
                    'required skills', 'qualifications', 'key attributes']

        start_idx = None
        for pat in priority:
            for i, line in enumerate(lines):
                if line.strip().lower().startswith(pat):
                    # begin after this heading line
                    start_idx = i + 1
                    break
            if start_idx is not None:
                break

        if start_idx is None:
            return ''

        section_lines = []
        for line in lines[start_idx:]:
            lower = line.strip().lower()
            if lower == '':
                # stop if we've already collected some content
                if section_lines:
                    break
                else:
                    continue
            if any(lower.startswith(pat) for pat in priority):
                break
            section_lines.append(line)

        return ' '.join(section_lines)

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

        # if a qualifications section exists, only use that text for keyword extraction
        qual_section = self.extract_qualification_section(job_text)
        if qual_section:
            job_for_keywords = self.preprocess_text(qual_section)
        else:
            job_for_keywords = job_processed

        # Extract keywords
        resume_keywords = self.extract_keywords(resume_processed, num_keywords=30)
        job_keywords = self.extract_keywords(job_for_keywords, num_keywords=30)

        # normalize skill aliases (e.g. "amazon web services" -> "aws")
        resume_keywords = [self.skill_aliases.get(k, k) for k in resume_keywords]
        job_keywords = [self.skill_aliases.get(k, k) for k in job_keywords]
        
        # Calculate match score
        match_score = self.calculate_match_score(resume_processed, job_processed)
        
        # Find matched and missing skills
        matched_skills = self.find_matched_skills(resume_keywords, job_keywords)
        missing_skills = self.find_missing_skills(resume_keywords, job_keywords)
        
        total_quals = len(job_keywords)
        matched_count = len(matched_skills)
        qual_pct = (matched_count / total_quals * 100) if total_quals > 0 else 0.0

        return {
            'match_score': match_score,
            'match_percentage': match_score * 100,
            'qualified_matches': matched_count,
            'total_qualifications': total_quals,
            'qualification_match_percentage': qual_pct,
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
    
    # Display overall similarity score
    match_pct = results['match_percentage']
    print(f"\nMatch Score: {match_pct:.1f}%")
    # display interpretation
    if match_pct >= 80:
        print("Status: EXCELLENT MATCH [✔]")
    elif match_pct >= 60:
        print("Status: GOOD MATCH [✔]")
    elif match_pct >= 40:
        print("Status: MODERATE MATCH")
    else:
        print("Status: WEAK MATCH")

    # show qualification-specific statistics (if any)
    if 'total_qualifications' in results:
        tq = results['total_qualifications']
        if tq > 0:
            qm = results.get('qualified_matches', 0)
            qpct = results.get('qualification_match_percentage', 0.0)
            print(f"\nQualifications Matched: {qm} / {tq} ({qpct:.1f}%)")
    
    # Display matched skills
    print(f"\nMatched Skills ({len(results['matched_skills'])}):")
    if results['matched_skills']:
        for skill in sorted(results['matched_skills']):
            print(f"  * {skill}")
    else:
        print("  (No overlapping skills found)")
    
    # Display missing skills
    print(f"\nMissing Skills ({len(results['missing_skills'])}):")
    if results['missing_skills']:
        for skill in sorted(results['missing_skills'])[:10]:  # Show top 10
            print(f"  - {skill}")
        if len(results['missing_skills']) > 10:
            print(f"  ... and {len(results['missing_skills']) - 10} more")
    else:
        print("  (All job skills are present in resume)")
    
    print("\n" + "="*60)


def main():
    """Main function to run the job matcher.

    Accepts optional command-line arguments so it can be used in scripts or pipes.

    Usage:
        python job_matcher.py resume.txt job.txt
    """
    print("Welcome to AI Job Matcher!")
    print("This tool compares your resume with a job description.\n")

    # command-line override
    if len(sys.argv) >= 3:
        resume_path = sys.argv[1]
        job_path = sys.argv[2]
    else:
        resume_path = input("Enter the path to your resume file: ").strip()
        job_path = input("Enter the path to the job description file: ").strip()

    # Create matcher and run analysis
    matcher = JobMatcher()
    results = matcher.match(resume_path, job_path)

    # Display results
    display_results(results)


if __name__ == "__main__":
    main()

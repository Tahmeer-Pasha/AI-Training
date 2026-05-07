"""
Resume Shortlisting Engine

This module implements an intelligent resume screening system that evaluates
candidates against job descriptions using multiple NLP techniques:

1. Skill Extraction: Identifies technical and soft skills from text
2. Keyword Matching: Uses TF-IDF for term overlap analysis  
3. Semantic Similarity: Leverages sentence transformers for meaning-based matching
4. Hybrid Scoring: Combines multiple signals for robust evaluation

The system outputs structured CSV reports suitable for HR workflows.

Author: [Your Name]
Date: 2024
"""

from __future__ import annotations

import csv
import re
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Set, Optional, Any

from constants import CSV_FIELDNAMES, DEFAULT_SKILL_KEYWORDS, STOP_WORDS
from retrieval.vector_store import VectorStore
from utils import load_text, extract_candidate_name, normalize_text, filter_meaningful_terms


def normalize_text(text: str) -> List[str]:
    """
    Extract alphanumeric tokens from text for analysis.
    
    Args:
        text: Input text to normalize
        
    Returns:
        List of normalized tokens (lowercase, alphanumeric + common symbols)
    """
    return re.findall(r"[A-Za-z0-9#+\-.]+", text.lower())


def compact_text(text: str) -> str:
    """
    Remove extra whitespace and normalize text formatting.
    
    Args:
        text: Input text to compact
        
    Returns:
        Cleaned text with normalized spacing
    """
    return re.sub(r"\s+", " ", text).strip()


def extract_candidate_name(resume_text: str, source_file: Optional[Path] = None) -> str:
    """
    Extract candidate name from resume text, typically from the first line.
    
    Args:
        resume_text: Full resume content
        source_file: Source file path as fallback
        
    Returns:
        Extracted candidate name or filename if extraction fails
    """
    lines = [line.strip() for line in resume_text.splitlines() if line.strip()]
    
    if lines:
        # Assume first non-empty line contains the name
        candidate_line = lines[0]
        # Validate it looks like a name (1-5 words)
        if 1 <= len(candidate_line.split()) <= 5:
            return candidate_line
    
    # Fallback to filename without extension
    return source_file.stem if source_file is not None else "Unknown Candidate"


def filter_meaningful_terms(words: List[str]) -> Set[str]:
    """
    Filter out stop words and short terms to focus on meaningful content.
    
    Args:
        words: List of words to filter
        
    Returns:
        Set of meaningful terms
    """
    return {
        word for word in words 
        if len(word) > 1 and word.lower() not in STOP_WORDS
    }


def extract_skills_from_text(text: str, additional_keywords: Optional[List[str]] = None) -> List[str]:
    """
    Extract technical and professional skills from text using keyword matching.
    
    This function searches for predefined skill keywords and any additional
    keywords provided. It uses longest-match-first to avoid partial matches.
    
    Args:
        text: Text to analyze for skills
        additional_keywords: Extra keywords to search for
        
    Returns:
        List of found skills in order of discovery
    """
    # Combine default skills with any additional ones
    all_keywords = set(DEFAULT_SKILL_KEYWORDS)
    if additional_keywords:
        all_keywords.update(keyword.lower() for keyword in additional_keywords)
    
    text_lower = text.lower()
    found_skills = []
    
    # Sort by length (longest first) to prioritize specific terms
    # e.g., "machine learning" before "machine" or "learning"
    for keyword in sorted(all_keywords, key=len, reverse=True):
        if keyword in text_lower and keyword not in found_skills:
            found_skills.append(keyword)
    
    return found_skills


def build_term_set(text: str) -> Set[str]:
    """
    Build a set of meaningful terms from text for overlap analysis.
    
    Args:
        text: Input text to process
        
    Returns:
        Set of filtered, normalized terms
    """
    tokens = normalize_text(text)
    return {
        token for token in tokens 
        if token not in STOP_WORDS and len(token) > 2
    }


@dataclass
class CandidateEvaluation:
    """
    Structured representation of a candidate's evaluation results.
    
    This class encapsulates all the information needed to make a hiring
    decision and provides methods for serialization to CSV format.
    """
    candidate_name: str
    resume_path: str
    decision: str  # "SHORTLIST" or "REJECT"
    overall_score: float
    matched_skills: str
    required_skills: str
    evaluation_summary: str
    
    def to_csv_row(self) -> Dict[str, str]:
        """
        Convert evaluation to CSV row format.
        
        Returns:
            Dictionary suitable for CSV writer
        """
        return {
            "candidate_name": self.candidate_name,
            "source_file": self.resume_path,
            "status": self.decision,
            "score": f"{self.overall_score:.3f}",
            "matched_skills": self.matched_skills,
            "required_skills": self.required_skills,
            "summary": self.evaluation_summary,
        }


class ResumeShortlistingAgent:
    """
    Intelligent resume screening and candidate shortlisting system.
    
    This agent combines multiple NLP techniques to evaluate resumes:
    - Skill extraction and matching
    - Term overlap analysis using TF-IDF concepts
    - Semantic similarity using vector embeddings
    - Configurable scoring thresholds
    
    The system is designed for HR professionals who need to efficiently
    screen large numbers of candidates against specific job requirements.
    """
    
    def __init__(self, 
                 score_threshold: float = 0.6, 
                 min_skills_required: int = 2,
                 embedding_model: str = "all-MiniLM-L6-v2"):
        """
        Initialize the shortlisting agent with configurable parameters.
        
        Args:
            score_threshold: Minimum score for shortlisting (0.0-1.0)
            min_skills_required: Minimum matched skills for automatic shortlisting
            embedding_model: Sentence transformer model for semantic similarity
        """
        self.score_threshold = score_threshold
        self.min_skills_required = min_skills_required
        
        # Initialize vector store for semantic similarity
        self.vector_store = VectorStore()
        
        print(f"Initialized shortlisting agent:")
        print(f"  Score threshold: {score_threshold}")
        print(f"  Min skills required: {min_skills_required}")
        print(f"  Embedding model: {embedding_model}")
    
    def evaluate_candidate(self, 
                          resume_text: str, 
                          job_description: str, 
                          resume_file: Optional[Path] = None) -> CandidateEvaluation:
        """
        Comprehensive evaluation of a single candidate against job requirements.
        
        This method implements a multi-factor scoring algorithm:
        1. Skill matching (40% weight)
        2. Term overlap analysis (30% weight)  
        3. Semantic similarity (30% weight)
        
        Args:
            resume_text: Full text content of the resume
            job_description: Job requirements and description
            resume_file: Source file path for reference
            
        Returns:
            CandidateEvaluation with detailed scoring and decision
        """
        # Extract basic candidate information
        file_path = str(resume_file) if resume_file else "sample_resume"
        candidate_name = extract_candidate_name(resume_text, resume_file)
        
        # 1. SKILL ANALYSIS
        # Extract skills from both job description and resume
        required_skills = extract_skills_from_text(job_description)
        candidate_skills = extract_skills_from_text(resume_text)
        
        # Find intersection of skills
        matched_skills = sorted(set(required_skills) & set(candidate_skills))
        skill_match_ratio = len(matched_skills) / max(1, len(required_skills))
        
        # 2. TERM OVERLAP ANALYSIS
        # Build term sets for keyword-based matching
        job_terms = build_term_set(job_description)
        resume_terms = build_term_set(resume_text)
        
        # Calculate overlap ratio (similar to TF-IDF concept)
        common_terms = job_terms & resume_terms
        term_overlap_ratio = len(common_terms) / max(1, len(job_terms))
        
        # 3. SEMANTIC SIMILARITY
        # Use vector embeddings for meaning-based matching
        semantic_score = self._calculate_semantic_similarity(resume_text, job_description)
        
        # 4. HYBRID SCORING
        # Combine all factors with weighted importance
        overall_score = (
            0.4 * skill_match_ratio +      # Skills are most important
            0.3 * term_overlap_ratio +     # Keyword matching
            0.3 * semantic_score           # Semantic understanding
        )
        
        # 5. DECISION LOGIC
        # Shortlist if score meets threshold OR has minimum required skills
        should_shortlist = (
            overall_score >= self.score_threshold or 
            len(matched_skills) >= self.min_skills_required
        )
        decision = "SHORTLIST" if should_shortlist else "REJECT"
        
        # 6. GENERATE SUMMARY
        summary = self._generate_evaluation_summary(
            len(matched_skills), len(required_skills),
            term_overlap_ratio, semantic_score, overall_score
        )
        
        return CandidateEvaluation(
            candidate_name=candidate_name,
            resume_path=file_path,
            decision=decision,
            overall_score=overall_score,
            matched_skills=", ".join(matched_skills) if matched_skills else "None",
            required_skills=", ".join(sorted(required_skills)) if required_skills else "None",
            evaluation_summary=compact_text(summary)
        )
    
    def _calculate_semantic_similarity(self, resume_text: str, job_description: str) -> float:
        """
        Calculate semantic similarity between resume and job description.
        
        Args:
            resume_text: Resume content
            job_description: Job requirements
            
        Returns:
            Similarity score between 0.0 and 1.0
        """
        try:
            # Add documents to vector store
            documents = [resume_text, job_description]
            metadatas = [{"type": "resume"}, {"type": "job"}]
            
            self.vector_store.add_documents(documents, metadatas)
            
            # Query resume content against job description
            results = self.vector_store.query(job_description, n_results=1)
            
            if results and "distances" in results and results["distances"]:
                # Convert distance to similarity (ChromaDB uses cosine distance)
                distance = results["distances"][0][0]
                similarity = 1.0 - distance  # Convert distance to similarity
                return max(0.0, min(1.0, similarity))  # Clamp to [0,1]
            
        except Exception as e:
            print(f"Warning: Semantic similarity calculation failed: {e}")
        
        return 0.0  # Fallback if similarity calculation fails
    
    def _generate_evaluation_summary(self, 
                                   matched_count: int, 
                                   required_count: int,
                                   term_overlap: float, 
                                   semantic_score: float,
                                   overall_score: float) -> str:
        """
        Generate human-readable evaluation summary.
        
        Args:
            matched_count: Number of matched skills
            required_count: Total required skills
            term_overlap: Term overlap ratio
            semantic_score: Semantic similarity score
            overall_score: Final combined score
            
        Returns:
            Formatted summary string
        """
        return (
            f"Skills: {matched_count}/{required_count} matched. "
            f"Keyword overlap: {term_overlap:.1%}. "
            f"Semantic match: {semantic_score:.1%}. "
            f"Overall score: {overall_score:.3f}"
        )
    
    def run(self, resume_inputs: List[Dict[str, Any]], job_description: str) -> List[Dict[str, str]]:
        """
        Process multiple resumes and return evaluation results.
        
        Args:
            resume_inputs: List of dicts with 'text' and 'path' keys
            job_description: Job requirements text
            
        Returns:
            List of evaluation results as CSV-ready dictionaries
        """
        results = []
        
        print(f"Processing {len(resume_inputs)} resume(s)...")
        
        for i, resume_data in enumerate(resume_inputs, 1):
            resume_text = resume_data["text"]
            resume_path = resume_data.get("path")
            
            # Convert path to Path object if it's a string
            if isinstance(resume_path, str):
                resume_path = Path(resume_path)
            
            print(f"  [{i}/{len(resume_inputs)}] Evaluating: {resume_path.name if resume_path else 'sample'}")
            
            # Evaluate candidate
            evaluation = self.evaluate_candidate(resume_text, job_description, resume_path)
            results.append(evaluation.to_csv_row())
        
        return results
    
    def write_csv(self, results: List[Dict[str, str]], output_path: Path, append: bool = False) -> None:
        """
        Write evaluation results to CSV file.
        
        Args:
            results: List of evaluation result dictionaries
            output_path: Path for output CSV file
            append: Whether to append to existing file
        """
        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Determine write mode
        mode = "a" if append and output_path.exists() else "w"
        
        with output_path.open(mode, newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=CSV_FIELDNAMES)
            
            # Write header only for new files or when not appending
            if mode == "w":
                writer.writeheader()
            
            # Write all results
            for result in results:
                writer.writerow(result)
        
        print(f"Results written to: {output_path}")
    
    def process_folder(self, 
                      resumes_folder: Path, 
                      job_description_path: Path, 
                      output_csv: Path) -> List[Dict[str, str]]:
        """
        Process all resume files in a folder and generate shortlist.
        
        This method is optimized for large batches of resumes, processing
        them incrementally and writing results as they're completed.
        
        Args:
            resumes_folder: Directory containing resume files
            job_description_path: Path to job description file
            output_csv: Output CSV file path
            
        Returns:
            List of all evaluation results
        """
        print(f"Processing resume folder: {resumes_folder}")
        
        # Load job description once
        job_description = load_text(job_description_path)
        
        # Find all supported resume files
        resume_files = []
        for pattern in ["*.pdf", "*.txt", "*.docx"]:
            resume_files.extend(resumes_folder.glob(pattern))
        
        resume_files.sort()  # Process in consistent order
        
        if not resume_files:
            print(f"No resume files found in {resumes_folder}")
            return []
        
        print(f"Found {len(resume_files)} resume file(s)")
        
        all_results = []
        
        # Process each resume individually for memory efficiency
        for i, resume_path in enumerate(resume_files, 1):
            print(f"[{i}/{len(resume_files)}] Processing: {resume_path.name}")
            
            try:
                # Load and evaluate resume
                resume_text = load_text(resume_path)
                evaluation = self.evaluate_candidate(resume_text, job_description, resume_path)
                result = evaluation.to_csv_row()
                
                all_results.append(result)
                
                # Write result immediately (append mode after first)
                self.write_csv([result], output_csv, append=(i > 1))
                
                # Print quick status
                status = evaluation.decision
                score = evaluation.overall_score
                print(f"    -> {status} (Score: {score:.3f})")
                
            except Exception as e:
                print(f"    -> ERROR: Failed to process {resume_path.name}: {e}")
                # Continue with other files
                continue
        
        return all_results
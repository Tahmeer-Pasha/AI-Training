"""
Resume Shortlisting System

An intelligent resume screening and candidate shortlisting tool that uses
advanced NLP techniques to evaluate resumes against job descriptions.

This package provides automated candidate evaluation using:
- TF-IDF for keyword matching
- Semantic similarity using sentence transformers
- Hybrid scoring algorithms
- Structured CSV output for HR workflows

Author: [Your Name]
Version: 1.0.0
"""

from .shortlisting import ResumeShortlistingAgent
from .constants import DEFAULT_SKILL_KEYWORDS, STOP_WORDS, CSV_FIELDNAMES

__version__ = "1.0.0"
__author__ = "[Your Name]"
__email__ = "[your.email@example.com]"

__all__ = [
    "ResumeShortlistingAgent",
    "DEFAULT_SKILL_KEYWORDS", 
    "STOP_WORDS", 
    "CSV_FIELDNAMES"
]
#!/usr/bin/env python3
"""
Resume Shortlisting System

Entry point for the automated resume screening and candidate shortlisting tool.
This system helps HR professionals and recruiters efficiently evaluate large
numbers of resumes against job requirements using NLP techniques.

Usage:
    python main.py --job job_description.txt --resumes-folder ./candidates/
    python main.py --use-sample

For more options, run: python main.py --help
"""

from cli import main

if __name__ == "__main__":
    main()
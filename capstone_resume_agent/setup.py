"""
Setup configuration for Resume Shortlisting System

This setup script allows the package to be installed as a proper Python package
with all dependencies and entry points configured correctly.

Author: [Your Name]
Date: 2024
"""

from setuptools import setup, find_packages
import os

# Get the directory of this setup.py file
here = os.path.abspath(os.path.dirname(__file__))

# Read the README file for long description
with open(os.path.join(here, "README.md"), "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements from requirements.txt
with open(os.path.join(here, "requirements.txt"), "r", encoding="utf-8") as fh:
    requirements = [
        line.strip() 
        for line in fh 
        if line.strip() and not line.startswith("#")
    ]

setup(
    name="resume-shortlisting-system",
    version="1.0.0",
    author="[Your Name]",
    author_email="[your.email@example.com]",
    description="Intelligent resume screening and candidate shortlisting using NLP",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/resume-shortlisting-system",
    
    # Package configuration
    py_modules=[
        "shortlisting", 
        "cli", 
        "utils", 
        "constants"
    ],
    packages=find_packages(include=["retrieval", "retrieval.*"]),
    
    # Dependencies
    install_requires=requirements,
    
    # Python version requirement
    python_requires=">=3.11",
    
    # Entry points for command-line usage
    entry_points={
        "console_scripts": [
            "resume-shortlist=cli:main",
        ],
    },
    
    # Package data (include sample files)
    include_package_data=True,
    package_data={
        "": ["data/*", "input/*", "tests/*"],
    },
    
    # Classification metadata
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Office/Business :: Human Resources",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Text Processing :: Linguistic",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Natural Language :: English",
    ],
    
    # Keywords for discovery
    keywords=[
        "resume", "screening", "shortlisting", "hr", "recruitment", 
        "nlp", "machine-learning", "ai", "automation"
    ],
    
    # Optional dependencies for enhanced functionality
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
        "docs": [
            "sphinx>=7.0.0",
            "sphinx-rtd-theme>=1.3.0",
        ],
    },
    
    # Project URLs
    project_urls={
        "Bug Reports": "https://github.com/yourusername/resume-shortlisting-system/issues",
        "Source": "https://github.com/yourusername/resume-shortlisting-system",
        "Documentation": "https://github.com/yourusername/resume-shortlisting-system/blob/main/README.md",
    },
)
#!/usr/bin/env python3
"""
Agentic Resume Shortlisting System - Main Entry Point

This script provides a command-line interface for the agentic resume shortlisting
system that uses Llama 3 for intelligent candidate evaluation.

Usage:
    python agentic_main.py --job job.txt --resumes-folder ./resumes --output results.csv
    python agentic_main.py --use-sample  # Use built-in sample data
    python agentic_main.py --job job.txt --resumes-folder ./resumes --llm-off  # Traditional mode
"""

import argparse
import sys
from pathlib import Path

from agentic_shortlister import AgenticResumeShortlister
from utils import load_text, check_dependencies, print_system_info


def create_sample_data():
    """Create sample data for testing the agentic system"""
    
    sample_job = """
Senior Software Engineer - AI/ML Team

We are seeking a Senior Software Engineer to join our AI/ML team. The ideal candidate will have:

Required Skills:
- Python programming (5+ years)
- Machine Learning frameworks (TensorFlow, PyTorch)
- Cloud platforms (AWS, Azure, GCP)
- Docker and Kubernetes
- RESTful API development
- Git version control

Preferred Skills:
- Natural Language Processing
- Computer Vision
- MLOps and model deployment
- Agile development methodologies
- Leadership and mentoring experience

Responsibilities:
- Design and implement ML models
- Build scalable AI systems
- Collaborate with cross-functional teams
- Mentor junior developers
- Contribute to technical architecture decisions

Requirements:
- Bachelor's degree in Computer Science or related field
- 5+ years of software development experience
- 3+ years of ML/AI experience
- Strong problem-solving skills
- Excellent communication abilities
"""
    
    sample_resume = """
John Smith
Senior Software Engineer

EXPERIENCE:
Senior ML Engineer | TechCorp | 2020-2024
- Developed and deployed 15+ machine learning models using Python and TensorFlow
- Built scalable ML pipelines on AWS using Docker and Kubernetes
- Led a team of 4 junior engineers on NLP projects
- Implemented MLOps practices reducing deployment time by 60%
- Created RESTful APIs serving 1M+ requests daily

Software Engineer | DataSoft | 2018-2020
- Developed web applications using Python, Django, and PostgreSQL
- Implemented CI/CD pipelines using Git and Jenkins
- Collaborated with product teams using Agile methodologies
- Optimized database queries improving performance by 40%

EDUCATION:
Master of Science in Computer Science | Stanford University | 2018
Bachelor of Science in Computer Science | UC Berkeley | 2016

SKILLS:
- Programming: Python, Java, JavaScript, SQL
- ML/AI: TensorFlow, PyTorch, scikit-learn, OpenCV
- Cloud: AWS (EC2, S3, Lambda), Docker, Kubernetes
- Tools: Git, Jenkins, Jira, Confluence
- Databases: PostgreSQL, MongoDB, Redis

CERTIFICATIONS:
- AWS Certified Machine Learning Specialist
- Google Cloud Professional ML Engineer

PROJECTS:
- Built a computer vision system for quality control (99.2% accuracy)
- Developed NLP chatbot handling 10K+ customer queries daily
- Created recommendation engine increasing user engagement by 25%
"""
    
    return sample_job, sample_resume


def main():
    """Main entry point for the agentic shortlisting system"""
    
    parser = argparse.ArgumentParser(
        description="Agentic Resume Shortlisting System with Llama 3",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python agentic_main.py --use-sample
  python agentic_main.py --job job_description.txt --resumes-folder ./candidates
  python agentic_main.py --job job.txt --resumes-folder ./resumes --output results.csv --llm-off
        """
    )
    
    parser.add_argument(
        "--job", 
        type=Path,
        help="Path to job description file"
    )
    
    parser.add_argument(
        "--resumes-folder", 
        type=Path,
        help="Folder containing resume files"
    )
    
    parser.add_argument(
        "--output", 
        type=Path,
        default="agentic_shortlist_results.csv",
        help="Output CSV file path (default: agentic_shortlist_results.csv)"
    )
    
    parser.add_argument(
        "--use-sample", 
        action="store_true",
        help="Use built-in sample data for testing"
    )
    
    parser.add_argument(
        "--llm-off", 
        action="store_true",
        help="Disable Llama 3 and use traditional NLP only"
    )
    
    parser.add_argument(
        "--threshold", 
        type=float,
        default=0.65,
        help="Score threshold for shortlisting (0.0-1.0, default: 0.65)"
    )
    
    parser.add_argument(
        "--system-info", 
        action="store_true",
        help="Show system information and dependencies"
    )
    
    args = parser.parse_args()
    
    # Show system info if requested
    if args.system_info:
        print_system_info()
        return
    
    # Validate arguments
    if not args.use_sample:
        if not args.job or not args.resumes_folder:
            print("Error: --job and --resumes-folder are required (or use --use-sample)")
            parser.print_help()
            sys.exit(1)
    
    print("Agentic Resume Shortlisting System")
    print("=" * 50)
    
    # Check dependencies
    deps = check_dependencies()
    if not deps["pdf_support"]:
        print("Warning: PDF support not available. Install with: pip install pypdf")
    
    # Initialize the agentic system
    use_llm = not args.llm_off
    shortlister = AgenticResumeShortlister(
        use_llm=use_llm, 
        score_threshold=args.threshold
    )
    
    try:
        if args.use_sample:
            # Use sample data
            print("\nUsing sample data for demonstration")
            
            job_description, sample_resume = create_sample_data()
            
            resume_inputs = [{
                "text": sample_resume,
                "path": "sample_resume.txt"
            }]
            
            # Process sample data
            results = shortlister.process_resumes(resume_inputs, job_description)
            
            # Write results
            shortlister.write_enhanced_csv(results, args.output)
            
        else:
            # Process real data
            results = shortlister.process_folder(
                args.resumes_folder,
                args.job,
                args.output
            )
        
        print("\nAgentic analysis completed successfully!")
        
        if use_llm:
            print("\nLlama 3 provided intelligent insights including:")
            print("   - Structured skill extraction")
            print("   - Experience level assessment")
            print("   - Strengths and gaps analysis")
            print("   - Intelligent recommendations")
            print("   - Targeted interview questions")
        else:
            print("\nTraditional NLP analysis completed")
        
        print(f"\nResults saved to: {args.output}")
        
    except KeyboardInterrupt:
        print("\nProcess interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
"""
Resume Shortlisting CLI

A command-line interface for automated resume screening and candidate shortlisting.
This tool uses advanced NLP techniques including TF-IDF and semantic similarity
to evaluate resumes against job descriptions and provide ranked candidate lists.

Author: [Your Name]
Date: 2024
"""

import argparse
import sys
from pathlib import Path
from typing import List, Dict, Any

from shortlisting import ResumeShortlistingAgent
from utils import extract_text_from_pdf, print_json


def load_text_from_file(file_path: Path) -> str:
    """
    Load text content from a file, supporting both PDF and text formats.
    
    Args:
        file_path: Path to the file to be loaded
        
    Returns:
        str: Extracted text content
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        ValueError: If the file format is not supported
    """
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    if file_path.suffix.lower() == ".pdf":
        return extract_text_from_pdf(file_path)
    elif file_path.suffix.lower() in [".txt", ".md"]:
        return file_path.read_text(encoding="utf-8").strip()
    else:
        raise ValueError(f"Unsupported file format: {file_path.suffix}")


def validate_inputs(args: argparse.Namespace) -> None:
    """
    Validate command line arguments to ensure all required inputs are provided.
    
    Args:
        args: Parsed command line arguments
        
    Raises:
        SystemExit: If validation fails
    """
    if args.use_sample:
        # Sample data validation is handled internally
        return
    
    if not args.job:
        print("Error: Job description file is required (--job)")
        sys.exit(1)
    
    if args.resumes_folder:
        if not args.resumes_folder.is_dir():
            print(f"Error: Resume folder does not exist: {args.resumes_folder}")
            sys.exit(1)
    elif args.resumes:
        # Validate individual resume files
        for resume_file in args.resumes:
            if not resume_file.exists():
                print(f"Error: Resume file not found: {resume_file}")
                sys.exit(1)
    elif args.resume:
        if not args.resume.exists():
            print(f"Error: Resume file not found: {args.resume}")
            sys.exit(1)
    else:
        print("Error: Must provide either --resume, --resumes, or --resumes-folder")
        sys.exit(1)


def setup_argument_parser() -> argparse.ArgumentParser:
    """
    Configure and return the command line argument parser.
    
    Returns:
        argparse.ArgumentParser: Configured argument parser
    """
    parser = argparse.ArgumentParser(
        description="Resume Shortlisting System - Automated candidate screening using NLP",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process individual resumes
  python main.py --job job_desc.txt --resumes resume1.pdf resume2.pdf

  # Process entire folder of resumes
  python main.py --job job_desc.txt --resumes-folder ./candidates/

  # Use sample data for testing
  python main.py --use-sample

  # Custom output file
  python main.py --job job_desc.txt --resumes-folder ./candidates/ --output results.csv
        """
    )
    
    # Input arguments
    parser.add_argument(
        "--job", 
        type=Path, 
        help="Path to job description file (.txt or .pdf)"
    )
    parser.add_argument(
        "--resume", 
        type=Path, 
        help="Path to a single resume file (.txt or .pdf)"
    )
    parser.add_argument(
        "--resumes", 
        type=Path, 
        nargs="+", 
        help="Paths to multiple resume files (.txt or .pdf)"
    )
    parser.add_argument(
        "--resumes-folder", 
        type=Path, 
        help="Folder containing resume files to process"
    )
    
    # Output arguments
    parser.add_argument(
        "--output", 
        type=Path, 
        default=Path("shortlist_results.csv"),
        help="Output CSV file for results (default: shortlist_results.csv)"
    )
    
    # Options
    parser.add_argument(
        "--use-sample", 
        action="store_true",
        help="Use built-in sample data for demonstration"
    )
    parser.add_argument(
        "--threshold", 
        type=float, 
        default=0.6,
        help="Minimum score threshold for shortlisting (0.0-1.0, default: 0.6)"
    )
    parser.add_argument(
        "--max-candidates", 
        type=int, 
        default=10,
        help="Maximum number of candidates to shortlist (default: 10)"
    )
    
    return parser


def process_sample_data() -> List[Dict[str, Any]]:
    """
    Process built-in sample data for demonstration purposes.
    
    Returns:
        List[Dict[str, Any]]: Shortlisting results
    """
    print("Using sample data for demonstration...")
    
    # Load sample files
    data_dir = Path(__file__).parent / "data"
    job_description = load_text_from_file(data_dir / "sample_job_description.txt")
    
    # Create sample resume inputs
    resume_inputs = []
    sample_resume_text = load_text_from_file(data_dir / "sample_resume.txt")
    resume_inputs.append({
        "path": data_dir / "sample_resume.txt",
        "text": sample_resume_text
    })
    
    # Initialize and run shortlisting agent
    agent = ResumeShortlistingAgent()
    return agent.run(resume_inputs, job_description)


def process_individual_resumes(resume_files: List[Path], job_file: Path) -> List[Dict[str, Any]]:
    """
    Process individual resume files against a job description.
    
    Args:
        resume_files: List of resume file paths
        job_file: Job description file path
        
    Returns:
        List[Dict[str, Any]]: Shortlisting results
    """
    print(f"Processing {len(resume_files)} resume(s)...")
    
    # Load job description
    job_description = load_text_from_file(job_file)
    
    # Load resume files
    resume_inputs = []
    for resume_file in resume_files:
        try:
            resume_text = load_text_from_file(resume_file)
            resume_inputs.append({
                "path": resume_file,
                "text": resume_text
            })
            print(f"  ✓ Loaded: {resume_file.name}")
        except Exception as e:
            print(f"  ✗ Failed to load {resume_file.name}: {e}")
    
    # Run shortlisting
    agent = ResumeShortlistingAgent()
    return agent.run(resume_inputs, job_description)


def main() -> None:
    """
    Main entry point for the resume shortlisting CLI.
    
    This function orchestrates the entire shortlisting process:
    1. Parse command line arguments
    2. Validate inputs
    3. Process resumes based on input type
    4. Generate and save results
    """
    # Parse command line arguments
    parser = setup_argument_parser()
    args = parser.parse_args()
    
    # Validate inputs
    validate_inputs(args)
    
    print("=" * 60)
    print("Resume Shortlisting System")
    print("=" * 60)
    
    try:
        # Process based on input type
        if args.use_sample:
            results = process_sample_data()
        elif args.resumes_folder:
            # Use the agent's built-in folder processing
            print(f"Processing resume folder: {args.resumes_folder}")
            agent = ResumeShortlistingAgent()
            results = agent.process_folder(args.resumes_folder, args.job, args.output)
        else:
            # Process individual files
            resume_files = args.resumes or [args.resume]
            results = process_individual_resumes(resume_files, args.job)
            
            # Save results to CSV
            agent = ResumeShortlistingAgent()
            agent.write_csv(results, args.output)
        
        # Display results summary
        print("\n" + "=" * 60)
        print("SHORTLISTING RESULTS")
        print("=" * 60)
        print(f"Total candidates processed: {len(results)}")
        
        # Count shortlisted candidates
        shortlisted = [r for r in results if r.get('decision') == 'SHORTLIST']
        print(f"Candidates shortlisted: {len(shortlisted)}")
        
        if shortlisted:
            print(f"\nTop candidates:")
            for i, candidate in enumerate(shortlisted[:5], 1):
                score = candidate.get('overall_score', 0)
                name = Path(candidate.get('resume_path', 'Unknown')).stem
                print(f"  {i}. {name} (Score: {score:.3f})")
        
        print(f"\nDetailed results saved to: {args.output}")
        
        # Optional: Print JSON output for programmatic use
        if len(sys.argv) > 1 and '--json' in sys.argv:
            print_json({"results": results})
            
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)
    
    print("\nShortlisting completed successfully!")


if __name__ == "__main__":
    main()
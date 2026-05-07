"""
Utility Functions for Resume Processing

This module provides essential utilities for the resume shortlisting system:
- PDF text extraction for resume parsing
- File I/O operations with error handling
- JSON formatting for structured output
- Text processing helpers

The utilities are designed to handle various file formats commonly
used in HR workflows (PDF, TXT, DOCX).

Author: [Your Name]
Date: 2024
"""

import json
import sys
from pathlib import Path
from typing import Optional, Dict, Any

# Optional PDF processing - graceful degradation if not available
try:
    from pypdf import PdfReader
    PDF_SUPPORT = True
except ImportError:
    PdfReader = None
    PDF_SUPPORT = False

# Optional DOCX processing - for Microsoft Word documents
try:
    import docx
    DOCX_SUPPORT = True
except ImportError:
    docx = None
    DOCX_SUPPORT = False


def extract_text_from_pdf(file_path: Path) -> str:
    """
    Extract text content from PDF files using pypdf library.
    
    This function handles multi-page PDFs and concatenates all text content.
    It's essential for processing resume files that are commonly in PDF format.
    
    Args:
        file_path: Path to the PDF file to process
        
    Returns:
        Extracted text content as a single string
        
    Raises:
        RuntimeError: If pypdf library is not installed
        FileNotFoundError: If the PDF file doesn't exist
        Exception: If PDF is corrupted or unreadable
    """
    if not PDF_SUPPORT:
        raise RuntimeError(
            "PDF processing requires the 'pypdf' library. "
            "Install it with: pip install pypdf"
        )
    
    if not file_path.exists():
        raise FileNotFoundError(f"PDF file not found: {file_path}")
    
    try:
        reader = PdfReader(str(file_path))
        text_parts = []
        
        # Extract text from each page
        for page_num, page in enumerate(reader.pages):
            try:
                page_text = page.extract_text() or ""
                if page_text.strip():  # Only add non-empty pages
                    text_parts.append(page_text)
            except Exception as e:
                print(f"Warning: Could not extract text from page {page_num + 1}: {e}")
                continue
        
        # Combine all pages with proper spacing
        full_text = "\n\n".join(text_parts).strip()
        
        if not full_text:
            print(f"Warning: No text extracted from {file_path}")
            return ""
        
        return full_text
        
    except Exception as e:
        raise Exception(f"Failed to process PDF {file_path}: {e}")


def extract_text_from_docx(file_path: Path) -> str:
    """
    Extract text content from Microsoft Word documents.
    
    Args:
        file_path: Path to the DOCX file
        
    Returns:
        Extracted text content
        
    Raises:
        RuntimeError: If python-docx library is not installed
    """
    if not DOCX_SUPPORT:
        raise RuntimeError(
            "DOCX processing requires the 'python-docx' library. "
            "Install it with: pip install python-docx"
        )
    
    try:
        doc = docx.Document(str(file_path))
        paragraphs = []
        
        for paragraph in doc.paragraphs:
            text = paragraph.text.strip()
            if text:
                paragraphs.append(text)
        
        return "\n".join(paragraphs)
        
    except Exception as e:
        raise Exception(f"Failed to process DOCX {file_path}: {e}")


def load_text(file_path: Path) -> str:
    """
    Universal text loader that handles multiple file formats.
    
    This is the main entry point for loading resume content. It automatically
    detects file type based on extension and uses the appropriate parser.
    
    Supported formats:
    - .pdf: PDF documents (requires pypdf)
    - .docx: Microsoft Word documents (requires python-docx)  
    - .txt: Plain text files
    - .md: Markdown files (treated as plain text)
    
    Args:
        file_path: Path to the file to load
        
    Returns:
        Text content of the file
        
    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If file format is not supported
        Exception: If file processing fails
    """
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Get file extension (case-insensitive)
    extension = file_path.suffix.lower()
    
    try:
        if extension == ".pdf":
            return extract_text_from_pdf(file_path)
        elif extension == ".docx":
            return extract_text_from_docx(file_path)
        elif extension in [".txt", ".md"]:
            # Handle plain text files with UTF-8 encoding
            return file_path.read_text(encoding="utf-8").strip()
        else:
            raise ValueError(
                f"Unsupported file format: {extension}. "
                f"Supported formats: .pdf, .docx, .txt, .md"
            )
    
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        raise


def print_json(data: Dict[str, Any], indent: int = 2) -> None:
    """
    Print data as formatted JSON with proper encoding.
    
    This function is useful for debugging and displaying structured
    results in a readable format.
    
    Args:
        data: Dictionary or other JSON-serializable data to print
        indent: Number of spaces for indentation (default: 2)
    """
    try:
        formatted_json = json.dumps(
            data, 
            indent=indent, 
            ensure_ascii=False,  # Allow Unicode characters
            sort_keys=True       # Sort keys for consistent output
        )
        print(formatted_json)
    except (TypeError, ValueError) as e:
        print(f"Error formatting JSON: {e}")
        print(f"Raw data: {data}")


def validate_file_access(file_path: Path, required: bool = True) -> bool:
    """
    Validate that a file exists and is readable.
    
    Args:
        file_path: Path to validate
        required: Whether the file is required (affects error handling)
        
    Returns:
        True if file is accessible, False otherwise
        
    Raises:
        FileNotFoundError: If file is required but doesn't exist
    """
    if not file_path.exists():
        if required:
            raise FileNotFoundError(f"Required file not found: {file_path}")
        return False
    
    if not file_path.is_file():
        if required:
            raise ValueError(f"Path is not a file: {file_path}")
        return False
    
    # Test readability
    try:
        with file_path.open('r', encoding='utf-8') as f:
            f.read(1)  # Try to read one character
        return True
    except (PermissionError, UnicodeDecodeError):
        if required:
            raise PermissionError(f"Cannot read file: {file_path}")
        return False


def get_supported_extensions() -> list[str]:
    """
    Get list of supported file extensions based on available libraries.
    
    Returns:
        List of supported file extensions
    """
    extensions = [".txt", ".md"]  # Always supported
    
    if PDF_SUPPORT:
        extensions.append(".pdf")
    
    if DOCX_SUPPORT:
        extensions.append(".docx")
    
    return extensions


def check_dependencies() -> Dict[str, bool]:
    """
    Check which optional dependencies are available.
    
    Returns:
        Dictionary mapping dependency names to availability status
    """
    return {
        "pdf_support": PDF_SUPPORT,
        "docx_support": DOCX_SUPPORT,
    }


def print_system_info() -> None:
    """
    Print system information and dependency status.
    
    Useful for debugging and setup verification.
    """
    print("Resume Shortlisting System - Dependency Status")
    print("=" * 50)
    
    deps = check_dependencies()
    extensions = get_supported_extensions()
    
    print(f"Python version: {sys.version}")
    print(f"PDF support: {'✓' if deps['pdf_support'] else '✗'}")
    print(f"DOCX support: {'✓' if deps['docx_support'] else '✗'}")
    print(f"Supported file types: {', '.join(extensions)}")
    
    if not deps['pdf_support']:
        print("\nTo enable PDF support: pip install pypdf")
    
    if not deps['docx_support']:
        print("To enable DOCX support: pip install python-docx")


# Utility function for text preprocessing
def clean_text(text: str) -> str:
    """
    Clean and normalize text for better processing.
    
    Args:
        text: Raw text to clean
        
    Returns:
        Cleaned text with normalized whitespace
    """
    if not text:
        return ""
    
    # Normalize whitespace
    import re
    text = re.sub(r'\s+', ' ', text)
    
    # Remove excessive newlines but preserve paragraph breaks
    text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
    
    return text.strip()


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


def normalize_text(text: str) -> list[str]:
    """
    Extract alphanumeric tokens from text for analysis.
    
    Args:
        text: Input text to normalize
        
    Returns:
        List of normalized tokens (lowercase, alphanumeric + common symbols)
    """
    import re
    return re.findall(r"[A-Za-z0-9#+\-.]+", text.lower())


def filter_meaningful_terms(words: list[str]) -> set[str]:
    """
    Filter out stop words and short terms to focus on meaningful content.
    
    Args:
        words: List of words to filter
        
    Returns:
        Set of meaningful terms
    """
    from constants import STOP_WORDS
    return {
        word for word in words 
        if len(word) > 1 and word.lower() not in STOP_WORDS
    }
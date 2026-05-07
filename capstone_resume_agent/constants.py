"""
Configuration Constants for Resume Shortlisting System

This module defines the core configuration used throughout the shortlisting
system, including skill keywords, stop words, and output formats.

The skill keywords are carefully curated to cover major technology domains
and professional competencies commonly sought in technical roles.

Author: [Your Name]
Date: 2024
"""

# =============================================================================
# SKILL KEYWORDS DATABASE
# =============================================================================

# Technical Skills - Programming Languages
PROGRAMMING_LANGUAGES = [
    "python", "java", "javascript", "typescript", "c++", "c#", "go", "rust",
    "scala", "kotlin", "swift", "php", "ruby", "r", "matlab", "sql"
]

# Technical Skills - Web Technologies
WEB_TECHNOLOGIES = [
    "react", "angular", "vue", "nodejs", "express", "django", "flask",
    "spring", "rest api", "graphql", "html", "css", "sass", "webpack"
]

# Technical Skills - Cloud & DevOps
CLOUD_DEVOPS = [
    "aws", "azure", "gcp", "docker", "kubernetes", "terraform", "ansible",
    "jenkins", "ci/cd", "devops", "microservices", "serverless", "lambda"
]

# Technical Skills - Databases
DATABASES = [
    "mysql", "postgresql", "mongodb", "redis", "elasticsearch", "cassandra",
    "dynamodb", "sql server", "oracle", "nosql", "database design"
]

# Technical Skills - Data & AI
DATA_AI = [
    "machine learning", "deep learning", "data science", "artificial intelligence",
    "tensorflow", "pytorch", "pandas", "numpy", "scikit-learn", "spark",
    "hadoop", "etl", "data pipeline", "analytics", "statistics"
]

# Technical Skills - Mobile & Desktop
MOBILE_DESKTOP = [
    "ios", "android", "react native", "flutter", "xamarin", "swift",
    "objective-c", "kotlin", "electron", "wpf", "winforms"
]

# Soft Skills & Leadership
SOFT_SKILLS = [
    "leadership", "team management", "project management", "agile", "scrum",
    "communication", "problem solving", "mentoring", "collaboration",
    "strategic thinking", "innovation", "adaptability"
]

# Industry & Domain Knowledge
DOMAIN_KNOWLEDGE = [
    "fintech", "healthcare", "e-commerce", "gaming", "cybersecurity",
    "blockchain", "iot", "embedded systems", "networking", "security"
]

# Combine all skill categories into master list
DEFAULT_SKILL_KEYWORDS = (
    PROGRAMMING_LANGUAGES + 
    WEB_TECHNOLOGIES + 
    CLOUD_DEVOPS + 
    DATABASES + 
    DATA_AI + 
    MOBILE_DESKTOP + 
    SOFT_SKILLS + 
    DOMAIN_KNOWLEDGE
)

# =============================================================================
# TEXT PROCESSING CONFIGURATION
# =============================================================================

# Stop words to filter out during text analysis
# These are common words that don't add meaningful information for matching
STOP_WORDS = {
    # Articles and prepositions
    "a", "an", "and", "the", "for", "with", "that", "this", "from", "to",
    "in", "on", "at", "by", "of", "or", "but", "as", "if", "when", "where",
    
    # Common resume/job description words
    "description", "skills", "experience", "years", "year", "work", "job",
    "candidate", "required", "preferred", "responsibilities", "duties",
    "position", "role", "company", "team", "department", "organization",
    
    # Qualifiers and connectors
    "strong", "excellent", "good", "solid", "proven", "demonstrated",
    "ability", "knowledge", "understanding", "familiarity", "proficiency",
    
    # Time and quantity words
    "minimum", "maximum", "plus", "over", "under", "more", "less", "than",
    "must", "should", "will", "can", "may", "able", "capable"
}

# =============================================================================
# OUTPUT CONFIGURATION
# =============================================================================

# CSV column headers for shortlisting results
CSV_FIELDNAMES = [
    "candidate_name",      # Extracted candidate name
    "source_file",         # Original resume file path
    "status",             # SHORTLIST or REJECT decision
    "score",              # Overall matching score (0.0-1.0)
    "matched_skills",     # Skills found in both resume and job description
    "required_skills",    # All skills extracted from job description
    "summary"             # Human-readable evaluation summary
]

# =============================================================================
# SCORING CONFIGURATION
# =============================================================================

# Default scoring weights for hybrid evaluation
SCORING_WEIGHTS = {
    "skill_matching": 0.4,      # Weight for skill overlap
    "term_overlap": 0.3,        # Weight for keyword matching
    "semantic_similarity": 0.3   # Weight for semantic understanding
}

# Default thresholds for decision making
DEFAULT_THRESHOLDS = {
    "score_threshold": 0.6,           # Minimum overall score for shortlisting
    "min_skills_required": 2,         # Minimum matched skills for auto-shortlist
    "max_candidates": 50              # Maximum candidates to process in batch
}

# =============================================================================
# FILE PROCESSING CONFIGURATION
# =============================================================================

# Supported file extensions for resume processing
SUPPORTED_EXTENSIONS = [".pdf", ".txt", ".docx", ".md"]

# Maximum file size for processing (in MB)
MAX_FILE_SIZE_MB = 10

# Text length limits
MAX_TEXT_LENGTH = 50000  # Maximum characters per document
MIN_TEXT_LENGTH = 100    # Minimum characters for valid resume

# =============================================================================
# SYSTEM CONFIGURATION
# =============================================================================

# Default embedding model for semantic similarity
DEFAULT_EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# Vector store configuration
VECTOR_STORE_CONFIG = {
    "collection_name": "resume_shortlisting",
    "distance_metric": "cosine",
    "embedding_dimension": 384  # Dimension for all-MiniLM-L6-v2
}

# Logging configuration
LOG_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "date_format": "%Y-%m-%d %H:%M:%S"
}
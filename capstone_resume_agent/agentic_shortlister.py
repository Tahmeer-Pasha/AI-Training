"""
Agentic Resume Shortlisting System with Llama 3 Integration

This module implements an intelligent resume screening system that combines:
- Traditional NLP techniques (TF-IDF, embeddings)
- Llama 3 LLM for intelligent analysis and structured insights
- Multi-factor scoring for comprehensive assessment

Author: AI Learning Project
Date: 2024
"""

import csv
import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Any, Optional

from constants import CSV_FIELDNAMES, DEFAULT_SKILL_KEYWORDS, STOP_WORDS
from llm_agent import LlamaAgent
from retrieval.vector_store import VectorStore
from utils import load_text, extract_candidate_name, normalize_text, filter_meaningful_terms

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class AgenticEvaluation:
    """Enhanced evaluation results with LLM insights"""
    candidate_name: str
    resume_path: str
    decision: str
    overall_score: float
    llm_score: float
    skill_match_score: float
    semantic_score: float
    matched_skills: str
    extracted_skills: str
    years_experience: int
    education_level: str
    strengths: str
    gaps: str
    recommendation: str
    reasoning: str
    interview_questions: str
    
    def to_csv_row(self) -> Dict[str, str]:
        """Convert to CSV format with enhanced fields"""
        return {
            "candidate_name": self.candidate_name,
            "source_file": self.resume_path,
            "status": self.decision,
            "overall_score": f"{self.overall_score:.2f}",
            "llm_score": f"{self.llm_score:.2f}",
            "skill_match_score": f"{self.skill_match_score:.2f}",
            "semantic_score": f"{self.semantic_score:.2f}",
            "matched_skills": self.matched_skills,
            "extracted_skills": self.extracted_skills,
            "years_experience": str(self.years_experience),
            "education_level": self.education_level,
            "strengths": self.strengths,
            "gaps": self.gaps,
            "recommendation": self.recommendation,
            "reasoning": self.reasoning[:200] + "..." if len(self.reasoning) > 200 else self.reasoning,
            "interview_questions": self.interview_questions[:300] + "..." if len(self.interview_questions) > 300 else self.interview_questions
        }


class AgenticResumeShortlister:
    """
    Advanced Agentic Resume Shortlisting System with Llama 3
    
    This system combines traditional NLP with LLM intelligence for:
    - Structured skill and experience extraction
    - Intelligent job-candidate matching
    - Automated interview question generation
    - Comprehensive evaluation with reasoning
    """
    
    def __init__(self, use_llm: bool = True, score_threshold: float = 0.65):
        """
        Initialize the agentic shortlisting system
        
        Args:
            use_llm: Whether to use Llama 3 for enhanced analysis
            score_threshold: Minimum score for shortlisting
        """
        self.use_llm = use_llm
        self.score_threshold = score_threshold
        
        # Initialize LLM agent
        if self.use_llm:
            self.llm_agent = LlamaAgent()
            if self.llm_agent.check_ollama_connection():
                print("Llama 3 agent initialized successfully")
                print("Agentic AI System: Llama 3 connected and ready")
            else:
                logger.warning("⚠ Ollama not available, using traditional methods")
                print("Llama 3 not available - falling back to traditional NLP")
                self.use_llm = False
        
        # Initialize vector store for semantic analysis
        self.vector_store = VectorStore()
        
        # Enhanced CSV fieldnames for LLM output
        self.enhanced_fieldnames = [
            "candidate_name", "source_file", "status", "overall_score", 
            "llm_score", "skill_match_score", "semantic_score",
            "matched_skills", "extracted_skills", "years_experience", 
            "education_level", "strengths", "gaps", "recommendation", 
            "reasoning", "interview_questions"
        ]
        
        print(f"Agentic Resume Shortlister initialized")
        print(f"   LLM Mode: {'ON' if self.use_llm else 'OFF'}")
        print(f"   Score Threshold: {score_threshold}")
    
    def extract_skills_from_text(self, text: str) -> List[str]:
        """Extract skills using keyword matching"""
        text_lower = text.lower()
        found_skills = []
        
        for keyword in sorted(DEFAULT_SKILL_KEYWORDS, key=len, reverse=True):
            if keyword in text_lower and keyword not in found_skills:
                found_skills.append(keyword)
        
        return found_skills
    
    def calculate_skill_match_score(self, resume_text: str, job_description: str) -> tuple:
        """Calculate traditional skill matching score"""
        required_skills = self.extract_skills_from_text(job_description)
        candidate_skills = self.extract_skills_from_text(resume_text)
        
        matched_skills = list(set(required_skills) & set(candidate_skills))
        score = len(matched_skills) / max(1, len(required_skills)) * 100
        
        return score, matched_skills
    
    def calculate_semantic_similarity(self, resume_text: str, job_description: str) -> float:
        """Calculate semantic similarity using vector embeddings"""
        try:
            documents = [resume_text, job_description]
            metadatas = [{"type": "resume"}, {"type": "job"}]
            
            self.vector_store.add_documents(documents, metadatas)
            results = self.vector_store.query(job_description, n_results=1)
            
            if results and "distances" in results and results["distances"]:
                distance = results["distances"][0][0]
                similarity = (1.0 - distance) * 100  # Convert to percentage
                return max(0.0, min(100.0, similarity))
            
        except Exception as e:
            logger.error(f"Semantic similarity calculation failed: {e}")
        
        return 0.0
    
    def evaluate_candidate(self, resume_text: str, job_description: str, 
                          resume_file: Optional[Path] = None) -> AgenticEvaluation:
        """
        Comprehensive agentic evaluation of candidate
        
        Args:
            resume_text: Full resume content
            job_description: Job requirements
            resume_file: Source file path
            
        Returns:
            AgenticEvaluation with detailed LLM insights
        """
        file_path = str(resume_file) if resume_file else "sample_resume"
        candidate_name = extract_candidate_name(resume_text, resume_file)
        
        # Traditional scoring
        skill_score, matched_skills = self.calculate_skill_match_score(resume_text, job_description)
        semantic_score = self.calculate_semantic_similarity(resume_text, job_description)
        
        if self.use_llm:
            # LLM-powered analysis
            try:
                print(f"Analyzing {candidate_name} with Llama 3...")
                
                # Extract structured data
                resume_data = self.llm_agent.extract_skills_and_experience(resume_text)
                
                # Get intelligent evaluation
                llm_evaluation = self.llm_agent.evaluate_job_match(resume_data, job_description)
                
                # Generate interview questions
                interview_questions = self.llm_agent.generate_interview_questions(resume_data, job_description)
                
                # Combine scores (LLM gets higher weight)
                llm_score = llm_evaluation.get('overall_score', 50)
                overall_score = (
                    llm_score * 0.6 +           # 60% LLM analysis
                    skill_score * 0.25 +        # 25% skill matching
                    semantic_score * 0.15       # 15% semantic similarity
                )
                
                # Enhanced decision logic
                should_shortlist = (
                    overall_score >= self.score_threshold or
                    llm_evaluation.get('recommendation', '').lower() in ['strong match', 'good match'] or
                    len(matched_skills) >= 3
                )
                
                return AgenticEvaluation(
                    candidate_name=candidate_name,
                    resume_path=file_path,
                    decision="SHORTLIST" if should_shortlist else "REJECT",
                    overall_score=overall_score,
                    llm_score=llm_score,
                    skill_match_score=skill_score,
                    semantic_score=semantic_score,
                    matched_skills=", ".join(matched_skills) if matched_skills else "None",
                    extracted_skills=", ".join(resume_data.get('technical_skills', [])[:10]),
                    years_experience=resume_data.get('years_experience', 0),
                    education_level=resume_data.get('education_level', 'Unknown'),
                    strengths="; ".join(llm_evaluation.get('strengths', [])[:3]),
                    gaps="; ".join(llm_evaluation.get('gaps', [])[:3]),
                    recommendation=llm_evaluation.get('recommendation', 'Requires Review'),
                    reasoning=llm_evaluation.get('reasoning', 'LLM analysis completed'),
                    interview_questions="; ".join(interview_questions[:3])
                )
                
            except Exception as e:
                logger.error(f"LLM analysis failed for {candidate_name}: {e}")
                # Fall back to traditional analysis
        
        # Traditional analysis (fallback or when LLM disabled)
        traditional_score = (skill_score * 0.6 + semantic_score * 0.4)
        should_shortlist = traditional_score >= self.score_threshold
        
        if traditional_score >= 80:
            recommendation = "Strong Match"
        elif traditional_score >= 65:
            recommendation = "Good Match"
        elif traditional_score >= 50:
            recommendation = "Moderate Match"
        else:
            recommendation = "Weak Match"
        
        return AgenticEvaluation(
            candidate_name=candidate_name,
            resume_path=file_path,
            decision="SHORTLIST" if should_shortlist else "REJECT",
            overall_score=traditional_score,
            llm_score=0.0,
            skill_match_score=skill_score,
            semantic_score=semantic_score,
            matched_skills=", ".join(matched_skills) if matched_skills else "None",
            extracted_skills="Traditional analysis - skills not extracted",
            years_experience=0,
            education_level="Not analyzed",
            strengths="Traditional analysis - strengths not identified",
            gaps="Traditional analysis - gaps not identified",
            recommendation=recommendation,
            reasoning=f"Traditional scoring: {traditional_score:.1f}% based on skill matching and semantic similarity",
            interview_questions="LLM not available - manual question generation needed"
        )
    
    def process_resumes(self, resume_inputs: List[Dict[str, Any]], 
                       job_description: str) -> List[Dict[str, str]]:
        """
        Process multiple resumes with agentic analysis
        
        Args:
            resume_inputs: List of resume data dictionaries
            job_description: Job requirements text
            
        Returns:
            List of evaluation results
        """
        results = []
        
        print(f"\nStarting agentic analysis of {len(resume_inputs)} candidates...")
        if self.use_llm:
            print("Using Llama 3 for intelligent evaluation")
        else:
            print("Using traditional NLP methods")
        
        for i, resume_data in enumerate(resume_inputs, 1):
            resume_text = resume_data["text"]
            resume_path = resume_data.get("path")
            
            if isinstance(resume_path, str):
                resume_path = Path(resume_path)
            
            print(f"\n[{i}/{len(resume_inputs)}] Processing: {resume_path.name if resume_path else 'sample'}")
            
            try:
                evaluation = self.evaluate_candidate(resume_text, job_description, resume_path)
                results.append(evaluation.to_csv_row())
                
                # Show quick results
                print(f"   Decision: {evaluation.decision}")
                print(f"   Overall Score: {evaluation.overall_score:.1f}%")
                if self.use_llm:
                    print(f"   LLM Score: {evaluation.llm_score:.1f}%")
                    print(f"   Recommendation: {evaluation.recommendation}")
                
            except Exception as e:
                logger.error(f"Failed to process {resume_path}: {e}")
                continue
        
        return results
    
    def write_enhanced_csv(self, results: List[Dict[str, str]], output_path: Path) -> None:
        """Write results to CSV with enhanced fields"""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with output_path.open("w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.enhanced_fieldnames)
            writer.writeheader()
            
            for result in results:
                writer.writerow(result)
        
        print(f"\nEnhanced results written to: {output_path}")
    
    def process_folder(self, resumes_folder: Path, job_description_path: Path, 
                      output_csv: Path) -> List[Dict[str, str]]:
        """Process folder of resumes with agentic analysis"""
        print(f"\nAgentic Resume Shortlisting System")
        print(f"Processing folder: {resumes_folder}")
        
        # Load job description
        job_description = load_text(job_description_path)
        print(f"Job description loaded: {len(job_description)} characters")
        
        # Find resume files
        resume_files = []
        for pattern in ["*.pdf", "*.txt", "*.docx"]:
            resume_files.extend(resumes_folder.glob(pattern))
        
        resume_files.sort()
        
        if not resume_files:
            print(f"No resume files found in {resumes_folder}")
            return []
        
        print(f"Found {len(resume_files)} resume files")
        
        # Prepare resume inputs
        resume_inputs = []
        for resume_path in resume_files:
            try:
                resume_text = load_text(resume_path)
                resume_inputs.append({"text": resume_text, "path": resume_path})
            except Exception as e:
                print(f"Failed to load {resume_path.name}: {e}")
        
        # Process with agentic analysis
        results = self.process_resumes(resume_inputs, job_description)
        
        # Write enhanced results
        self.write_enhanced_csv(results, output_csv)
        
        # Summary statistics
        shortlisted = sum(1 for r in results if r["status"] == "SHORTLIST")
        print(f"\nProcessing Summary:")
        print(f"   Total Processed: {len(results)}")
        print(f"   Shortlisted: {shortlisted}")
        print(f"   Rejection Rate: {((len(results) - shortlisted) / len(results) * 100):.1f}%")
        
        return results
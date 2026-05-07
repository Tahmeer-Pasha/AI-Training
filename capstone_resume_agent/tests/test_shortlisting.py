"""
Test Suite for Resume Shortlisting System

This module contains unit tests to verify the core functionality
of the resume shortlisting system.

Author: [Your Name]
Date: 2024
"""

import pytest
from pathlib import Path
import tempfile
import csv

from shortlisting import ResumeShortlistingAgent, CandidateEvaluation
from utils import load_text, print_json
from constants import DEFAULT_SKILL_KEYWORDS


class TestResumeShortlistingAgent:
    """Test cases for the main shortlisting agent."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.agent = ResumeShortlistingAgent(score_threshold=0.5)
        
        # Sample job description
        self.job_description = """
        Software Engineer Position
        
        We are looking for a skilled software engineer with experience in:
        - Python programming
        - AWS cloud services
        - Docker containerization
        - REST API development
        - Agile methodologies
        
        The ideal candidate should have strong problem-solving skills
        and experience with microservices architecture.
        """
        
        # Sample resume (good match)
        self.good_resume = """
        John Smith
        Senior Software Engineer
        
        Experience:
        - 5 years of Python development
        - Extensive AWS experience including EC2, S3, Lambda
        - Docker and Kubernetes expertise
        - Built multiple REST APIs using Flask and Django
        - Worked in Agile/Scrum teams
        - Microservices architecture design
        
        Skills: Python, AWS, Docker, REST API, Agile, Microservices
        """
        
        # Sample resume (poor match)
        self.poor_resume = """
        Jane Doe
        Marketing Specialist
        
        Experience:
        - Social media marketing
        - Content creation
        - Brand management
        - Customer engagement
        
        Skills: Marketing, Social Media, Content Writing
        """
    
    def test_skill_extraction(self):
        """Test that skills are correctly extracted from text."""
        from shortlisting import extract_skills_from_text
        
        skills = extract_skills_from_text(self.job_description)
        
        # Should find key skills mentioned in job description
        assert "python" in skills
        assert "aws" in skills
        assert "docker" in skills
        assert "rest api" in skills
        assert "agile" in skills
    
    def test_candidate_evaluation_good_match(self):
        """Test evaluation of a well-matched candidate."""
        evaluation = self.agent.evaluate_candidate(
            self.good_resume, 
            self.job_description
        )
        
        # Should be shortlisted with good score
        assert evaluation.decision == "SHORTLIST"
        assert evaluation.overall_score > 0.5
        assert evaluation.candidate_name == "John Smith"
        assert "python" in evaluation.matched_skills.lower()
        assert "aws" in evaluation.matched_skills.lower()
    
    def test_candidate_evaluation_poor_match(self):
        """Test evaluation of a poorly matched candidate."""
        evaluation = self.agent.evaluate_candidate(
            self.poor_resume, 
            self.job_description
        )
        
        # Should be rejected with low score
        assert evaluation.decision == "REJECT"
        assert evaluation.overall_score < 0.5
        assert evaluation.candidate_name == "Jane Doe"
    
    def test_batch_processing(self):
        """Test processing multiple resumes at once."""
        resume_inputs = [
            {"path": Path("good_resume.txt"), "text": self.good_resume},
            {"path": Path("poor_resume.txt"), "text": self.poor_resume}
        ]
        
        results = self.agent.run(resume_inputs, self.job_description)
        
        # Should return results for both resumes
        assert len(results) == 2
        
        # First result should be shortlisted, second rejected
        assert results[0]["status"] == "SHORTLIST"
        assert results[1]["status"] == "REJECT"
    
    def test_csv_output(self):
        """Test CSV file generation."""
        resume_inputs = [
            {"path": Path("test_resume.txt"), "text": self.good_resume}
        ]
        
        results = self.agent.run(resume_inputs, self.job_description)
        
        # Write to temporary CSV file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            temp_path = Path(f.name)
        
        try:
            self.agent.write_csv(results, temp_path)
            
            # Verify CSV was created and has correct structure
            assert temp_path.exists()
            
            with temp_path.open('r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                
                assert len(rows) == 1
                assert "candidate_name" in rows[0]
                assert "status" in rows[0]
                assert "score" in rows[0]
                
        finally:
            # Clean up temporary file
            if temp_path.exists():
                temp_path.unlink()


class TestUtilities:
    """Test cases for utility functions."""
    
    def test_load_text_from_string_file(self):
        """Test loading text from a temporary text file."""
        test_content = "This is a test resume content."
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(test_content)
            temp_path = Path(f.name)
        
        try:
            loaded_content = load_text(temp_path)
            assert loaded_content == test_content
        finally:
            temp_path.unlink()
    
    def test_print_json_functionality(self):
        """Test JSON printing utility."""
        test_data = {"test": "data", "number": 42}
        
        # Should not raise any exceptions
        try:
            print_json(test_data)
        except Exception as e:
            pytest.fail(f"print_json raised an exception: {e}")


class TestConstants:
    """Test cases for configuration constants."""
    
    def test_skill_keywords_exist(self):
        """Test that skill keywords are properly defined."""
        assert len(DEFAULT_SKILL_KEYWORDS) > 0
        assert "python" in DEFAULT_SKILL_KEYWORDS
        assert "java" in DEFAULT_SKILL_KEYWORDS
        assert "aws" in DEFAULT_SKILL_KEYWORDS
    
    def test_skill_keywords_are_lowercase(self):
        """Test that all skill keywords are lowercase for consistency."""
        for skill in DEFAULT_SKILL_KEYWORDS:
            assert skill == skill.lower(), f"Skill '{skill}' is not lowercase"


def test_sample_data_exists():
    """Test that sample data files exist and are readable."""
    data_dir = Path(__file__).parent / "data"
    
    sample_files = [
        "sample_resume.txt",
        "sample_job_description.txt",
        "sample_skills.txt"
    ]
    
    for filename in sample_files:
        file_path = data_dir / filename
        assert file_path.exists(), f"Sample file missing: {filename}"
        
        # Should be readable
        content = load_text(file_path)
        assert len(content) > 0, f"Sample file is empty: {filename}"


if __name__ == "__main__":
    # Run tests when script is executed directly
    pytest.main([__file__, "-v"])
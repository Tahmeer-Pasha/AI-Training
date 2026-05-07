"""
LLM Agent for Resume Analysis using Llama 3
Provides intelligent resume evaluation and structured insights extraction
"""

import json
import requests
from typing import Dict, List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class LlamaAgent:
    """Agentic AI system using Llama 3 for resume analysis"""
    
    def __init__(self, model_name: str = "llama3", base_url: str = "http://localhost:11434"):
        self.model_name = model_name
        self.base_url = base_url
        self.api_url = f"{base_url}/api/generate"
        
    def _call_llama(self, prompt: str, temperature: float = 0.3) -> str:
        """Make API call to Ollama Llama 3"""
        try:
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": temperature,
                    "top_p": 0.9,
                    "max_tokens": 500,
                    "num_predict": 500
                }
            }
            
            response = requests.post(self.api_url, json=payload, timeout=120)
            response.raise_for_status()
            
            result = response.json()
            return result.get("response", "").strip()
            
        except Exception as e:
            logger.error(f"Error calling Llama 3: {e}")
            return ""
    
    def extract_skills_and_experience(self, resume_text: str) -> Dict:
        """Extract structured skills and experience using Llama 3"""
        prompt = f"""
Analyze this resume and extract key information. Return only valid JSON.

Resume: {resume_text[:2000]}

Return JSON:
{{
    "technical_skills": ["python", "tensorflow"],
    "years_experience": 5,
    "education_level": "Bachelor's",
    "key_achievements": ["achievement1"],
    "domain_expertise": ["AI/ML"]
}}
"""
        
        response = self._call_llama(prompt, temperature=0.1)
        
        try:
            # Extract JSON from response
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            if start_idx != -1 and end_idx != -1:
                json_str = response[start_idx:end_idx]
                return json.loads(json_str)
        except:
            pass
            
        # Fallback structure
        return {
            "technical_skills": [],
            "years_experience": 0,
            "education_level": "Unknown",
            "key_achievements": [],
            "domain_expertise": []
        }
    
    def evaluate_job_match(self, resume_data: Dict, job_description: str) -> Dict:
        """Evaluate how well resume matches job requirements using Llama 3"""
        prompt = f"""
Evaluate this candidate for the job. Return only JSON.

Job: {job_description[:1000]}

Candidate:
- Skills: {resume_data.get('technical_skills', [])}
- Experience: {resume_data.get('years_experience', 0)} years

Return JSON:
{{
    "overall_score": 75,
    "recommendation": "Good Match",
    "strengths": ["Python", "ML experience"],
    "gaps": ["Cloud experience"],
    "reasoning": "Strong technical background"
}}
"""
        
        response = self._call_llama(prompt, temperature=0.2)
        
        try:
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            if start_idx != -1 and end_idx != -1:
                json_str = response[start_idx:end_idx]
                return json.loads(json_str)
        except:
            pass
            
        # Fallback evaluation
        return {
            "overall_score": 50,
            "skill_match_score": 50,
            "experience_match_score": 50,
            "education_match_score": 50,
            "strengths": ["Analysis unavailable"],
            "gaps": ["Analysis unavailable"],
            "recommendation": "Requires Manual Review",
            "reasoning": "LLM analysis failed, manual review needed"
        }
    
    def generate_interview_questions(self, resume_data: Dict, job_description: str) -> List[str]:
        """Generate targeted interview questions using Llama 3"""
        prompt = f"""
Generate 3 interview questions for this candidate.

Job: {job_description[:800]}
Skills: {resume_data.get('technical_skills', [])}

Return JSON:
{{
    "questions": [
        "Tell me about your Python experience",
        "How do you approach ML problems?",
        "Describe a challenging project"
    ]
}}
"""
        
        response = self._call_llama(prompt, temperature=0.4)
        
        try:
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            if start_idx != -1 and end_idx != -1:
                json_str = response[start_idx:end_idx]
                data = json.loads(json_str)
                return data.get("questions", [])
        except:
            pass
            
        return [
            "Tell me about your most challenging project",
            "How do you stay updated with technology trends?",
            "Describe a time you solved a complex problem",
            "What interests you about this role?",
            "How do you handle tight deadlines?"
        ]
    
    def check_ollama_connection(self) -> bool:
        """Check if Ollama is running and Llama 3 is available"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get("models", [])
                return any(self.model_name in model.get("name", "") for model in models)
        except:
            pass
        return False
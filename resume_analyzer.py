import json
import os
import logging
from typing import Dict, List, Optional
from openai import OpenAI

logger = logging.getLogger(__name__)

class ResumeAnalyzer:
    """AI-powered resume analyzer using OpenAI API"""
    
    def __init__(self):
        self.openai_client = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY", "your-openai-api-key")
        )
    
    def analyze_resume(self, resume_text: str, job_description: str = None) -> Dict:
        """Analyze resume content and provide scoring and recommendations"""
        try:
            # Prepare the analysis prompt
            if job_description:
                prompt = f"""
                Analyze the following resume against the job description and provide a comprehensive analysis.
                
                RESUME:
                {resume_text}
                
                JOB DESCRIPTION:
                {job_description}
                
                Please provide analysis in JSON format with the following structure:
                {{
                    "overall_score": number (0-100),
                    "skills_match_score": number (0-100),
                    "experience_match_score": number (0-100),
                    "education_match_score": number (0-100),
                    "strengths": ["list of strengths"],
                    "weaknesses": ["list of areas for improvement"],
                    "missing_skills": ["list of skills missing from resume"],
                    "recommendations": ["list of specific recommendations"],
                    "keywords_found": ["list of relevant keywords found"],
                    "keywords_missing": ["list of important keywords missing"],
                    "ats_compatibility": number (0-100),
                    "summary": "brief summary of the analysis"
                }}
                """
            else:
                prompt = f"""
                Analyze the following resume and provide a comprehensive analysis focusing on overall quality, structure, and content.
                
                RESUME:
                {resume_text}
                
                Please provide analysis in JSON format with the following structure:
                {{
                    "overall_score": number (0-100),
                    "content_quality_score": number (0-100),
                    "structure_score": number (0-100),
                    "completeness_score": number (0-100),
                    "strengths": ["list of strengths"],
                    "weaknesses": ["list of areas for improvement"],
                    "recommendations": ["list of specific recommendations"],
                    "missing_sections": ["list of missing resume sections"],
                    "ats_compatibility": number (0-100),
                    "summary": "brief summary of the analysis"
                }}
                """
            
            # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
            # do not change this unless explicitly requested by the user
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert HR professional and resume analyst. Provide detailed, actionable feedback to help improve resumes and job match compatibility."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                response_format={"type": "json_object"},
                temperature=0.3
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
            
        except Exception as e:
            logger.error(f"Error analyzing resume: {str(e)}")
            raise Exception(f"Failed to analyze resume: {str(e)}")
    
    def extract_skills(self, resume_text: str) -> List[str]:
        """Extract skills from resume text"""
        try:
            prompt = f"""
            Extract all technical skills, soft skills, and competencies from the following resume text.
            
            RESUME:
            {resume_text}
            
            Please provide the skills in JSON format:
            {{
                "technical_skills": ["list of technical skills"],
                "soft_skills": ["list of soft skills"],
                "certifications": ["list of certifications"],
                "tools_and_technologies": ["list of tools and technologies"]
            }}
            """
            
            # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
            # do not change this unless explicitly requested by the user
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert at extracting and categorizing skills from resumes."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                response_format={"type": "json_object"},
                temperature=0.1
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
            
        except Exception as e:
            logger.error(f"Error extracting skills: {str(e)}")
            return {"technical_skills": [], "soft_skills": [], "certifications": [], "tools_and_technologies": []}
    
    def calculate_job_match_score(self, resume_text: str, job_description: str) -> Dict:
        """Calculate compatibility score between resume and job"""
        try:
            prompt = f"""
            Calculate the compatibility score between the following resume and job description.
            
            RESUME:
            {resume_text}
            
            JOB DESCRIPTION:
            {job_description}
            
            Please provide the match analysis in JSON format:
            {{
                "match_score": number (0-100),
                "skill_overlap": number (0-100),
                "experience_relevance": number (0-100),
                "education_fit": number (0-100),
                "cultural_fit_indicators": number (0-100),
                "matching_keywords": ["list of matching keywords"],
                "gap_analysis": ["list of gaps or missing requirements"],
                "recommendation": "overall recommendation (Strong Match/Good Match/Potential Match/Poor Match)"
            }}
            """
            
            # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
            # do not change this unless explicitly requested by the user
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert recruiter analyzing job-candidate compatibility."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                response_format={"type": "json_object"},
                temperature=0.2
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
            
        except Exception as e:
            logger.error(f"Error calculating job match: {str(e)}")
            raise Exception(f"Failed to calculate job match score: {str(e)}")
    
    def generate_improvement_suggestions(self, analysis_result: Dict) -> List[str]:
        """Generate specific improvement suggestions based on analysis"""
        suggestions = []
        
        if 'recommendations' in analysis_result:
            suggestions.extend(analysis_result['recommendations'])
        
        if 'missing_skills' in analysis_result and analysis_result['missing_skills']:
            suggestions.append(f"Consider acquiring these skills: {', '.join(analysis_result['missing_skills'][:5])}")
        
        if 'ats_compatibility' in analysis_result and analysis_result['ats_compatibility'] < 70:
            suggestions.append("Improve ATS compatibility by using standard section headings and including more relevant keywords")
        
        return suggestions

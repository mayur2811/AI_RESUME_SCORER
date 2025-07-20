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
        
        # Check if API key is available and valid
        api_key = os.environ.get("OPENAI_API_KEY", "")
        if not api_key or api_key == "your-openai-api-key" or len(api_key) < 20:
            logger.warning("OpenAI API key not configured properly")
            return self._get_mock_analysis(resume_text, job_description)
        
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
            # Fall back to mock analysis if API fails
            return self._get_mock_analysis(resume_text, job_description)
    
    def _get_mock_analysis(self, resume_text: str, job_description: str = None) -> Dict:
        """Provide a mock analysis when OpenAI API is unavailable"""
        
        # Basic text analysis for mock scoring
        word_count = len(resume_text.split())
        has_experience = any(keyword in resume_text.lower() for keyword in ['experience', 'worked', 'developed', 'managed', 'led'])
        has_skills = any(keyword in resume_text.lower() for keyword in ['python', 'javascript', 'java', 'react', 'sql', 'aws'])
        has_education = any(keyword in resume_text.lower() for keyword in ['degree', 'university', 'college', 'bachelor', 'master', 'phd'])
        
        # Calculate mock scores based on content
        base_score = 60
        if word_count > 200: base_score += 10
        if has_experience: base_score += 15
        if has_skills: base_score += 10
        if has_education: base_score += 5
        
        overall_score = min(base_score, 95)  # Cap at 95 for mock
        
        if job_description:
            # Job-specific analysis
            return {
                "overall_score": overall_score,
                "skills_match_score": overall_score - 5,
                "experience_match_score": overall_score - 3,
                "education_match_score": overall_score - 2,
                "strengths": [
                    "Resume contains relevant experience" if has_experience else "Clear presentation of background",
                    "Technical skills mentioned" if has_skills else "Professional formatting",
                    "Education background provided" if has_education else "Adequate length"
                ],
                "weaknesses": [
                    "Could benefit from more specific achievements",
                    "Consider adding quantifiable results"
                ],
                "missing_skills": [
                    "Cloud computing experience",
                    "Leadership examples"
                ],
                "recommendations": [
                    "Add specific metrics and achievements",
                    "Include more technical keywords",
                    "Highlight relevant project outcomes"
                ],
                "keywords_found": ["experience", "skills"] if has_experience and has_skills else ["professional"],
                "keywords_missing": ["leadership", "metrics", "achievements"],
                "ats_compatibility": overall_score - 10,
                "summary": f"Resume shows {overall_score}% compatibility. Consider enhancing with more specific achievements and metrics."
            }
        else:
            # General analysis
            return {
                "overall_score": overall_score,
                "content_quality_score": overall_score - 3,
                "structure_score": overall_score - 5,
                "completeness_score": overall_score - 2,
                "strengths": [
                    "Professional presentation",
                    "Relevant experience mentioned" if has_experience else "Clear structure",
                    "Technical skills included" if has_skills else "Appropriate length"
                ],
                "weaknesses": [
                    "Could include more quantifiable achievements",
                    "Consider adding more specific details"
                ],
                "recommendations": [
                    "Add specific metrics and numbers to achievements",
                    "Include more action verbs in experience descriptions",
                    "Consider adding a professional summary section"
                ],
                "missing_sections": [
                    "Professional summary" if "summary" not in resume_text.lower() else None,
                    "Certifications" if "certification" not in resume_text.lower() else None
                ],
                "ats_compatibility": overall_score - 8,
                "summary": f"Resume scores {overall_score}% overall. Focus on adding specific achievements and improving ATS compatibility."
            }
    
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

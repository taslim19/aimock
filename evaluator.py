"""
Answer Evaluator Module
Evaluates user answers using rule-based scoring and NLP techniques
"""

import re
import json
from collections import Counter


class AnswerEvaluator:
    """Evaluates interview answers based on multiple criteria"""
    
    def __init__(self):
        self.quality_indicators = {
            'positive': [
                'experience', 'implemented', 'successful', 'achieved', 'improved',
                'solved', 'developed', 'managed', 'led', 'collaborated', 'optimized',
                'analyzed', 'designed', 'delivered', 'exceeded', 'enhanced'
            ],
            'negative': [
                'didn\'t', 'couldn\'t', 'failed', 'unable', 'lack', 'limited',
                'struggled', 'difficult', 'problem', 'issue', 'challenge'
            ],
            'technical': [
                'algorithm', 'architecture', 'framework', 'methodology', 'pattern',
                'optimization', 'scalability', 'performance', 'security', 'database',
                'api', 'microservice', 'deployment', 'testing', 'debugging'
            ],
            'communication': [
                'clearly', 'effectively', 'communicated', 'explained', 'presented',
                'discussed', 'collaborated', 'coordinated', 'aligned', 'understood'
            ]
        }
        
        self.minimum_length = 20  # Minimum characters for a good answer
        self.ideal_length = 100   # Ideal answer length
    
    def evaluate_answer(self, answer_text, question_text, difficulty='medium'):
        """Evaluate an answer and return scores and feedback"""
        if not answer_text or len(answer_text.strip()) < 10:
            return self._generate_failed_evaluation("Answer is too short or empty.")
        
        answer_lower = answer_text.lower()
        answer_length = len(answer_text)
        
        # Calculate individual scores
        clarity_score = self._evaluate_clarity(answer_text, answer_length)
        accuracy_score = self._evaluate_accuracy(answer_text, question_text, difficulty)
        communication_score = self._evaluate_communication(answer_text, answer_lower)
        confidence_score = self._evaluate_confidence(answer_text, answer_lower)
        
        # Calculate overall score (weighted average)
        overall_score = (
            clarity_score * 0.25 +
            accuracy_score * 0.30 +
            communication_score * 0.25 +
            confidence_score * 0.20
        )
        
        # Generate feedback
        feedback = self._generate_feedback(
            clarity_score, accuracy_score, communication_score, 
            confidence_score, overall_score, answer_text, answer_length
        )
        
        # Identify strengths and improvements
        strengths = self._identify_strengths(
            clarity_score, accuracy_score, communication_score, confidence_score, answer_lower
        )
        improvements = self._identify_improvements(
            clarity_score, accuracy_score, communication_score, confidence_score, answer_length
        )
        
        return {
            'clarity': round(clarity_score, 2),
            'accuracy': round(accuracy_score, 2),
            'communication': round(communication_score, 2),
            'confidence': round(confidence_score, 2),
            'overall': round(overall_score, 2),
            'feedback': feedback,
            'strengths': strengths,
            'improvements': improvements
        }
    
    def _evaluate_clarity(self, answer_text, answer_length):
        """Evaluate clarity of the answer"""
        score = 50.0  # Base score
        
        # Length check
        if answer_length >= self.minimum_length:
            score += 20
        if self.minimum_length <= answer_length <= self.ideal_length * 2:
            score += 10
        
        # Sentence structure
        sentences = re.split(r'[.!?]+', answer_text)
        if len(sentences) > 1:
            score += 10
        
        # Check for proper punctuation
        if any(punct in answer_text for punct in ['.', '!', '?']):
            score += 5
        
        # Check for capitalization
        if answer_text[0].isupper():
            score += 5
        
        return min(score, 100.0)
    
    def _evaluate_accuracy(self, answer_text, question_text, difficulty):
        """Evaluate accuracy and relevance of the answer"""
        score = 40.0  # Base score
        
        answer_lower = answer_text.lower()
        question_lower = question_text.lower()
        
        # Extract key terms from question
        question_keywords = self._extract_keywords(question_text)
        answer_keywords = self._extract_keywords(answer_text)
        
        # Check keyword overlap
        overlap = len(set(question_keywords) & set(answer_keywords))
        if overlap > 0:
            score += min(overlap * 10, 30)
        
        # Check for technical terms (for technical questions)
        if any(word in question_lower for word in ['explain', 'what is', 'difference', 'how']):
            technical_count = sum(1 for word in self.quality_indicators['technical'] 
                                if word in answer_lower)
            score += min(technical_count * 5, 20)
        
        # Check for specific examples or details
        if any(word in answer_lower for word in ['example', 'instance', 'case', 'time when']):
            score += 10
        
        # Difficulty adjustment
        if difficulty == 'hard':
            score *= 0.9  # Slightly lower for hard questions
        elif difficulty == 'easy':
            score *= 1.1  # Slightly higher for easy questions
        
        return min(score, 100.0)
    
    def _evaluate_communication(self, answer_text, answer_lower):
        """Evaluate communication quality"""
        score = 50.0  # Base score
        
        # Check for communication-related keywords
        comm_keywords = sum(1 for word in self.quality_indicators['communication'] 
                          if word in answer_lower)
        score += min(comm_keywords * 8, 20)
        
        # Check for structure indicators
        structure_words = ['first', 'second', 'then', 'finally', 'additionally', 'however', 'therefore']
        structure_count = sum(1 for word in structure_words if word in answer_lower)
        score += min(structure_count * 5, 15)
        
        # Check for positive language
        positive_count = sum(1 for word in self.quality_indicators['positive'] 
                           if word in answer_lower)
        score += min(positive_count * 3, 15)
        
        return min(score, 100.0)
    
    def _evaluate_confidence(self, answer_text, answer_lower):
        """Evaluate confidence level in the answer"""
        score = 50.0  # Base score
        
        # Check for confident language
        confident_phrases = [
            'i am confident', 'i believe', 'i know', 'i have experience',
            'i successfully', 'i achieved', 'i implemented', 'i led'
        ]
        confident_count = sum(1 for phrase in confident_phrases if phrase in answer_lower)
        score += min(confident_count * 10, 30)
        
        # Check for hedging language (reduces confidence)
        hedging_phrases = ['maybe', 'perhaps', 'i think', 'i guess', 'not sure', 'uncertain']
        hedging_count = sum(1 for phrase in hedging_phrases if phrase in answer_lower)
        score -= min(hedging_count * 5, 20)
        
        # Check for specific examples (shows confidence through experience)
        if any(word in answer_lower for word in ['when i', 'in my experience', 'i have']):
            score += 10
        
        # Check for negative language
        negative_count = sum(1 for word in self.quality_indicators['negative'] 
                           if word in answer_lower)
        score -= min(negative_count * 3, 15)
        
        return max(min(score, 100.0), 0.0)
    
    def _extract_keywords(self, text):
        """Extract important keywords from text"""
        # Remove common stop words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 
                     'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were',
                     'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did',
                     'will', 'would', 'should', 'could', 'may', 'might', 'must',
                     'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they'}
        
        words = re.findall(r'\b\w+\b', text.lower())
        keywords = [w for w in words if w not in stop_words and len(w) > 3]
        
        return keywords[:10]  # Return top 10 keywords
    
    def _generate_feedback(self, clarity, accuracy, communication, confidence, overall, answer_text, length):
        """Generate detailed feedback"""
        feedback_parts = []
        
        # Overall assessment
        if overall >= 80:
            feedback_parts.append("Excellent answer! You demonstrated strong understanding and communication skills.")
        elif overall >= 65:
            feedback_parts.append("Good answer with room for improvement in some areas.")
        elif overall >= 50:
            feedback_parts.append("Adequate answer, but consider providing more detail and structure.")
        else:
            feedback_parts.append("Your answer needs significant improvement. Focus on clarity and providing specific examples.")
        
        # Specific feedback
        if clarity < 60:
            feedback_parts.append("Work on making your answer clearer and more structured. Use complete sentences and proper punctuation.")
        elif clarity >= 80:
            feedback_parts.append("Your answer was clear and well-structured.")
        
        if accuracy < 60:
            feedback_parts.append("Try to be more specific and relevant to the question. Include relevant examples or details.")
        elif accuracy >= 80:
            feedback_parts.append("Your answer was accurate and directly addressed the question.")
        
        if communication < 60:
            feedback_parts.append("Improve your communication by using transition words and organizing your thoughts better.")
        elif communication >= 80:
            feedback_parts.append("You communicated your ideas effectively.")
        
        if confidence < 60:
            feedback_parts.append("Be more confident in your responses. Avoid hedging language and provide concrete examples from your experience.")
        elif confidence >= 80:
            feedback_parts.append("You demonstrated confidence in your knowledge and experience.")
        
        # Length feedback
        if length < self.minimum_length:
            feedback_parts.append(f"Your answer is too short. Aim for at least {self.minimum_length} characters to provide a comprehensive response.")
        elif length > self.ideal_length * 3:
            feedback_parts.append("Your answer is quite long. Consider being more concise while maintaining key points.")
        
        return " ".join(feedback_parts)
    
    def _identify_strengths(self, clarity, accuracy, communication, confidence, answer_lower):
        """Identify strengths in the answer"""
        strengths = []
        
        if clarity >= 70:
            strengths.append("Clear and well-structured response")
        if accuracy >= 70:
            strengths.append("Accurate and relevant information")
        if communication >= 70:
            strengths.append("Effective communication")
        if confidence >= 70:
            strengths.append("Confident expression")
        
        if any(word in answer_lower for word in ['example', 'instance', 'experience']):
            strengths.append("Used specific examples")
        
        if any(word in answer_lower for word in self.quality_indicators['technical']):
            strengths.append("Demonstrated technical knowledge")
        
        if not strengths:
            strengths.append("Attempted to answer the question")
        
        return strengths
    
    def _identify_improvements(self, clarity, accuracy, communication, confidence, length):
        """Identify areas for improvement"""
        improvements = []
        
        if clarity < 70:
            improvements.append("Improve clarity and structure of your response")
        if accuracy < 70:
            improvements.append("Provide more accurate and relevant information")
        if communication < 70:
            improvements.append("Enhance communication skills and organization")
        if confidence < 70:
            improvements.append("Build confidence in your responses")
        
        if length < self.minimum_length:
            improvements.append("Provide more detailed answers")
        elif length > self.ideal_length * 3:
            improvements.append("Be more concise while maintaining key points")
        
        if not improvements:
            improvements.append("Continue practicing to maintain your strong performance")
        
        return improvements
    
    def _generate_failed_evaluation(self, reason):
        """Generate evaluation for failed/invalid answers"""
        return {
            'clarity': 0.0,
            'accuracy': 0.0,
            'communication': 0.0,
            'confidence': 0.0,
            'overall': 0.0,
            'feedback': reason,
            'strengths': [],
            'improvements': ['Provide a complete answer to the question']
        }


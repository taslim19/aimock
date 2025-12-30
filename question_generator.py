"""
AI Question Generator Module
Generates interview questions using NLP (spaCy) and domain knowledge
"""

import random
import json
import re
try:
    import spacy
    SPACY_AVAILABLE = True
except ImportError:
    SPACY_AVAILABLE = False


class QuestionGenerator:
    """Generates interview questions using NLP (spaCy) and domain knowledge"""
    
    def __init__(self):
        # Load spaCy model if available (try models with word vectors first)
        self.nlp = None
        self.spacy_available = False
        
        if SPACY_AVAILABLE:
            models_to_try = ["en_core_web_md", "en_core_web_lg", "en_core_web_sm"]
            for model_name in models_to_try:
                try:
                    self.nlp = spacy.load(model_name)
                    self.spacy_available = True
                    break
                except OSError:
                    continue
        
        self.domain_knowledge = self._load_domain_knowledge()
        self.question_templates = self._load_question_templates()
    
    def _load_domain_knowledge(self):
        """Load domain-specific knowledge base"""
        return {
            'IT/Software Engineering': {
                'topics': [
                    'Object-Oriented Programming', 'Data Structures', 'Algorithms',
                    'Database Design', 'RESTful APIs', 'Microservices Architecture',
                    'Cloud Computing', 'DevOps', 'Software Testing', 'Version Control',
                    'Design Patterns', 'System Design', 'Security', 'Performance Optimization'
                ],
                'concepts': {
                    'OOP': ['Encapsulation', 'Inheritance', 'Polymorphism', 'Abstraction'],
                    'Data Structures': ['Arrays', 'Linked Lists', 'Stacks', 'Queues', 'Trees', 'Graphs'],
                    'Algorithms': ['Sorting', 'Searching', 'Dynamic Programming', 'Greedy Algorithms'],
                    'Databases': ['SQL', 'NoSQL', 'ACID Properties', 'Normalization', 'Indexing']
                },
                'technologies': ['Python', 'Java', 'JavaScript', 'React', 'Node.js', 'Docker', 'Kubernetes']
            },
            'HR/Human Resources': {
                'topics': [
                    'Teamwork', 'Leadership', 'Problem Solving', 'Communication',
                    'Time Management', 'Conflict Resolution', 'Adaptability', 'Work Ethics'
                ],
                'situations': [
                    'worked under pressure', 'handled a difficult situation',
                    'led a team project', 'resolved a conflict', 'learned a new skill',
                    'made a mistake', 'achieved a goal', 'worked with a difficult colleague'
                ],
                'challenges': [
                    'tight deadlines', 'conflicting priorities', 'team disagreements',
                    'unclear requirements', 'resource constraints'
                ]
            },
            'Finance': {
                'topics': [
                    'Financial Analysis', 'Investment Banking', 'Risk Management',
                    'Accounting Principles', 'Financial Modeling', 'Market Analysis',
                    'Portfolio Management', 'Corporate Finance'
                ],
                'concepts': {
                    'Analysis': ['DCF', 'NPV', 'IRR', 'ROI', 'Financial Ratios'],
                    'Markets': ['Stock Market', 'Bond Market', 'Derivatives', 'Forex'],
                    'Tools': ['Excel', 'Bloomberg', 'Financial Statements', 'Valuation Models']
                },
                'scenarios': [
                    'company valuation', 'investment decision', 'risk assessment',
                    'market trend analysis', 'financial planning'
                ]
            },
            'Management': {
                'topics': [
                    'Leadership', 'Strategic Planning', 'Team Management',
                    'Change Management', 'Decision Making', 'Performance Management'
                ],
                'situations': [
                    'leading a team', 'managing a project', 'handling underperformance',
                    'implementing change', 'making strategic decisions'
                ],
                'styles': [
                    'Transformational', 'Transactional', 'Servant Leadership',
                    'Democratic', 'Autocratic'
                ]
            }
        }
    
    def _load_question_templates(self):
        """Load question templates for different domains"""
        return {
            'IT/Software Engineering': [
                "Explain {topic} and its importance in software development.",
                "What is the difference between {concept1} and {concept2}?",
                "How would you design a system to handle {scenario}?",
                "Describe your experience with {technology}. What challenges did you face?",
                "What are the best practices for implementing {topic}?",
                "How would you optimize a {component} for better performance?",
                "Explain the trade-offs between {option1} and {option2}.",
                "How do you ensure code quality when working with {technology}?",
                "Describe a time when you had to debug a complex issue related to {topic}.",
                "What security considerations should be taken when working with {technology}?"
            ],
            'HR/Human Resources': [
                "Tell me about yourself and your professional background.",
                "Describe a time when you {situation}. What was the outcome?",
                "How do you handle {challenge} in the workplace?",
                "What are your greatest strengths and how do they help you in your role?",
                "Can you share an example of a weakness you've worked on improving?",
                "Why are you interested in this position and our company?",
                "How do you prioritize tasks when you have multiple deadlines?",
                "Describe a situation where you had to work with a difficult team member.",
                "How do you stay motivated during challenging projects?",
                "Where do you see yourself in 5 years?"
            ],
            'Finance': [
                "Explain {concept} and its application in financial analysis.",
                "How would you analyze {scenario} from a financial perspective?",
                "What factors would you consider when evaluating {investment_type}?",
                "Describe your experience with {tool} and how you've used it in analysis.",
                "How do you assess the financial health of a company?",
                "Explain the impact of {event} on financial markets.",
                "What is your approach to risk management in {context}?",
                "How would you present financial data to non-financial stakeholders?",
                "Describe a time when your financial analysis led to an important decision.",
                "What trends do you see in the current financial market?"
            ],
            'Management': [
                "How do you motivate and inspire your team members?",
                "Describe a time when you had to make a difficult decision as a manager.",
                "How do you handle conflict within your team?",
                "What is your leadership style and how has it evolved?",
                "How do you prioritize tasks and manage your team's workload?",
                "Describe a situation where you had to manage an underperforming team member.",
                "How do you ensure effective communication within your team?",
                "What strategies do you use for change management?",
                "How do you balance the needs of your team with organizational goals?",
                "Describe your approach to developing and mentoring team members."
            ]
        }
    
    def generate_questions(self, domain, num_questions=5, difficulty='medium'):
        """Generate interview questions for a given domain"""
        if domain not in self.domain_knowledge:
            domain = 'IT/Software Engineering'  # Default domain
        
        knowledge = self.domain_knowledge[domain]
        templates = self.question_templates.get(domain, [])
        
        questions = []
        used_templates = set()
        
        for i in range(num_questions):
            # Select a random template
            available_templates = [t for t in templates if t not in used_templates]
            if not available_templates:
                available_templates = templates
                used_templates.clear()
            
            template = random.choice(available_templates)
            used_templates.add(template)
            
            # Fill in the template with domain-specific content
            question_text = self._fill_template(template, domain, knowledge, difficulty)
            
            # Determine question type
            question_type = self._determine_question_type(template, domain)
            
            questions.append({
                'text': question_text,
                'type': question_type,
                'difficulty': difficulty,
                'domain': domain
            })
        
        return questions
    
    def _fill_template(self, template, domain, knowledge, difficulty):
        """Fill question template with appropriate content"""
        question = template
        
        # Replace placeholders based on domain
        if domain == 'IT/Software Engineering':
            if '{topic}' in template:
                question = question.replace('{topic}', random.choice(knowledge['topics']))
            elif '{concept1}' in template and '{concept2}' in template:
                concept_pair = random.choice(list(knowledge['concepts'].values()))
                if len(concept_pair) >= 2:
                    concepts = random.sample(concept_pair, 2)
                    question = question.replace('{concept1}', concepts[0])
                    question = question.replace('{concept2}', concepts[1])
            elif '{technology}' in template:
                question = question.replace('{technology}', random.choice(knowledge['technologies']))
            elif '{scenario}' in template:
                scenarios = ['high traffic', 'data consistency', 'scalability', 'security']
                question = question.replace('{scenario}', random.choice(scenarios))
            elif '{component}' in template:
                components = ['database query', 'API endpoint', 'frontend component', 'algorithm']
                question = question.replace('{component}', random.choice(components))
            elif '{option1}' in template and '{option2}' in template:
                options = [
                    ('SQL', 'NoSQL'),
                    ('Monolithic', 'Microservices'),
                    ('Synchronous', 'Asynchronous'),
                    ('Caching', 'Database queries')
                ]
                opt1, opt2 = random.choice(options)
                question = question.replace('{option1}', opt1)
                question = question.replace('{option2}', opt2)
        
        elif domain == 'HR/Human Resources':
            if '{situation}' in template:
                question = question.replace('{situation}', random.choice(knowledge['situations']))
            elif '{challenge}' in template:
                question = question.replace('{challenge}', random.choice(knowledge['challenges']))
        
        elif domain == 'Finance':
            if '{concept}' in template:
                all_concepts = []
                for concept_list in knowledge['concepts'].values():
                    all_concepts.extend(concept_list)
                if all_concepts:
                    question = question.replace('{concept}', random.choice(all_concepts))
            elif '{scenario}' in template:
                question = question.replace('{scenario}', random.choice(knowledge['scenarios']))
            elif '{investment_type}' in template:
                investments = ['stocks', 'bonds', 'real estate', 'startups', 'mutual funds']
                question = question.replace('{investment_type}', random.choice(investments))
            elif '{tool}' in template:
                question = question.replace('{tool}', random.choice(knowledge['concepts']['Tools']))
            elif '{event}' in template:
                events = ['interest rate changes', 'market volatility', 'economic recession', 'regulatory changes']
                question = question.replace('{event}', random.choice(events))
            elif '{context}' in template:
                contexts = ['portfolio management', 'corporate finance', 'investment banking']
                question = question.replace('{context}', random.choice(contexts))
        
        elif domain == 'Management':
            if '{situation}' in template:
                question = question.replace('{situation}', random.choice(knowledge['situations']))
        
        return question
    
    def _determine_question_type(self, template, domain):
        """Determine the type of question"""
        template_lower = template.lower()
        
        if any(word in template_lower for word in ['describe', 'tell me', 'share', 'time when']):
            return 'behavioral'
        elif any(word in template_lower for word in ['how would', 'how do', 'what would']):
            return 'situational'
        elif any(word in template_lower for word in ['explain', 'what is', 'difference between']):
            return 'technical'
        else:
            return 'general'


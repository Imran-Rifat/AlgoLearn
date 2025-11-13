import openai
import json
import os
from typing import List, Dict, Any


class OpenAIService:
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.model = os.getenv('OPENAI_MODEL', 'gpt-4')

    def check_connection(self):
        """Check if OpenAI API is accessible"""
        try:
            self.client.models.list()
            return True
        except:
            return False

    def generate_concept_explanation(self, chapter_name: str, topics: List[str],
                                     difficulty: str, language: str) -> Dict[str, Any]:
        """Generate comprehensive concept explanation using OpenAI"""

        prompt = f"""
        You are an expert computer science educator specializing in data structures and algorithms.
        Create a comprehensive learning module for "{chapter_name}" focusing on {difficulty} level learners.
        Primary topics to cover: {', '.join(topics)}
        Programming language: {language}

        Generate a structured learning module with:

        THEORY SECTION:
        - Core concepts with real-world analogies
        - Key operations and their implementations
        - Time and space complexity analysis
        - Common use cases and applications

        PRACTICAL SECTION:
        - Step-by-step implementation guide in {language}
        - Code examples with detailed explanations
        - Common pitfalls and best practices

        EXERCISES:
        - 3 practice problems with increasing difficulty
        - Sample inputs and expected outputs
        - Hints for each problem

        Format the response as JSON with these keys:
        - title: Module title
        - overview: Brief description
        - learning_objectives: Array of 4-5 key objectives
        - theory_content: Detailed HTML-formatted theory
        - code_examples: Array of dicts with 'code', 'explanation', 'complexity'
        - practice_problems: Array of dicts with 'problem', 'hint', 'solution_approach'
        - key_takeaways: Array of main points
        - estimated_duration: Estimated study time

        Make it engaging, practical, and suitable for {difficulty} level.
        """

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system",
                     "content": "You are a expert DSA educator creating comprehensive learning materials."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=4000,
                response_format={"type": "json_object"}
            )

            content = response.choices[0].message.content
            return json.loads(content)

        except Exception as e:
            return self._get_fallback_concept(chapter_name, language, difficulty)

    def generate_practice_question(self, chapter_name: str, topics: List[str],
                                   level: int, language: str) -> Dict[str, Any]:
        """Generate practice question using OpenAI"""

        difficulty_map = {
            1: "beginner", 2: "beginner", 3: "easy",
            4: "easy", 5: "medium", 6: "medium",
            7: "hard", 8: "hard", 9: "expert", 10: "expert"
        }

        difficulty = difficulty_map.get(level, "medium")

        prompt = f"""
        Create a {difficulty} level coding problem about {chapter_name} for {language} programmers.
        Focus on: {', '.join(topics[:2])}
        Difficulty level: {level}/10

        Requirements:
        - Problem should test fundamental DSA concepts
        - Include clear problem statement with examples
        - Provide 3-5 test cases with inputs and expected outputs
        - Include constraints and edge cases
        - Solution should be implementable in 15-40 lines of {language} code
        - Include hints that gradually reveal the solution

        Format as JSON with:
        - problem_id: Unique identifier
        - title: Problem title
        - description: Detailed problem statement
        - difficulty: {difficulty}
        - constraints: Array of constraints
        - examples: Array of dicts with 'input', 'output', 'explanation'
        - hints: Array of 3 hints (general to specific)
        - function_signature: Function signature in {language}
        - test_cases: Array of dicts with 'input', 'expected_output'
        - topics: Array of relevant topics

        Make it practical and interview-relevant.
        """

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You create high-quality coding problems for technical interviews."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=3000,
                response_format={"type": "json_object"}
            )

            content = response.choices[0].message.content
            question_data = json.loads(content)
            question_data['generated_level'] = level
            return question_data

        except Exception as e:
            return self._get_fallback_question(chapter_name, language, level)

    def analyze_code(self, user_code: str, question_description: str,
                     test_cases: List[Dict], language: str) -> Dict[str, Any]:
        """Analyze user's code solution using OpenAI"""

        prompt = f"""
        Analyze this {language} code solution:

        PROBLEM:
        {question_description}

        USER'S CODE:
        ```{language}
        {user_code}
        ```

        TEST CASES:
        {json.dumps(test_cases, indent=2)}

        Provide comprehensive analysis as JSON with:

        - correctness_score: 0-100
        - is_correct: boolean
        - feedback: Detailed analysis of the solution
        - strengths: Array of what's done well
        - improvements: Array of specific improvements needed
        - efficiency_analysis: Time and space complexity assessment
        - alternative_approaches: Array of other possible solutions
        - code_quality: Assessment of readability and best practices
        - bugs: Array of any bugs or edge case issues
        - suggested_optimizations: Array of optimization suggestions

        Be constructive, specific, and focus on learning.
        Highlight both what's good and what can be improved.
        """

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a expert code reviewer providing constructive feedback."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=2000,
                response_format={"type": "json_object"}
            )

            content = response.choices[0].message.content
            return json.loads(content)

        except Exception as e:
            return self._get_fallback_analysis()

    def generate_recommendation(self, completed_chapters: List[Dict],
                                performance: Dict, language: str) -> Dict[str, Any]:
        """Generate personalized learning recommendations"""

        prompt = f"""
        Based on the following learning progress, recommend next steps:

        COMPLETED CHAPTERS:
        {json.dumps(completed_chapters, indent=2)}

        PERFORMANCE SUMMARY:
        {json.dumps(performance, indent=2)}

        TARGET LANGUAGE: {language}

        Provide personalized learning recommendations as JSON with:

        - next_chapter: Recommended chapter to study next
        - reason: Why this recommendation
        - preparation_required: Any prerequisite review needed
        - estimated_difficulty: Easy/Medium/Hard for this user
        - practice_focus: Specific topics to practice
        - learning_path: Array of suggested next 3 chapters
        - confidence_score: 0-100 how confident in this recommendation
        - alternative_options: Other good options to consider

        Base recommendations on:
        1. Logical learning progression in DSA
        2. User's performance patterns
        3. Industry interview requirements
        4. Foundational knowledge building
        """

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a learning path advisor for computer science education."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=1500,
                response_format={"type": "json_object"}
            )

            content = response.choices[0].message.content
            return json.loads(content)

        except Exception as e:
            return self._get_fallback_recommendation()

    def _get_fallback_concept(self, chapter_name: str, language: str, difficulty: str) -> Dict[str, Any]:
        """Fallback concept explanation when OpenAI fails"""
        return {
            "title": f"{chapter_name} - {difficulty.title()} Concepts",
            "overview": f"Learn fundamental {chapter_name} concepts in {language}",
            "learning_objectives": [
                f"Understand basic {chapter_name} operations",
                f"Implement {chapter_name} in {language}",
                f"Analyze time and space complexity",
                "Solve practice problems"
            ],
            "theory_content": f"<p>Comprehensive {chapter_name} explanation would be generated here.</p>",
            "code_examples": [],
            "practice_problems": [],
            "key_takeaways": ["Master core concepts", "Practice implementation", "Understand complexity"],
            "estimated_duration": "2-3 hours"
        }

    def _get_fallback_question(self, chapter_name: str, language: str, level: int) -> Dict[str, Any]:
        """Fallback question when OpenAI fails"""
        return {
            "problem_id": f"fallback_{chapter_name.lower().replace(' ', '_')}_{level}",
            "title": f"Basic {chapter_name} Problem",
            "description": f"Implement a basic {chapter_name} operation in {language}",
            "difficulty": "medium",
            "constraints": ["Time complexity: O(n)", "Space complexity: O(1)"],
            "examples": [{"input": "Sample input", "output": "Sample output", "explanation": "Sample explanation"}],
            "hints": ["Think about the core operations", "Consider edge cases", "Optimize your solution"],
            "function_signature": f"def solution(input):",
            "test_cases": [{"input": "test", "expected_output": "result"}],
            "topics": [chapter_name],
            "generated_level": level
        }

    def _get_fallback_analysis(self) -> Dict[str, Any]:
        """Fallback analysis when OpenAI fails"""
        return {
            "correctness_score": 0,
            "is_correct": False,
            "feedback": "Analysis service temporarily unavailable. Please check your code manually.",
            "strengths": [],
            "improvements": ["Service unavailable - try again later"],
            "efficiency_analysis": "Unable to analyze",
            "alternative_approaches": [],
            "code_quality": "Unable to assess",
            "bugs": ["Analysis service down"],
            "suggested_optimizations": []
        }

    def _get_fallback_recommendation(self) -> Dict[str, Any]:
        """Fallback recommendation when OpenAI fails"""
        return {
            "next_chapter": "Arrays & Strings",
            "reason": "Foundational chapter for all DSA topics",
            "preparation_required": "Basic programming knowledge",
            "estimated_difficulty": "Easy",
            "practice_focus": ["Array manipulation", "String operations"],
            "learning_path": ["Arrays & Strings", "Linked Lists", "Stacks & Queues"],
            "confidence_score": 80,
            "alternative_options": ["Linked Lists", "Complexity Analysis"]
        }
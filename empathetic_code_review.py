import json
import re
import os
from dotenv import load_dotenv
load_dotenv()  # Load variables from .env into environment
from typing import Dict, List, Any
import requests

class EmpatheticCodeReviewer:
    def __init__(self):
            self.api_key = os.getenv("OPENAI_API_KEY")
            self.api_url = os.getenv("OPENAI_API_URL")
        
    def call_gemini_api(self, prompt: str) -> str:
        """
        Calls the Google Gemini API with the given prompt and returns the response.
        """
        headers = {
            "Content-Type": "application/json",
        }
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 2000,
            }
        }
        
        try:
            response = requests.post(
                f"{self.api_url}?key={self.api_key}", 
                headers=headers, 
                json=payload
            )
            response.raise_for_status()
            
            # Extract the response text from Gemini API
            response_data = response.json()
            if "candidates" in response_data and len(response_data["candidates"]) > 0:
                if "content" in response_data["candidates"][0]:
                    parts = response_data["candidates"][0]["content"].get("parts", [])
                    if parts and "text" in parts[0]:
                        return parts[0]["text"]
            
            return "Error: Could not extract response from Gemini API"
            
        except requests.exceptions.RequestException as e:
            return f"Error calling Gemini API: {str(e)}"
    
    def analyze_severity(self, comment: str) -> str:
        """
        Analyzes the severity of a comment to adjust tone accordingly.
        Returns: 'low', 'medium', or 'high'
        """
        negative_words = ["terrible", "awful", "horrible", "never", "always", "wrong", "bad", "inefficient", "stupid", "dumb"]
        intense_words = ["terrible", "awful", "horrible", "never", "always"]
        
        comment_lower = comment.lower()
        negative_count = sum(1 for word in negative_words if word in comment_lower)
        intense_count = sum(1 for word in intense_words if word in comment_lower)
        
        if intense_count > 0 or negative_count > 2:
            return "high"
        elif negative_count > 0:
            return "medium"
        else:
            return "low"
    
    def get_relevant_resource(self, comment: str, language: str = "python") -> str:
        """
        Returns a relevant external resource link based on the comment content.
        """
        comment_lower = comment.lower()
        
        if any(term in comment_lower for term in ["inefficient", "performance", "complexity", "algorithm"]):
            return "https://wiki.python.org/moin/TimeComplexity"
        elif any(term in comment_lower for term in ["naming", "variable", "function", "class"]):
            if language == "python":
                return "https://www.python.org/dev/peps/pep-0008/#naming-conventions"
            else:
                return "https://google.github.io/styleguide/"
        elif any(term in comment_lower for term in ["boolean", "redundant", "condition", "if"]):
            return "https://www.python.org/dev/peps/pep-0008/#programming-recommendations"
        elif any(term in comment_lower for term in ["loop", "iteration", "comprehension"]):
            return "https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions"
        elif any(term in comment_lower for term in ["function", "method", "modular"]):
            return "https://en.wikipedia.org/wiki/Single-responsibility_principle"
        else:
            if language == "python":
                return "https://www.python.org/dev/peps/pep-0008/"
            else:
                return "https://google.github.io/styleguide/"
    
    def detect_language(self, code_snippet: str) -> str:
        """
        Simple language detection based on code patterns.
        """
        if re.search(r"def\s+\w+\s*\(|import\s+\w+|\.py$", code_snippet):
            return "python"
        elif re.search(r"function\s+\w+\s*\(|const\s+|let\s+|var\s+", code_snippet):
            return "javascript"
        elif re.search(r"public|private|class\s+\w+|System\.out\.println", code_snippet):
            return "java"
        elif re.search(r"#include|using namespace|std::|cout\s*<<", code_snippet):
            return "cpp"
        elif re.search(r"func\s+\w+\s*\(|import\s+\w+|fmt\.Print", code_snippet):
            return "go"
        else:
            return "python"  # default to python
    
    def parse_ai_response(self, ai_response: str) -> Dict[str, str]:
        """
        Parses the AI response to extract the different sections.
        """
        # Initialize default values
        result = {
            "positive_rephrasing": "Great job on the code! Here's a suggestion for improvement.",
            "why": "This follows software engineering best practices for code quality.",
            "suggested_code": "# Code improvement would go here"
        }
        
        # Try to extract positive rephrasing (look for encouraging language)
        encouragement_patterns = [
            r"(?:great|good|nice|excellent|well done).*?\.(?=\s|$)",
            r"[^.!?]*[Pp]ositive[^.!?]*\.",
            r"[^.!?]*[Ee]ncouraging[^.!?]*\."
        ]
        
        for pattern in encouragement_patterns:
            matches = re.findall(pattern, ai_response, re.IGNORECASE | re.DOTALL)
            if matches:
                result["positive_rephrasing"] = matches[0]
                break
        
        # Try to extract the "why" explanation
        why_patterns = [
            r"[Ww]hy[^.:]*[:.]\s*(.*?)(?=\n\n|\n\s*\n|$)",
            r"[Pp]rinciple[^.:]*[:.]\s*(.*?)(?=\n\n|\n\s*\n|$)",
            r"[Ee]xplanation[^.:]*[:.]\s*(.*?)(?=\n\n|\n\s*\n|$)"
        ]
        
        for pattern in why_patterns:
            matches = re.findall(pattern, ai_response, re.DOTALL)
            if matches:
                result["why"] = matches[0]
                break
        
        # Try to extract code examples
        code_pattern = r'```(?:python)?\s*(.*?)\s*```'
        code_matches = re.findall(code_pattern, ai_response, re.DOTALL)
        if code_matches:
            result["suggested_code"] = code_matches[0]
        
        return result
    
    def generate_feedback(self, code_snippet: str, review_comments: List[str]) -> str:
        """
        Generates empathetic feedback for each review comment.
        """
        language = self.detect_language(code_snippet)
        markdown_output = [
            "# Empathetic Code Review Report\n\n",
            "## Original Code Snippet\n\n",
            f"```{language}\n{code_snippet}\n```\n\n"
        ]
        
        for i, comment in enumerate(review_comments, 1):
            severity = self.analyze_severity(comment)
            resource_link = self.get_relevant_resource(comment, language)
            
            prompt = f"""
            You are an experienced software developer and mentor. Your task is to provide constructive, 
            empathetic code review feedback that helps junior developers learn and improve. 
            
            Code snippet:
            {code_snippet}
            
            Original review comment: "{comment}"
            
            Please provide three things in your response:
            1. A positive rephrasing of this feedback that is encouraging and constructive
            2. A clear explanation of the underlying software principle (the "why")
            3. A concrete code example demonstrating the recommended fix
            
            Format your response clearly with each section separated by blank lines.
            The code language is {language}.
            """
            
            ai_response = self.call_gemini_api(prompt)
            parsed_response = self.parse_ai_response(ai_response)
            
            markdown_output.extend([
                f"---\n\n",
                f"### Analysis of Comment {i}: \"{comment}\"\n\n",
                f"* **Positive Rephrasing:** {parsed_response['positive_rephrasing']}\n\n",
                f"* **The 'Why':** {parsed_response['why']}\n\n",
                f"* **Suggested Improvement:**\n\n",
                f"```{language}\n{parsed_response['suggested_code']}\n```\n\n",
                f"* **Learn More:** [Relevant Resource]({resource_link})\n\n"
            ])
        
        # Add holistic summary
        summary_prompt = f"""
        Based on these review comments: {review_comments}
        For this code: {code_snippet}
        
        Please provide an overall encouraging summary that highlights the positive aspects
        and frames the feedback as growth opportunities rather than criticism.
        Keep it brief and motivating (2-3 sentences).
        """
        
        summary = self.call_gemini_api(summary_prompt)
        markdown_output.extend([
            "---\n\n",
            "## Overall Summary\n\n",
            f"{summary}\n\n",
            "---\n\n",
            "*This empathetic code review was generated by AI to foster a positive learning environment.*\n"
        ])
        
        return "".join(markdown_output)
    
    def process_json_input(self, json_input: str) -> str:
        """
        Processes the JSON input and generates the markdown report.
        """
        try:
            data = json.loads(json_input)
            code_snippet = data.get("code_snippet", "")
            review_comments = data.get("review_comments", [])
            
            if not code_snippet or not review_comments:
                return "Error: Missing 'code_snippet' or 'review_comments' in JSON input."
            
            return self.generate_feedback(code_snippet, review_comments)
            
        except json.JSONDecodeError:
            return "Error: Invalid JSON input."


# Example usage and test function
def main():
    # Example input JSON
    example_input = """
    {
        "code_snippet": "def get_active_users(users):\\n    results = []\\n    for u in users:\\n        if u.is_active == True and u.profile_complete == True:\\n            results.append(u)\\n    return results",
        "review_comments": [
            "This is inefficient. Don't loop twice conceptually.",
            "Variable 'u' is a bad name.",
            "Boolean comparison '== True' is redundant."
        ]
    }
    """
    
    reviewer = EmpatheticCodeReviewer()
    report = reviewer.process_json_input(example_input)
    
    # Print the report
    print(report)
    
    # Optionally save to file
    with open("code_review_report.md", "w") as f:
        f.write(report)


if __name__ == "__main__":
    main()
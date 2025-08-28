Empathetic Code Reviewer 🤖💙
An AI-powered tool that transforms critical code review feedback into constructive, educational, and empathetic guidance for developers.

Overview
The Empathetic Code Reviewer addresses a common challenge in software development: code reviews often become sources of friction due to blunt or impersonal feedback. This tool uses Google's Gemini AI to rephrase critical comments into supportive, educational guidance that helps developers understand the "why" behind suggestions, not just the "what".

Features
Empathetic Rephrasing: Converts direct criticism into constructive feedback

Educational Explanations: Provides clear explanations of software principles

Code Examples: Offers concrete improvements with working code snippets

Severity-Based Tone Adjustment: Adapts feedback tone based on comment harshness

Language Detection: Automatically identifies programming languages

Resource Linking: Provides relevant external documentation links

Holistic Summaries: Delivers encouraging overall feedback

Installation
1 Clone the repository:
   git clone https://github.com/your-username/empathetic-code-reviewer.git
cd empathetic-code-reviewer

2 Install dependencies:
 pip install -r requirements.txt

3 Set up environment variables:

Create a .env file in the root directory

Add your Gemini API key:

GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_API_URL=https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent

Usage
Basic Usage
Run the program and input your JSON when prompted:
python empathetic_reviewer.py

Input Format
Provide input as a JSON object with the following structure:

{
  "code_snippet": "def example_function():\n    pass",
  "review_comments": [
    "Comment 1",
    "Comment 2"
  ]
}

Output
The program generates a comprehensive Markdown report with:

Original code snippet

Analysis of each review comment

Positive rephrasing of feedback

Explanation of software principles

Suggested code improvements

Relevant resource links

Overall encouraging summary

API Requirements
This tool requires a Google Gemini API key:

Get your API key from Google AI Studio

Add it to your .env file as GEMINI_API_KEY



folder stucture 


empathetic-code-reviewer/
├── empathetic_reviewer.py  # Main application
├── requirements.txt        # Python dependencies
├── .env                   # Environment variables (create this)
├── .gitignore            # Git ignore rules
└── README.md             # This file

Dependencies
requests - HTTP library for API calls

python-dotenv - Environment variable management

json - JSON parsing (standard library)

re - Regular expressions (standard library)

os - Operating system interface (standard library)

How It Works
Input Processing: Accepts JSON with code and review comments

Language Detection: Identifies programming language from code patterns

Severity Analysis: Assesses comment harshness to adjust tone

AI Processing: Uses Gemini API to generate empathetic feedback

Response Parsing: Extracts key components from AI response

Report Generation: Creates comprehensive Markdown output

Supported Languages
Python (default)

JavaScript

Java

C++

Go
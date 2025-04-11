from google import genai
from dotenv import load_dotenv
import os
import json

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


def get_response( message: str):
    

    user_prompt="""You are a coding reasoning agent that solves coding problems step by step.
    You have access to these tools:
    - show_reasoning(steps: list) - Show your step-by-step reasoning process
    - calculate(expression: str) - Calculate the result of an expression
    - verify(expression: str, expected: float) - Verify if a calculation is correct

    First show your reasoning, then calculate and verify each step.

    Respond with EXACTLY ONE line in one of these formats:
    1. FUNCTION_CALL: {"function_name":"show_reasoning","steps":["First Step","Second Step"]}
    2. FINAL_ANSWER: answer

    Example:
    User: Solve the coding question "Given an integer x, return true if x is a palindrome, and false otherwise."
    Assistant: FUNCTION_CALL: {"function_name":"show_reasoning","steps":["1. First, convert input to int array", "2. Example: 24142 becomes [2,4,1,4,2]"]}
    User: Next step?
    Assistant: FUNCTION_CALL: {"function_name":"calculate","steps":[24142]} 
    User: Result is [2,4,1,4,2]. Let's verify this step.
    Assistant: FUNCTION_CALL: {"function_name":"verify","steps":[24142,[2,4,1,4,2]}
    User: Verified. Next step?
    Assistant: FUNCTION_CALL: {"function_name":"show_reasoning","steps":["1. For the integer array [2,4,1,4,2], iterate from 1st element and last element simulatenosuly. let's call the variable name as i and j respectively", "2. Keep Compare whether array[i] == arra[j]. Increment i by 1 step and decement j by 1 step. Stop if j becomes less than i"]}
    User: Next step?.
    Assistant: FUNCTION_CALL: {"function_name":"verify","steps":[array[i],array[j]}
    User: True if array[i] == array[j], false otherwise.
    Assistant: FINAL_ANSWER: true"""


    
    if True:
        
        response = client.models.generate_content(
            model="gemini-2.5-pro-exp-03-25",
            contents=user_prompt,
        )
        print("response is ",response.text.strip())
        return response.text.strip()
    #if response.text.startswith("```json"):
        #json_string = response.text[len("```json"):].strip().replace("```","")
        #print("json string is ",json_string)
        #return json_string
    #else:   
        #return json.loads(response.text)

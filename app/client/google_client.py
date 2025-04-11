from google import genai
from dotenv import load_dotenv
import os
import json

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


def get_response( message: str):
    

    system_prompt="""You are a Prompt Evaluation Assistant.
You will receive a prompt written by a student. Your job is to review this prompt
and assess how well it supports structured, step-by-step reasoning in an LLM (e.g.,
for math, logic, planning, or tool use).
Evaluate the prompt on the following criteria:
1. Explicit Reasoning Instructions✅
- Does the prompt tell the model to reason step-by-step?
- Does it include instructions like “explain your thinking” or “think before you
answer”?
2. Structured Output Format✅
- Does the prompt enforce a predictable output format (e.g., FUNCTION_CALL,
JSON, numbered steps)?
- Is the output easy to parse or validate?
3. Separation of Reasoning and Tools✅
- Are reasoning steps clearly separated from computation or tool-use steps?
- Is it clear when to calculate, when to verify, when to reason?
4. Conversation Loop Support✅
- Could this prompt work in a back-and-forth (multi-turn) setting?
- Is there a way to update the context with results from previous steps?
5. Instructional Framing✅
- Are there examples of desired behavior or “formats” to follow?
- Does the prompt define exactly how responses should look?
6. Internal Self-Checks✅
- Does the prompt instruct the model to self-verify or sanity-check intermediate
steps?
7. Reasoning Type Awareness✅
- Does the prompt encourage the model to tag or identify the type of reasoning
used (e.g., arithmetic, logic, lookup)?
8. Error Handling or Fallbacks✅
- Does the prompt specify what to do if an answer is uncertain, a tool fails, or
the model is unsure?
9. Overall Clarity and Robustness✅
- Is the prompt easy to follow?
- Is it likely to reduce hallucination and drift?
---
Respond with a structured review in JSON in this format:
{
"explicit_reasoning": true,
"structured_output": true,
"tool_separation": true,
"conversation_loop": false,
"instructional_framing": true,
"internal_self_checks": false,
"reasoning_type_awareness": false,
"fallbacks": false,
"overall_clarity": "Excellent structure, but could improve with self-checks and
error fallbacks."
}


Here's the User Prompt.

Problem: I need you to calculate the largest strictly increasing or deceasing substring of a string.

Explanations: Increasing substring means that each character in substring has higher ASCII code than its previous character. For Descreasing substring, each character's ASCII code will be lower than its previous character.

Question: String is "hfadsfdsfchurdcvbh"
 
If you need to create any helper function or utility function to arrive at an answer, you can create them and provide them in this format:
FUNCTION_CALL: function_name|args1|args2....
where function_name is the actual helper or utility function and args1, args2 are their corresponding arguments.

I need you to provide me how do you plan to solve this problem in bulleted points. Could you also tag each reasoning phase. An example would be: If a step involves breaking down a problem, could you tag it with "Thinking". Similarly if one of the step is extracting results from a function, could you please tag it as "Extracting Function Results". If a step involves executing certain commands or code, could you please tag it as "Code Execution"

Could you reverify whatever answer you had proposed in the first place. Reverifying means you should again check all the steps prior to it to determine whether any step was miscalculated or not. For each steps in reverification, tag them as "Correct" or "Incorrect". If a step is "Incorrect", reverify that step again till you get correct answer and tag it from "Incorrect" to "Correct"

If you find out that there are sub-problems which are already computed for the same set of inputs, could you please use memoization techniques in order to reuse that result instead of recomputing the same sub-problem again. This would allow you to reuse the results for new user input prompt. An example would be: 
For a string "fnbnnffav", if you need to calculate distict chracters encountered till index j, you could save the value of distinct characters stored at index k in a HashMap and when you are at index(k+1), you can query the HashMap with key "k" and get number of distinct characters and determine whether the current element is distinct till now or not. If not, then you can update entry in HashMap with key "k+1" and its value to be map.get(k)+1

The point I am trying to make is to reuse already computed value and save computation time. This technique would enable you to update your context window when the user sends different input strings.

If a string is malformed or a character in a string doesn't have corresponding ASCII character, respond with the answer "The provided string is invalid.

Only Provide the answer in the JSON Schema called Structured Review mentioned above. Don't provide any other text, keywords, etc. Ensure that the response is a valid JSON object.
I am noticing that I am not able to parse the response which you are sending to a valid JSON. Can you please ensure that you send the response in a JSON format so that I could convert it to JSON using json.loads() function correctly?
Could you please remove the json keyword which you are sending in the response """
    
    
    if True:
        
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=system_prompt,
        )
        print("response is ",response.text.strip())
        return response.text.strip()
    #if response.text.startswith("```json"):
        #json_string = response.text[len("```json"):].strip().replace("```","")
        #print("json string is ",json_string)
        #return json_string
    #else:   
        #return json.loads(response.text)

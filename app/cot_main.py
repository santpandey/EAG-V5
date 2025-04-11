import os
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from google import genai
import asyncio
from rich.console import Console
from rich.panel import Panel
import json
import re

console = Console()

# Load environment variables and setup Gemini
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

async def generate_with_timeout(client, prompt, timeout=10):
    """Generate content with a timeout"""
    try:
        loop = asyncio.get_event_loop()
        response = await asyncio.wait_for(
            loop.run_in_executor(
                None, 
                lambda: client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=prompt
                )
            ),
            timeout=timeout
        )
        return response
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        return None

async def get_llm_response(client, prompt):
    """Get response from LLM with timeout"""
    response = await generate_with_timeout(client, prompt)
    if response and response.text:
        return response.text.strip()
    return None

async def main():
    try:
        #console.print(Panel("Chain of Thought Calculator", border_style="cyan"))

        server_params = StdioServerParameters(
            command="python",
            args=["app/cot_tools.py"]
        )


        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                #print("came here")
                await session.initialize()
                #print("session initialized")
                system_prompt = """You are a coding reasoning agent that solves coding problems step by step.
    You have access to these tools:
    - show_reasoning(steps: list) - Show your step-by-step reasoning process
    - calculate(expression: str) - Reverse the incoming String
    - verify(expression: str, expected: float) - Verify if a calculation is correct

    First show your reasoning, then calculate and verify each step.

    Respond with EXACTLY ONE line in one of these formats:
    1. FUNCTION_CALL: {"function_name":"show_reasoning","steps":["First Step","Second Step"]}
    2. FINAL_ANSWER: answer

    Example:
    User: Solve the coding question "Given an integer x, return true if x is a palindrome, and false otherwise."
    Assistant: FUNCTION_CALL: {"function_name":"show_reasoning","steps":["1. First, Reverse the integer to a string", "2. Example: 24142 becomes '24142'"]}
    User: Next step?
    Assistant: FUNCTION_CALL: {"function_name":"calculate","steps":[24142]} 
    User: Result is '24142'. Let's verify this step.
    Assistant: FUNCTION_CALL: {"function_name":"verify","steps":[24142,'24142']}
    User: Verified. Next step?
    Assistant: FUNCTION_CALL: {"function_name":"FINAL_ANSWER","steps":[24142,'24142']}
    User: True if both the integers are same, false otherwise.
    Assistant: FINAL_ANSWER: true"""

                problem = "Given an integer 1221, return true if 1221 is a palindrome, and false otherwise."
                console.print(Panel(f"Problem: {problem}", border_style="cyan"))

                # Initialize conversation
                prompt = f"{system_prompt}\n\nSolve this problem step by step: {problem}"
                conversation_history = []
                i = -1
                while True:
                    #print("New Prompt ", prompt)
                    response = await generate_with_timeout(client, prompt)
                    if not response or not response.text:
                        break

                    result = response.text.strip()
                    #print("res", result)
                    match = re.search(r'FUNCTION_CALL:\s*({.+})', result)
                    result_json = json.loads(match.group(1))
                    print("result_json", result_json)
                    console.print(f"\n[yellow]Assistant:[/yellow] {result}")

                    if result.startswith("FUNCTION_CALL:"):
                        #_, function_info = result.split(":", 1)
                        #parts = [p.strip() for p in function_info.split("|")]
                        #func_name = parts[0]
                        #print("one")
                        #print(result_json)
                        try:
                            func_name = result_json["function_name"]
                        except Exception as e:
                            console.print(f"[red]Error: {e}[/red]")
                            break
                        
                        if func_name == "show_reasoning":
                            #steps = eval(parts[1])
                            #print("two")
                            #print(result_json)
                            steps = result_json["steps"]
                            await session.call_tool("show_reasoning", arguments={"steps": steps})
                            prompt += f"\nUser: Next step?"
                            
                        elif func_name == "calculate":
                            #expression = parts[1]
                            #print("three")
                            #print(result_json)
                            try:
                                if i > len(result_json["steps"]) - 1:
                                    i = 0
                                else:
                                    i += 1    
                                expression = result_json["steps"][i]
                                calc_result = await session.call_tool("calculate", arguments={"expression": expression})
                                print("calc_result", calc_result)
                                if calc_result.content:
                                    value = calc_result.content[0].text
                                    prompt += f"\nUser: Result is {value}. Let's verify this step."
                                    conversation_history.append((expression, value))
                            except Exception as e:
                                console.print(f"[red]Error: {e}[/red]")
                                break    
                            
                        elif func_name == "verify":
                            
                            print("four")
                            try:
                                if len(conversation_history) >= 2:
                                    original_str = conversation_history[0][1]
                                    reversed_str = conversation_history[1][1]
                                    print("original_str", original_str)
                                    print("reversed_str", reversed_str)
                                    verify_result = await session.call_tool("verify", arguments={
                                        "expression": original_str,
                                        "expected": reversed_str
                                    })
                                    if verify_result.content:
                                        value = verify_result.content[1].text
                                        print("value", value)
                                        if value:
                                            print("Result :", value)
                                            break
                                        else:
                                            print("Result :", value)
                                    prompt += f"\nUser: Verified. Next step?"
                                else:
                                    expression = result_json["steps"][0]
                                    expected = float(result_json["steps"][1])
                                    print("expression", expression)
                                    print("expected", expected)
                                
                                    verify_result = await session.call_tool("verify", arguments={
                                        "expression": expression,
                                        "expected": expected
                                    })
                                    if verify_result.content:
                                        value = verify_result.content[1].text
                                        print("value", value)
                                        if value:
                                            print("Result :", value)
                                            break
                                        else:
                                            print("Result :", value)    
                                        prompt += f"\r\nUser: Verified. Next step?"
                                        conversation_history.append((expression, value))
                                #expression, expected = parts[1], float(parts[2])
                                #console.print("[red]Error: Not enough history to verify palindrome[/red]")
                                #break
                            except Exception as e:
                                console.print(f"[red]Error: {e}[/red]")
                                break

                            #expression = result_json["steps"][0]
                            #expected = float(result_json["steps"][1])
                            #await session.call_tool("verify", arguments={
                            #    "expression": expression,
                            #    "expected": expected
                            #})
                            
                            
                    elif result.startswith("FINAL_ANSWER:"):
                        # Verify the final answer against the original problem
                        print("fanswer", result)
                        #if conversation_history:
                        #    final_answer = float(result.split("[")[1].split("]")[0])
                        #    await session.call_tool("verify", arguments={
                        #        "expression": problem,
                        #        "expected": final_answer
                        #    })
                        #break
                    
                    prompt += f"\nAssistant: {result}"

                #console.print("\n[green]Calculation completed![/green]")

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
    
    def extract_numbers_from_string(text):
        numbers = re.findall(r"[-+]?\d*\.?\d+", text)
        return numbers
    
if __name__ == "__main__":
    asyncio.run(main())

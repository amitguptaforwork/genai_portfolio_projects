from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import LLMFactory

#Use this line to choose the LLM provider
client, model = LLMFactory.getLLMClientAndModel("gemini")
#client, model = LLMFactory.getLLMClientAndModel("openai")



def run_command(command):
    print("Running command:", command)
    result = os.system(command)
    return result   

#print("**********",os.getcwd())

available_tools = {
    "run_command": {
        "fn": run_command,
        "description": "Takes an input and executes that command on the terminal and returns an output",
        "params": {
            "command": {
                "type": "string",
                "description": "Command to run"
            }
        }
    }
}

#Lets give hand and feet to our agent
system_prompt = """
You are a helpful AI assistant who is expert in resolving user queries
You work on start, plan, action, observe mode.
For the given user query and available tools, plan the step by step execution.

Based on the planning, select the relevant tool from the available tools 
And based on the selected tool, perform the action to call the tool

Based on the observation of the tool output, provide the final output to the user.

Rules:
- Follow the output json format
- Always perform one step at a time and wait for next input
- Carefully analyse the user query
- Try to identify the operating system of user and create the command accordingly
- In the file being generated, do not write \n, rather it should go to the next line

Output JSON format:
{{"step":"string",
  "content":"string",
  "function":"The name of the function if step is an action",
  "input":"The input parameter for the function"
}}

Available tools:
- run_command: Run a command


Example:
User Query :  Create a python project to square a number
Output: {{step : "plan", content : "The user wants to create a Python project to square a number. This involves creating a directory for the project, a Python file containing the squaring function, and potentially a script to run the function and display the output."}}
Output: {{step : "plan", content : "I need to create a directory, a python file, and write the square function inside that file using the run_command tool."}}
Output: {{step : "action", function : "run_command", input : "mkdir square_project && cd square_project && type nul > square.py"}}
Output: {{step : "action", function : "run_command", input : "echo "def square(x):\n return x * x" >> square_project/square.py"}}
Output: {{step : "observe", content : "Python file is created with a function named square which can used to square a number."}}
Output: {{step : "output", content : "Python file is created with a function named square which can used to square a number."}}
"""

messages=[
    {"role": "system", "content": system_prompt}
]

while True:
    query= input("> ")
    messages.append({"role": "user", "content": query})
    while True:
        response = client.chat.completions.create(
            model=model,
            response_format={"type": "json_object"},
            messages=messages
        )

        parsed_output = json.loads(response.choices[0].message.content)
        messages.append({"role": "assistant", "content": json.dumps(parsed_output)})
        step = parsed_output.get("step")
        if step == "plan":
            print(f"🧠: {parsed_output['content']}")
            continue
        if step == "action":
            tool_name = parsed_output.get("function")
            tool_input = parsed_output.get("input")
            if available_tools.get(tool_name, False)!= False:
                output = available_tools[tool_name].get("fn")(tool_input)
                messages.append({"role": "assistant", "content": json.dumps({"step":"observe","output":output})})
        if step == "output":
            print(f"🤖: {parsed_output['content']}")
            break        




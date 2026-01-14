import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from functions.call_function import available_functions, call_function

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")
args = parser.parse_args()

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key is None:
    raise Exception("invalid api key")

messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
client = genai.Client(api_key=api_key)

req = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=messages,
    config=types.GenerateContentConfig(
        tools=[available_functions],
        system_instruction=system_prompt,
        temperature=0,
    ),
)
usage_metadata = req.usage_metadata
if usage_metadata is None:
    raise RuntimeError("invalid usage metadata")

function_results = []
if req.function_calls is not None:
    for function_call in req.function_calls:
        function_call_result = call_function(function_call)
        if function_call_result.parts[0].function_response is None:
            raise RuntimeError("invalid function call")
        if function_call_result.parts[0].function_response.response is None:
            raise RuntimeError("invalid function call")
        if args.verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        function_results.extend(function_call_result.parts[0])

else:
    print(f"Response: {req.text}")

if args.verbose:
    print(f"User prompt: {args.user_prompt}")
    print(f"Prompt tokens: {usage_metadata.prompt_token_count}")
    print(f"Response tokens: {usage_metadata.candidates_token_count}")


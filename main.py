import argparse
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.call_function import available_functions, call_function
from functions.model_request import generate_content
from prompts import system_prompt


def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise Exception("invalid api key")

    client = genai.Client(api_key=api_key)

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    for _ in range(20):
        req = generate_content(client, messages, available_functions, system_prompt)
        usage_metadata = req.usage_metadata
        if usage_metadata is None:
            raise RuntimeError("invalid usage metadata")

        if len(req.candidates) > 0:
            for candidate in req.candidates:
                messages.append(candidate.content)

        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {usage_metadata.prompt_token_count}")
            print(f"Response tokens: {usage_metadata.candidates_token_count}")

        function_results = []
        if req.function_calls is not None:
            for function_call in req.function_calls:
                function_call_result = call_function(function_call)
                part = function_call_result.parts[0]
                if part.function_response is None:
                    raise RuntimeError("invalid function call")
                if part.function_response.response is None:
                    raise RuntimeError("invalid function call")
                if args.verbose:
                    print(f"-> {part.function_response.response}")

                function_results.append(part)

            messages.append(
                types.Content(
                    role="user",
                    parts=function_results,
                )
            )
        else:
            print(f"Response: {req.text}")
            return

    print("Error: could not finish, reached limit")
    exit(1)


if __name__ == "__main__":
    main()

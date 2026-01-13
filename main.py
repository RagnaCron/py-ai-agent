import os
import argparse
from dotenv import load_dotenv
from google import genai

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
args = parser.parse_args()

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key is None:
    raise Exception("invalid api key")

client = genai.Client(api_key=api_key)

req = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=args.user_prompt,
)
usage_metadata = req.usage_metadata
if usage_metadata is None:
    raise RuntimeError("invalid usage metadata")

print(f"Prompt tokens: {usage_metadata.prompt_token_count}")
print(f"Response tokens: {usage_metadata.candidates_token_count}")
print(f"Response: {req.text}")

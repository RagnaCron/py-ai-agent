from google.genai import types


def generate_content(client, messages, available_functions, system_prompt):
    req = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt,
            temperature=0,
        ),
    )
    return req

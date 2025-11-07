from google import genai
from google.genai import types
import json
import os
from dotenv import load_dotenv

load_dotenv()

with open('func/predict_tool.json', 'r', encoding='utf-8') as f:
    predict_function = json.load(f)

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
tools = types.Tool(function_declarations=[predict_function])
config = types.GenerateContentConfig(tools=[tools])

def chat_with_gemini(user_message: str):
    response = client.models.generate_content(
        model="gemini-2.0-flash-exp",
        contents=user_message,
        config=config,
    )
    
    if response.candidates[0].content.parts[0].function_call:
        function_call = response.candidates[0].content.parts[0].function_call
        return {
            "type": "function_call",
            "function_name": function_call.name,
            "arguments": dict(function_call.args)
        }
    else:
        return {
            "type": "text",
            "content": response.text
        }

def chat_with_gemini_stream(user_message: str):
    for chunk in client.models.generate_content_stream(
        model="gemini-2.0-flash-exp",
        contents=user_message,
        config=config,
    ):
        if chunk.candidates and chunk.candidates[0].content.parts:
            part = chunk.candidates[0].content.parts[0]
            if hasattr(part, 'function_call') and part.function_call:
                yield {
                    "type": "function_call",
                    "function_name": part.function_call.name,
                    "arguments": dict(part.function_call.args)
                }
                break
            elif hasattr(part, 'text') and part.text:
                yield {
                    "type": "text",
                    "content": part.text
                }

# src/dirmapper/ai/summarizer.py

from dirmapper.utils.logger import log_exception
from openai import OpenAI
import os

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def summarize_directory_structure(directory_structure: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a directory structure summarizer."},
            {"role": "user", "content": "Analyze the following directory structure and summarize the purpose of each file:"},
            {"role": "user", "content": directory_structure}

        ],
        max_tokens=500,
        temperature=0.5,
    )
    return response.choices[0].message.content

def summarize_command(args):
    try:
        with open(args.input_file, 'r') as file:
            directory_structure = file.read()
        summary = summarize_directory_structure(directory_structure)
        print(summary)
    except Exception as e:
        log_exception(e)
        print(f"Error: {e}")
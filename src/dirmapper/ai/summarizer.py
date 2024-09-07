# src/dirmapper/ai/summarizer.py

from dirmapper.formatter.format_instruction import FormatInstruction
from dirmapper.formatter.formatter import Formatter, MinimalistFormatter
from dirmapper.utils.logger import log_exception
from openai import OpenAI
import os

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

class DirectorySummarizer:
    def __init__(self, formatter: Formatter, format_instruction: FormatInstruction):
        self.formatter = formatter
        self.format_instruction = format_instruction

    def summarize(self, directory_structure: str) -> str:
        formatted_structure = self.formatter.format(directory_structure)
        return summarize_directory_structure(formatted_structure, self.format_instruction)

def summarize_directory_structure(directory_structure: str, format_instruction: FormatInstruction) -> str:
    
    output_type = 'summary'
    max_tokens = 2048  # Increase the max tokens limit
    temperature = 0.5
    model = "gpt-4o-mini"
    messages = [
        {"role": "system", "content": "You are a directory structure summarizer."},
        {"role": "user", "content": "Analyze the following directory structure and summarize the purpose of each file:"},
        {"role": "user", "content": directory_structure},
        {"role": "user", "content": format_instruction.get_instruction(output_type)}
    ]

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
    )

    summary = response.choices[0].message.content

    # Check if the response is truncated
    while response.choices[0].finish_reason == 'length':
        messages.append({"role": "assistant", "content": summary})
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        summary += response.choices[0].message.content

    return summary

# src/dirmapper/ai/summarizer.py
from dirmapper.formatter.format_instruction import FormatInstruction, MinimalistFormatInstruction

def summarize_command(args):
    try:
        with open(args.input_file, 'r') as file:
            directory_structure = file.read()

        formatter_map = {
            'minimalist': MinimalistFormatter(),
            # Add other formatters here
        }
        format_instruction_map = {
            'minimalist': MinimalistFormatInstruction(),
            # Add other format instructions here
        }

        formatter = formatter_map.get(args.format, MinimalistFormatter())
        format_instruction = format_instruction_map.get(args.format, MinimalistFormatInstruction())

        summarizer = DirectorySummarizer(formatter, format_instruction)
        summary = summarizer.summarize(directory_structure)

        if args.output:
            with open(args.output, 'w') as file:
                file.write(summary)
        else:
            print(summary)
    except Exception as e:
        log_exception(e)
        print(f"Error: {e}")
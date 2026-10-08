"""Chat assistant that lets an OpenAI model use the local resume tools."""

import json
import os

from src.fs_tools import list_files, read_file, search_in_file, write_file


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "List files in a project directory, optionally filtered by extension.",
            "parameters": {"type": "object", "properties": {
                "directory": {"type": "string"},
                "extension": {"type": ["string", "null"]},
            }, "required": ["directory"], "additionalProperties": False},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Extract text and metadata from a TXT, PDF, or DOCX file.",
            "parameters": {"type": "object", "properties": {
                "filepath": {"type": "string"},
            }, "required": ["filepath"], "additionalProperties": False},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_in_file",
            "description": "Search a resume for a keyword and return occurrences with context.",
            "parameters": {"type": "object", "properties": {
                "filepath": {"type": "string"}, "keyword": {"type": "string"},
            }, "required": ["filepath", "keyword"], "additionalProperties": False},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write a text file within the project directory, creating parent folders.",
            "parameters": {"type": "object", "properties": {
                "filepath": {"type": "string"}, "content": {"type": "string"},
            }, "required": ["filepath", "content"], "additionalProperties": False},
        },
    },
]

TOOL_FUNCTIONS = {
    "list_files": list_files,
    "read_file": read_file,
    "search_in_file": search_in_file,
    "write_file": write_file,
}


def ask_assistant(user_query: str, *, client=None, model: str = "gpt-4o-mini") -> str:
    """Answer a query, allowing the model to call the local file tools."""
    if client is None:
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise RuntimeError("Install dependencies with `pip install -r requirements.txt`.") from exc
        if not os.getenv("OPENAI_API_KEY"):
            raise RuntimeError("Set the OPENAI_API_KEY environment variable first.")
        client = OpenAI()

    messages = [
        {"role": "system", "content": (
            "You are a resume file assistant. Use the available tools to inspect the user's "
            "project files before answering file-specific questions. File paths must be relative "
            "to the project directory. Summarize findings clearly and never claim a tool action "
            "succeeded unless its result says success."
        )},
        {"role": "user", "content": user_query},
    ]

    # Bound tool rounds so an erroneous model response cannot loop indefinitely.
    for _ in range(8):
        response = client.chat.completions.create(
            model=model, messages=messages, tools=TOOLS, tool_choice="auto"
        )
        message = response.choices[0].message
        if not message.tool_calls:
            return message.content or ""

        messages.append(message)
        for tool_call in message.tool_calls:
            name = tool_call.function.name
            try:
                arguments = json.loads(tool_call.function.arguments)
                function = TOOL_FUNCTIONS[name]
                result = function(**arguments)
            except Exception as exc:
                result = {"success": False, "error": str(exc)}
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result, ensure_ascii=False),
            })

    raise RuntimeError("Assistant exceeded the maximum number of tool-calling rounds.")


def main():
    print("Resume File Assistant (type 'exit' to quit)")
    while True:
        try:
            query = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if query.lower() in {"exit", "quit"}:
            break
        if not query:
            continue
        try:
            print("Assistant:", ask_assistant(query))
        except Exception as exc:
            print(f"Assistant error: {exc}")


if __name__ == "__main__":
    main()

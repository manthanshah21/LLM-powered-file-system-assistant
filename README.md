# LLM-Powered File System Assistant

A Python assistant for reading, listing, searching, and writing resume files. It supports TXT, PDF, and DOCX extraction and uses OpenAI tool calling to select file operations from natural-language requests.

## Features

- Read text and metadata from `.txt`, `.pdf`, and `.docx` files.
- List files with size and modified-date metadata, optionally filtered by extension.
- Search file text case-insensitively and return matches with surrounding context.
- Write UTF-8 text files and create parent directories when needed.
- Keep file operations within the project directory.
- Ask an OpenAI model to call the tools in response to user requests.

## Setup

Use Python 3.10 or newer. Install the dependencies from the project root:

```bash
python -m pip install -r requirements.txt
```

Set an OpenAI API key before starting the assistant:

```bash
# PowerShell
$env:OPENAI_API_KEY = "your-api-key"

# macOS or Linux
export OPENAI_API_KEY="your-api-key"
```

## Run the assistant

From the project root, run:

```bash
python llm_file_assistant.py
```

Enter requests such as:

- `Read all resumes in the resumes folder`
- `Find resumes mentioning Python experience`
- `Create a summary file for resumes/sample.txt`

Type `exit` or `quit` to leave the interactive session.

## File tools

The tools are implemented in `src/fs_tools.py`:

- `read_file(filepath)` extracts text and metadata.
- `list_files(directory, extension=None)` returns file metadata.
- `search_in_file(filepath, keyword)` returns case-insensitive matches and context.
- `write_file(filepath, content)` writes a file inside the project directory.

Files in `resumes/` and generated files in `output/` are ignored by Git so resume data and generated output are not included in commits by default.

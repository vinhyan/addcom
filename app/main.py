from groq import Groq
import typer
from rich import print
import os
import sys

# Create Typer instance
app = typer.Typer()

# Initialize Groq client
client = Groq(
    api_key=os.getenv('GROQ_API_KEY')
)

# Create system prompt
prompt = (
    "You are a coding assistant. When provided with the contents of a code file, your task is to add appropriate "
    "comments to explain it's functionality where necessary. Comments should be formatted according to best practices. "
    "Return modified code with the added comments and no additional text or explanation as plain text"
)


def load_contents(filepath):
    """
    Read the contents of a file and return it. If the file is not found,
    print an error message and return None.
    """
    if not os.path.isfile(filepath):
        print(f"File not found: {filepath}", file=sys.stderr)
        return None
    
    with open(filepath, 'r') as file:
        return file.read()
    
def generate_comments(content: str) -> str:
    """
    Send the file content to the Groq API to generate comments.
    Returns the code with generated comments.
    """
    response = client.chat.completions.create(
        messages=[
            {
                "role": "system", 
                "content": prompt,
            },
            {
                "role": "user",
                "content": content,
            }
        ],
        model="llama3-8b-8192",
    )
    return response.choices[0].message.content


@app.command()
def add_comments(files: list[str]):
    """
    Add comments to each of the provided files.
    """
    for file in files:
        content = load_contents(file)
        if content:
            comments = generate_comments(content)
            print(f"--- {file} with added comments ---")
            print(comments)
            print()


if __name__ == '__main__':
    app()

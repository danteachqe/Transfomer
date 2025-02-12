import json
import tiktoken
from pathlib import Path

def compute_gpt4_token_counts(json_file_path: str):
    """
    Reads a JSON file that contains an array of objects with keys:
      'file', 'absolute_path', 'folder'.
    For each object, load the file from 'absolute_path',
    compute the GPT-4 token count of its content, and print the results.
    """

    # Load the JSON file
    json_path = Path(json_file_path)
    if not json_path.is_file():
        raise FileNotFoundError(f"JSON file not found: {json_file_path}")

    with open(json_path, "r", encoding="utf-8") as f:
        file_list = json.load(f)

    # Create a GPT-4 tokenizer
    # 'gpt-4' uses the same tokenizer as ChatGPT, often called "cl100k_base"
    # but we can directly do this to ensure future compatibility:
    try:
        enc = tiktoken.encoding_for_model("gpt-4")
    except KeyError:
        # If tiktoken doesn't recognize "gpt-4", fall back to cl100k_base
        enc = tiktoken.get_encoding("cl100k_base")

    # Process each entry
    total_tokens_across_all_files = 0

    for entry in file_list:
        file_name = entry["name"]
        abs_path = entry["absolute_path"]

        path_obj = Path(abs_path)
        if not path_obj.is_file():
            print(f"[WARNING] File not found, skipping: {abs_path}")
            continue

        # Read the file content
        with open(path_obj, "r", encoding="utf-8") as file_content:
            content = file_content.read()

        # Compute token count
        token_count = len(enc.encode(content))
        total_tokens_across_all_files += token_count

        # Print or store the result
        print(f"File: {abs_path}")
        print(f" - Tokens (GPT-4 tokenizer): {token_count}\n")

    print("=====================================")
    print(f"Total tokens across all files: {total_tokens_across_all_files}")

if __name__ == "__main__":
    # Update this path to point to your JSON file
    json_file = "playwright_files.json"  # or whatever your JSON file is named

    compute_gpt4_token_counts(json_file)

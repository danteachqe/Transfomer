import os
import json
from openai import OpenAI
from pathlib import Path

# Set API key (ensure it's set in the environment)
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set.")

client = OpenAI(api_key=api_key)

class GPT35Model:
    def __init__(self, model_name="gpt-4"):
        self.model_name = model_name

    def generate(self, prompt: str) -> str:
        completion = client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return completion.choices[0].message.content

def process_files(
    json_file_path: str,
    base_to_remove: str,
    output_directory: str
):
    """
    For each entry in the JSON (with 'absolute_path'),
    1) Verify the file exists at 'absolute_path'.
    2) Read file content.
    3) Send content to GPT as a prompt.
    4) Compute a relative path by removing 'base_to_remove' from 'absolute_path'
       so that the structure is preserved inside 'output_directory'.
    5) **If the file ends with .js, rename the output file to .py**.
    6) Write GPT response to that output path.
    """
    json_file_path = Path(json_file_path)
    base_to_remove_path = Path(base_to_remove)
    output_directory = Path(output_directory)

    if not json_file_path.is_file():
        raise FileNotFoundError(f"JSON file not found: {json_file_path}")

    # Load the JSON
    with open(json_file_path, "r", encoding="utf-8") as f:
        files_list = json.load(f)

    model = GPT35Model()

    print(f"[DEBUG] Loaded JSON with {len(files_list)} entries from {json_file_path}")

    for entry in files_list:
        absolute_path_str = entry["absolute_path"]
        file_name = entry["name"]     # e.g. "FlightsPage.js"
        folder = entry["folder"]      # e.g. "Pages"

        # Build the full path from 'absolute_path'
        source_path = Path(absolute_path_str)

        # Check if it exists
        if not source_path.is_file():
            print(f"[WARNING] Skipping (file not found): {source_path}")
            continue

        # Read file content
        with open(source_path, "r", encoding="utf-8") as sf:
            file_content = sf.read()

        print(f"[DEBUG] Reading from: {source_path}")
        print(f"[DEBUG] Characters loaded: {len(file_content)}")

        # Build prompt
        prompt = (
            "The following code is part of a Playwright framework. "
            "Adapt it to Python + Playwright with no structural or logical changes. Keep the page ojcect model in case you get such files but adapt it to python"
            "If you see a configuration file or something that doesn't look like code that needs adaptation, do not do anything to it"
            "Respond only with converted code, no other comments.\n\n"
            f"{file_content}"
        )

        # Generate GPT response
        response = model.generate(prompt)

        # Attempt to remove the base path so we only keep the subfolder + filename
        try:
            relative_path = source_path.relative_to(base_to_remove_path)
        except ValueError:
            print(f"[WARNING] {source_path} is not under {base_to_remove_path}, skipping.")
            continue

        # -----------------------------
        # If the source file ends with .js, change the destination extension to .py
        # -----------------------------
        if relative_path.suffix.lower() == ".js":
            relative_path = relative_path.with_suffix(".py")

        # Create the destination path under output_directory
        dest_file_path = output_directory / relative_path

        # Make sure the folder structure exists
        dest_file_path.parent.mkdir(parents=True, exist_ok=True)

        # Write the GPT response
        with open(dest_file_path, "w", encoding="utf-8") as out_file:
            out_file.write(response)

        print(f"[INFO] Saved response to {dest_file_path}")

if __name__ == "__main__":
    # Adjust these to your environment
    json_file_path = r"C:\Cursuri\Code\transformer\playwright_files.json"
    base_to_remove = r"C:\Cursuri\Code\Playwright"
    output_directory = r"C:\Cursuri\Code\transformer\destination"

    print("[DEBUG] Starting file processing...")
    process_files(json_file_path, base_to_remove, output_directory)
    print("[DEBUG] Finished file processing.")

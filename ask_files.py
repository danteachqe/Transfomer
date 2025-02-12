import os
import json
from openai import OpenAI  
from pathlib import Path

# Optionally, set the API key here if it's not set as an environment variable
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set.")

# Instantiate the client with the API key
client = OpenAI(api_key=api_key)

# Define a model class that will be passed to the function
class GPT35Model:
    def __init__(self, model_name="gpt-4"):
        self.model_name = model_name

    # This method must return a single string as an answer
    def generate(self, prompt: str) -> str:
        completion = client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        # Extract the text from the response
        return completion.choices[0].message.content

def ask_which_files_are_playwright(json_content: str) -> str:
    """
    Sends a prompt to the GPT model asking which files are part of the Playwright framework.
    :param json_content: A string containing the JSON representation of the folder structure.
    :return: The GPT model's response as a string.
    """
    model = GPT35Model()

    # Build your prompt, referencing the JSON content
    prompt = (
        "Based on the content of the following json folder export for an expisting Playwright with JS folder structure, which files are part of the Playwright framework? Ignore git conf and licencese and other items that are not part of the framework, json files can also be ignored. you can ignore also the playwright configuration file "
        "Respond only with a json list(no other comments) that contains the absolute location of the files and the folder of the files.\n\n"
        f"{json_content}"
    )

    # Send the prompt and get a response
    response = model.generate(prompt)
    return response

def main():
    """
    Example main function to:
      1) Read the JSON file.
      2) Send its content to GPT.
      3) Parse and save the response as a JSON file.
    """
    # Read from the folder_structure.json (or any JSON file) as an example:
    json_file_path = Path("folder_structure.json")
    if not json_file_path.is_file():
        print(f"Could not find the file {json_file_path}")
        return

    with open(json_file_path, "r", encoding="utf-8") as f:
        folder_structure = f.read()  # Keep it as raw text

    # Ask the GPT model which files belong to Playwright
    result_str = ask_which_files_are_playwright(folder_structure)
    print("GPT Model Response (raw string):\n", result_str)

    # Try to parse the response as JSON
    try:
        result_json = json.loads(result_str)
    except json.JSONDecodeError:
        print("Error: GPT response was not valid JSON.")
        return

    # Save the parsed JSON to a file
    output_path = Path("playwright_files.json")
    with open(output_path, "w", encoding="utf-8") as outfile:
        json.dump(result_json, outfile, indent=2)

    print(f"Playwright file list saved to {output_path.resolve()}")

if __name__ == "__main__":
    main()

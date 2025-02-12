import os
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

def process_file_with_prompts(
    source_file: str,
    prompt1: str,
    output_file1: str,
    prompt2: str,
    output_file2: str
):
    """
    1. Reads the content from the source file.
    2. Sends two different prompts (each appended with the file content) to GPT.
    3. Saves each GPT response to the specified output file.
    """
    source_file_path = Path(source_file)
    if not source_file_path.is_file():
        raise FileNotFoundError(f"Source file not found: {source_file_path}")

    # Read the file content
    with open(source_file_path, "r", encoding="utf-8") as f:
        file_content = f.read()

    model = GPT35Model()

    # Build full prompts by appending the file content to each prompt.
    full_prompt1 = f"{prompt1}\n\n{file_content}"
    full_prompt2 = f"{prompt2}\n\n{file_content}"

    # Generate the first response
    print("[DEBUG] Generating response for prompt1...")
    response1 = model.generate(full_prompt1)
    output_file_path1 = Path(output_file1)
    output_file_path1.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file_path1, "w", encoding="utf-8") as out1:
        out1.write(response1)
    print(f"[INFO] Saved response for prompt1 to {output_file_path1}")

    # Generate the second response
    print("[DEBUG] Generating response for prompt2...")
    response2 = model.generate(full_prompt2)
    output_file_path2 = Path(output_file2)
    output_file_path2.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file_path2, "w", encoding="utf-8") as out2:
        out2.write(response2)
    print(f"[INFO] Saved response for prompt2 to {output_file_path2}")

if __name__ == "__main__":
    # Hard-coded file locations and prompts
    source_file = r"C:\Cursuri\Code\Playwright\playwright.config.js"
    prompt1 = "This file is the config file of the playwright + JS automation framework. I want to use the playwright + Python automation framework so I will use for this pytest(ini file and conf file). Generate only the pytest.ini file that will meaintain the functionality as is now in the confg file. Respond only with the content of the file, no other comments"
    output_file1 = r"C:\Cursuri\Code\transformer\final\pytest.ini"

    prompt2 = "This file is the config file of the playwright + JS automation framework. I want to use the playwright + Python automation framework so I will use for this pytest(ini file and conf file). Generate only the conftest.py file that will meaintain the functionality as is now in the confg file.  Respond only with the content of the file, no other comments"
    output_file2 = r"C:\Cursuri\Code\transformer\final\conftest.py"

    print("[DEBUG] Starting file processing...")
    process_file_with_prompts(source_file, prompt1, output_file1, prompt2, output_file2)
    print("[DEBUG] Finished file processing.")

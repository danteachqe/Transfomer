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

def process_files_with_prompt(file1: str, file2: str, file3: str, prompt: str, output_file: str):
    """
    Reads the content of three files, combines them with a provided prompt,
    sends the combined prompt to GPT, and saves the GPT response to the output file.
    """
    # Create Path objects for the files
    file1_path = Path(file1)
    file2_path = Path(file2)
    file3_path = Path(file3)
    
    # Check if the files exist
    if not file1_path.is_file():
        raise FileNotFoundError(f"File not found: {file1_path}")
    if not file2_path.is_file():
        raise FileNotFoundError(f"File not found: {file2_path}")
    if not file3_path.is_file():
        raise FileNotFoundError(f"File not found: {file3_path}")
    
    # Read file contents
    with open(file1_path, "r", encoding="utf-8") as f:
        content1 = f.read()
    with open(file2_path, "r", encoding="utf-8") as f:
        content2 = f.read()
    with open(file3_path, "r", encoding="utf-8") as f:
        content3 = f.read()
    
    # Build the full prompt by combining the provided prompt with each file's content.
    # You can adjust the labels and formatting as needed.
    full_prompt = (
        f"{prompt}\n\n"
        f"File 1 content:\n{content1}\n\n"
        f"File 2 content:\n{content2}\n\n"
        f"File 3 content:\n{content3}"
    )
    
    # Generate GPT response
    model = GPT35Model()
    print("[DEBUG] Generating response from GPT...")
    response = model.generate(full_prompt)
    
    # Save the GPT response to the output file.
    output_file_path = Path(output_file)
    output_file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file_path, "w", encoding="utf-8") as out_file:
        out_file.write(response)
    print(f"[INFO] Saved GPT response to {output_file_path}")

if __name__ == "__main__":
    # Hard-coded file paths
    file1 = r"C:\Cursuri\Code\transformer\final\pytest.ini"
    file2 = r"C:\Cursuri\Code\transformer\final\conftest.py"
    file3 = r"C:\Cursuri\Code\transformer\destination\Pages\HomePage.py"

    # Hard-coded prompt
    prompt = (
        "I am sending the content of 3 files.  pytest.ini, conftest.py and a script representing a page object model for a webpage "
        "I want you to adapt the content of the page object model with no function change so that its compatible with the configuration files. In case its already compatible do not change anything. Do not try to optimise just assure compatibility"
        "Respond with only the python code, and not other comment whatsoever, even is compatibility is achieved(repaste the py script, no not provide any additional comments)."
    )
    
    # Hard-coded output file location
    output_file = r"C:\Cursuri\Code\transformer\final\Pages\Homepage.py"
    
    print("[DEBUG] Starting processing of files with prompt...")
    process_files_with_prompt(file1, file2, file3, prompt, output_file)
    print("[DEBUG] Finished processing of files.")

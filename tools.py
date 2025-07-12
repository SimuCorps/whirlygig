# Note that the excessive documentation is for the models.
import os 
import google.genai as genai
def get_file(file: str):
    """Get the text contents of a file.

    Args:
        file: The file path.

    Returns:
        str: The text contents of the file.
    """
    if file.startswith("~"):
        file = os.path.expanduser(file)
    with open(file, 'r') as f:
        return f.read()

def get_files_in_directory(path: str):
    """Get a listing of all files in a directory.
    
    Args:
        path: The directory path.

    Returns:
        list: A list of all files in the directory (not recursive).
    """
    if path.startswith("~"):
        path = os.path.expanduser(path)
    return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

def new_agent(client: genai.client, config: genai.types.GenerateContentConfig, instructions: str, prompt: str):
    # Documentation for this is in main.py, since it uses the client and config provided by it.
    config.system_instruction = instructions
    return client.models.generate_content(
        model="gemini-2.5-flash",
        config=config,
        contents=prompt
    )
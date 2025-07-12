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

def get_files_in_directory(directory: str):
    """Get a listing of all files in a directory.
    
    Args:
        directory: The directory path.

    Returns:
        list: A list of all files in the directory (not recursive).
    """
    if directory.startswith("~"):
        directory = os.path.expanduser(directory)
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]


def new_agent(client: genai.client, config: genai.types.GenerateContentConfig, instructions: str, prompt: str):
    """Create a new agent. They will be ran one-shot [i.e, they only get your instructions and prompt, then return.]
    It may read files, but it cannot run commands.
    The instructions default to being empty, so you should explain its purpose in the instructions, and then use the prompt for "user" input.
    
    Args:
        instructions: The instructions for the agent.
        prompt: The prompt for the agent.

    Returns:
        str: The response from the agent.
    """
    return client.models.generate_content(
        model="gemini-2.5-flash",
        config=config,
        instructions=instructions,
        prompt=prompt
    )
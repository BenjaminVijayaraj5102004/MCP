from mcp.server.fastmcp import FastMCP
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("PromptReader")

mcp = FastMCP("Prompt-Reader")
BASE_PATH = r'D:\Studies\n8n\MCP\Prompts'

# FIXED: Added specific_file parameter
def _read_category_files(category: str, specific_file: str = None) -> str:
    folder_path = os.path.normpath(os.path.join(BASE_PATH, category))
    
    # Logic for a single specific file
    if specific_file:
        full_name = specific_file if specific_file.endswith(".md") else f"{specific_file}.md"
        file_path = os.path.join(folder_path, full_name)
        
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                return f"### SOURCE_FILE: {full_name}\n{f.read()}"
        return f"Error: {full_name} not found in {category}"

    # Original logic for all files
    all_content = []
    if not os.path.exists(folder_path):
        return f"Error: Folder '{category}' not found."

    filenames = [f for f in os.listdir(folder_path) if f.endswith(".md")]
    for filename in filenames:
        with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as f:
            all_content.append(f"### SOURCE_FILE: {filename}\n{f.read()}")

    return "\n\n---\n\n".join(all_content) if all_content else "No files found."

@mcp.resource("prompts://design")
def design_prompts() -> str:
    return _read_category_files("design")

@mcp.resource("prompts://engineering")
def engineering_prompts() -> str:
    # This now works because the helper accepts two arguments!
    return _read_category_files("engineering", "engineering-frontend-developer")

@mcp.resource("prompts://testing")
def testing_prompts() -> str:
    return _read_category_files("testing")

if __name__ == "__main__":
    mcp.run()
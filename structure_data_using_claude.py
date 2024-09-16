import os
import anthropic
from typing import Dict, List

import dotenv
dotenv.load_dotenv()



# Initialize Anthropic client
client = anthropic.Anthropic(
    # Use environment variable for API key instead of hardcoding
    api_key=os.environ.get("ANTHROPIC_API_KEY")
)

def structure_data_using_claude(data: str, query: str) -> str:
    """
    Design a webpage to display given text information based on a query.

    Args:
        data (str): The chunk of text information to structure.
        query (str): The query to guide the webpage design.

    Returns:
        str: A description of the webpage structure and design.
    """
    system_prompt = """
    You are a helpful assistant that structures data into a webpage.
    Given a chunk of text information and query, structure the data into a webpage.
    Provide specific details on the webpage design, keeping it simple and elegant.
    Design a single page without providing any code, focusing on structure and layout.
    """
    
    user_prompt = f"""
    Data: {data}
    Query: {query}
    """
    
    messages: List[Dict[str, str]] = [
        {"role": "user", "content": user_prompt},
    ]
    
    try:
        response = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=1024,
            system=system_prompt,
            messages=messages,
        )
        return response.content[0].text
    except Exception as e:
        print(f"Error occurred while calling Claude API: {e}")
        return ""


def structure_data_using_claude_refresh(data: str, query: str,old_structure: str) -> str:
    """
    Refresh and create the new webpage structure from the old one based on data and query.

    Args:
        data (str): The new chunk of text information to structure.
        query (str): The new query to guide the webpage design.
        old_structure (str): The old structure of the webpage.

    Returns:
        str: A description of the webpage structure and design.
    """
    system_prompt = """
    You are a cynical assistant that structures data into a webpage about why things suck.
    Given a chunk of text information and query, structure the data into a webpage that highlights negative aspects.
    Provide specific details on the webpage design, keeping it simple but with a pessimistic tone.
    Design a single page without providing any code, focusing on structure and layout that emphasizes drawbacks and flaws.
    """
    
    user_prompt = f"""
    Data: {data}
    Query: {query}
    Old Structure: {old_structure}
    
    Create a new structure different from the old one. 
    """
    
    messages: List[Dict[str, str]] = [
        {"role": "user", "content": user_prompt},
    ]
    
    try:
        response = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=1024,
            system=system_prompt,
            messages=messages,
        )
        return response.content[0].text
    except Exception as e:
        print(f"Error occurred while calling Claude API: {e}")
        return ""

def main():
    # Example usage
    data = "Hello, Claude"
    query = "Create a simple greeting page"
    result = structure_data_using_claude(data, query)
    print(result)

    result = structure_data_using_claude_refresh(data, query,result)
    print("New Structure:")
    print(result)

if __name__ == "__main__":
    main()

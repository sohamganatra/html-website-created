import os
import dotenv
from exa_py import Exa

dotenv.load_dotenv()

def get_exa_client():
    return Exa(os.getenv("EXA_API_KEY"))

def search_ai_startups(exa_client=get_exa_client(), query="hottest AI startups", num_results=10):
    return exa_client.search_and_contents(
        query,
        type="neural",
        use_autoprompt=True,
        num_results=num_results,
        text=True,
    )

def search_and_save_ai_startups(query="hottest AI startups", num_results=10):
    exa = get_exa_client()
    result = search_ai_startups(exa, query, num_results)
    
    # store result print in a file as simple output 
    with open("ai_startups.txt", "w") as f:
        f.write(str(result))
    
    return result

if __name__ == "__main__":
    search_and_save_ai_startups()

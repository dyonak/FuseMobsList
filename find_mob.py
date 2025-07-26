import json
from pathlib import Path

def find_mob(mobs_data, search_term):
    """
    Finds a mob's canonical name and its data by a given search term.

    This function performs a case-insensitive search against both the mob's
    main name and its list of synonyms.

    Args:
        mobs_data (dict): The dictionary of mobs loaded from the JSON file.
        search_term (str): The name or synonym to search for.

    Returns:
        tuple: A tuple containing the mob's canonical name (str) and its
               data (dict) if a match is found, otherwise (None, None).
    """
    # Use a lowercase search term for case-insensitive matching.
    term_lower = search_term.lower()

    # Iterate through each mob in the dictionary.
    for mob_name, mob_info in mobs_data.items():
        # 1. Check if the search term matches the mob's main name.
        if term_lower == mob_name.lower():
            return mob_name, mob_info

        # 2. Check if the search term exists in the mob's synonyms list.
        # We convert each synonym to lowercase to ensure the match is case-insensitive.
        synonyms_lower = [s.lower() for s in mob_info.get("synonyms", [])]
        if term_lower in synonyms_lower:
            return mob_name, mob_info

    # If the loop completes without finding a match, return None.
    return None, None

# --- Example Usage ---

# Construct the path to the JSON file relative to this script.
# This assumes 'find_mob.py' is in the same directory as 'mobs.json'.
json_file_path = Path(__file__).parent / "mobs.json"

if not json_file_path.exists():
    print(f"Error: The file '{json_file_path}' was not found.")
else:
    # Load the JSON data from the file
    with open(json_file_path, 'r') as f:
        all_mobs_data = json.load(f)

    # --- Test Cases ---
    queries = ["vindi", "tuna", "Wuoshi", "a non-existent mob"]

    for query in queries:
        print(f"Searching for: '{query}'")
        mob_name, mob_data = find_mob(all_mobs_data, query)

        if mob_name:
            print(f"  ✅ Found a match!")
            print(f"     Canonical Name: {mob_name}")
            print(f"     Location: {mob_data.get('location')}")
            print(f"     Synonyms: {', '.join(mob_data.get('synonyms', []))}")
            print(f"     Track: {mob_data.get('track')}")
            print(f"     Coth: {mob_data.get('coth')}")
            print(f"     ET: {mob_data.get('et')}")
            print("-" * 30)
        else:
            print(f"  ❌ No mob found with the name or synonym '{query}'.")
            print("-" * 30)
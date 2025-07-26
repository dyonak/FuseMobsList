import json
from pathlib import Path
from flask import Flask, jsonify, render_template, request, abort

# --- Configuration ---
app = Flask(__name__)
JSON_FILE_PATH = Path(__file__).parent / "mobs.json"

# --- Helper Functions ---
def load_mobs():
    """Loads mob data from the JSON file."""
    if not JSON_FILE_PATH.exists():
        return {}
    # Use utf-8 encoding for broader character support
    with open(JSON_FILE_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_mobs(data):
    """Saves mob data to the JSON file."""
    # Use utf-8 encoding and indent for readability
    with open(JSON_FILE_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

# --- Web Route (Frontend) ---
@app.route('/')
def index():
    """Serves the main HTML page."""
    return render_template('index.html')

# --- API Routes ---
@app.route('/api/mobs', methods=['GET'])
def get_all_mobs():
    """Returns all mob data, sorted by name."""
    mobs_data = load_mobs()
    # Sorting the dictionary by key (mob name) for consistent order
    sorted_mobs = dict(sorted(mobs_data.items()))
    return jsonify(sorted_mobs)

@app.route('/api/mobs/<string:mob_name>', methods=['PUT'])
def update_mob(mob_name):
    """Updates a specific mob's data."""
    mobs_data = load_mobs()

    # The frontend sends the canonical name, but we check for existence just in case.
    if mob_name not in mobs_data:
        abort(404, description=f"Mob '{mob_name}' not found.")

    if not request.json:
        abort(400, description="Invalid JSON payload.")

    update_data = request.json
    mob_to_update = mobs_data[mob_name]

    # Fields that are allowed to be updated per your request
    allowed_fields = {"fte", "coth", "track", "et", "synonyms"}

    for field, value in update_data.items():
        if field in allowed_fields:
            if field == "synonyms":
                # Basic validation for synonyms
                if isinstance(value, list) and all(isinstance(s, str) for s in value):
                    # Filter out any empty strings that might result from input processing
                    mob_to_update[field] = [s.strip() for s in value if s.strip()]
                else:
                    abort(400, description=f"Field '{field}' must be a list of strings.")
            else:
                mob_to_update[field] = value

    save_mobs(mobs_data)

    return jsonify({"message": "Mob updated successfully", "mob": mob_to_update})

# --- Main Execution ---
if __name__ == '__main__':
    # debug=True is great for development, but should be turned off for production
    app.run(debug=True)
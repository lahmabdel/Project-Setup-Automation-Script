import os
import json
import utilities


if __name__ == "__main__":
    # Step 1: Read Configuration from JSON File
    try:
        # Make sure the JSON file is in the same directory as the script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(script_dir, "config.json")

        # Load the JSON file
        with open(config_path, "r") as f:
            config = json.load(f)

        # Extract parameters from JSON
        base_path = config["base_path"]
        project_name = config["project_name"]
        github_url = config.get("github_url")  # Optional parameter
        github_token = config.get("github_token")  # GitHub personal access token

        # Call the main function
        utilities.create_project(base_path, project_name, github_url, github_token)

    except FileNotFoundError:
        print("Error: config.json file not found. Please create it in the script's directory.")
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in config.json.")
    except KeyError as e:
        print(f"Error: Missing required parameter in config.json: {e}")

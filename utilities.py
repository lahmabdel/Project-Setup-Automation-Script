import os
import json
import shutil
import subprocess
from github import Github, GithubException

def validate_github_token(token):
    """
    Validates if the GitHub token is still valid.
    """
    try:
        github = Github(token)
        user = github.get_user()
        user.login  # Accessing this will raise an error if the token is invalid
        print(f"GitHub token validated for user: {user.login}")
        return github, user
    except GithubException as e:
        print(f"Error: Invalid or expired GitHub token. {e}")
        return None, None


def check_github_repo_exists(user, repo_name):
    """
    Checks if a repository with the given name already exists for the authenticated user.
    """
    try:
        for repo in user.get_repos():
            if repo.name == repo_name:
                print(f"GitHub repository '{repo_name}' already exists.")
                return True
        return False
    except GithubException as e:
        print(f"Error checking GitHub repositories: {e}")
        return False


def create_github_repo(user, repo_name, description="", private=True):
    """
    Creates a GitHub repository using PyGithub.
    """
    try:
        repo = user.create_repo(
            name=repo_name,
            description=description,
            private=private
        )
        print(f"GitHub repository '{repo_name}' created successfully!")
        print(f"Repository URL: {repo.clone_url}")
        return repo.clone_url
    except GithubException as e:
        print(f"Error creating GitHub repository: {e}")
        return None


def create_project(base_path, project_name, github_url=None, github_token=None):
    """
    Creates a local project structure and optionally links it to a GitHub repository.
    """
    try:
        # Step 1: Ensure a Unique Project Name
        project_path = os.path.join(base_path, project_name)
        counter = 2
        while os.path.exists(project_path):
            project_name = f"{project_name.split('_')[0]}_{counter}"
            project_path = os.path.join(base_path, project_name)
            counter += 1

        os.makedirs(project_path, exist_ok=True)
        os.chdir(project_path)
        print(f"Created and moved into project folder: {project_path}")

        # Step 2: Create Virtual Environment
        subprocess.run(["python", "-m", "venv", "venv"], check=True)
        print("Virtual environment created.")

        # Step 3: Create Basic Files
        with open("requirements.txt", "w") as f:
            f.write("")  # Empty requirements.txt
        with open("main.py", "w") as f:
            f.write('if __name__ == "__main__":\n    print("Hello, world!")')
        print("Created requirements.txt and main.py.")

        # Step 4: Create a .gitignore File
        with open(".gitignore", "w") as f:
            f.write("venv/\n")
        print("Created .gitignore with 'venv/' excluded.")

        # Step 5: Copy README Template
        script_dir = os.path.dirname(os.path.abspath(__file__))
        template_path = os.path.join(script_dir, "readme_template.md")
        readme_destination = os.path.join(project_path, "README.md")
        if os.path.exists(template_path):
            shutil.copy(template_path, readme_destination)
            print(f"Copied README template from {template_path} to {readme_destination}.")
        else:
            print(f"Template file {template_path} does not exist. Skipping README creation.")

        # Step 6: Create a Utilities Folder
        utilities_path = os.path.join(project_path, "utilities")
        os.makedirs(utilities_path, exist_ok=True)
        print(f"Created utilities folder at: {utilities_path}")

        # Step 7: Initialize Git Repository
        if not os.path.exists(".git"):
            subprocess.run(["git", "init"], check=True)
            subprocess.run(["git", "add", "."], check=True)
            subprocess.run(["git", "commit", "-m", "Initial commit"], check=True)
            print("Initialized a Git repository and made the initial commit.")
        else:
            print("Git repository already initialized. Skipping git initialization.")

        # Step 8: Create or Validate GitHub Repository
        if github_token:
            github, user = validate_github_token(github_token)
            if not github or not user:
                return

            if not github_url:
                while check_github_repo_exists(user, project_name):
                    project_name = input("github repo alreay exists, please provide a valid name: ")
                else:
                    github_url = create_github_repo(
                        user, repo_name=project_name, description=f"Repository for {project_name}", private=True
                    )
                    if not github_url:
                        github_url = input("Error creating the GitHub repository. Please provide a GitHub URL manually: ")

        # Step 9: Connect to GitHub and Push
        if github_url:
            subprocess.run(["git", "remote", "add", "origin", github_url], check=True)
            subprocess.run(["git", "branch", "-M", "main"], check=True)
            
            # Pull remote changes to avoid conflicts
            try:
                subprocess.run(["git", "pull", "origin", "main", "--allow-unrelated-histories"], check=True)
            except subprocess.CalledProcessError:
                print("Warning: Failed to pull remote changes. Continuing with push.")

            # Push the changes
            subprocess.run(["git", "push", "-u", "origin", "main"], check=True)
            print(f"Connected to GitHub and pushed to {github_url}.")

        print(f"Project setup complete! Final project name: {project_name}")

    except Exception as e:
        print(f"Error: {e}")
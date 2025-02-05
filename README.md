

# Project Setup Automation Script

This Python script automates the process of setting up a Python project, including creating a local folder structure, initializing a Git repository, and optionally creating and linking a GitHub repository.

## Features

- Creates a local project folder with:
  - Virtual environment (`venv/`)
  - A basic `main.py` file
  - `requirements.txt` for dependencies
  - `.gitignore` pre-configured to exclude the virtual environment
  - A `utilities/` folder
  - A `README.md` (based on a customizable template)
- Initializes a Git repository with an initial commit.
- Optionally creates a GitHub repository and links it to the local project.
- Validates the GitHub personal access token.
- Handles errors such as:
  - Invalid or expired GitHub tokens.
  - Duplicate project names on GitHub.
  - Errors in creating or linking GitHub repositories.

---

## Requirements

- Python 3.x installed on your system.
- A GitHub personal access token with the `repo` scope.
- `PyGithub` Python package for GitHub integration:
  ```bash
  pip install PyGithub
  ```

---

## Installation

To use this automation tool, you can pull it from its GitHub repository and set it up locally.

### Steps to Pull and Install:

1. Open a terminal or command prompt.

2. Clone the repository using the following command:
   ```bash
   git clone https://github.com/yourusername/project_setup_automation.git
   ```

3. Navigate to the cloned directory:
   ```bash
   cd project_setup_automation
   ```

4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Customize your `config.json` file in the project directory. (See [Configuration](#configuration) for details.)

6. Run the script to set up a project:
   ```bash
   python main.py
   ```

## Configuration

Create a `config.json` file in the same directory as the script with the following structure:

```json
{
    "base_path": "C:\\Path\\To\\Your\\Projects",
    "project_name": "my_project",
    "github_token": "<your_personal_access_token>",
    "github_url": null
}
```

### Fields:
- `base_path`: The directory where your project folder will be created.
- `project_name`: The name of your project.
- `github_token` (optional): Your GitHub personal access token.
- `github_url` (optional): The URL of an existing GitHub repository to link with the local project. If not provided, the script will attempt to create a new repository.

---

## Usage

Run the script using Python:

```bash
python setup_project.py
```

### What Happens:
1. A new project folder is created in the specified `base_path`.
2. A virtual environment (`venv/`) is initialized.
3. Files like `main.py`, `requirements.txt`, `.gitignore`, and `README.md` are created.
4. A Git repository is initialized with an initial commit.
5. If `github_url` is not provided:
   - A GitHub repository is created using the GitHub token.
   - If the repository creation fails, the script prompts for a GitHub URL.
   - if GitHub URL not provided, the script won't link the local repository to a GitHub repository
6. The local repository is linked to the GitHub repository and changes are pushed.

---

## Error Handling

- **Invalid Token**: The script checks the GitHub token's validity and prompts an error if it is invalid or expired.
- **Duplicate Repository Names**: If a repository with the same name already exists, the script links to it instead of creating a new one.
- **GitHub Repository Creation Errors**: If creating the repository fails, the script asks for a manual GitHub URL.
- **Initial Commit Exists**: Skips Git initialization and commit if the repository is already initialized.

---

## Example

### Input `config.json`:
```json
{
    "base_path": "C:\\Users\\username\\projects",
    "project_name": "automation_tool",
    "github_token": "ghp_exampleToken1234567890",
    "github_url": null
}
```

### Example Run:
```bash
python setup_project.py
```




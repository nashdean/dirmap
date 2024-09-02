# Dirmapper

**Dirmapper** is a CLI tool to generate and create directory structures. It provides a visual representation of the directory and file structure, similar to the `tree` command, with support for `.gitignore`-like patterns to exclude specific files and directories. Additionally, it allows creating directory structures from templates.

## Features

- Generate a hierarchical view of a directory structure.
- Create directory structures from templates.
  - JSON Format
  - YAML Format
- Create directory structures from a text file with the directory map/structure. Useful when asking ChatGPT to create you a project directory.
  - Optionally create a reusable template from the directory map/structure.
- Support for `.mapping-ignore` file to exclude files and directories.
- Optional integration with `.gitignore` to exclude patterns specified in `.gitignore`.
- Case-sensitive and case-insensitive sorting options.

## Installation

### Using Homebrew

You can install `dirmapper` using Homebrew:

```sh
brew tap nashdean/dirmap
brew install dirmapper
```

### Using pipx

It is recommended to use `pipx` to install `dirmapper` in an isolated environment:

```sh
pipx install dirmapper
```

### Using pip

You can also install `dirmapper` using pip:

```sh
pip install dirmapper
```

## Usage

### Basic Usage

To generate a directory structure mapping:

```sh
dirmap read /path/to/root_directory /path/to/output_file
```

### Writing Directory Structure from a Template

To create a directory structure from a template file (YAML or JSON):

```sh
dirmap write /path/to/template_file /path/to/root_directory
```

### Writing Directory Structure from a Text File

To create a directory structure from a text file with the directory map/structure:

```sh
dirmap write /path/to/directory_map.txt /path/to/root_directory
```

### Exclude Patterns with .mapping-ignore

Create a `.mapping-ignore` file in the root directory and specify the patterns you want to exclude:

```
.git/
*.tmp
*.log
```

Then run:

```sh
dirmap read /path/to/root_directory /path/to/output_file --ignore_file /path/to/.mapping-ignore
```

### Inline Ignores and Complex Regex in .mapping-ignore

You can now include complex regex patterns in your `.mapping-ignore` file:

```
.git/
.*cache
regex:^.*\.log$
```

### Disable .gitignore Integration

By default, `dirmap` will also consider patterns in `.gitignore`. To disable this feature:

```sh
dirmap read /path/to/root_directory /path/to/output_file --ignore_file /path/to/.mapping-ignore --no_gitignore
```

### Case-Sensitive and Non-Case-Sensitive Sorting

You can specify the order in which directories and files are listed, with options for case-sensitive and non-case-sensitive sorting:

```sh
# Ascending order (case-insensitive)
dirmap read /path/to/root_directory /path/to/output_file --sort asc

# Ascending order (case-sensitive)
dirmap read /path/to/root_directory /path/to/output_file --sort asc:case

# Descending order (case-insensitive)
dirmap read /path/to/root_directory /path/to/output_file --sort desc

# Descending order (case-sensitive)
dirmap read /path/to/root_directory /path/to/output_file --sort desc:case
```

### Show Version

To display the version of `dirmapper`:

```sh
dirmap --version
```

or

```sh
dirmap -v
```

## Example

### Sample Directory Structure

```
project/
├── .git/
│   └── config
├── .github/
│   └── workflows/
│       └── ci.yml
├── src/
│   ├── main.py
│   ├── utils.py
└── README.md
```

### Sample .mapping-ignore

```
.git/
.github/
```

### Command

```sh
dirmap read project output.txt --ignore_file project/.mapping-ignore
```

### Sample Output

```
project/
├── src/
│   ├── main.py
│   └── utils.py
└── README.md
```

### Writing Directory Structure from Template

#### Sample Template (YAML)

```yaml
meta:
  version: "1.0"
  tool: "dirmapper"
  author: YOUR_NAME
template:
  src:
    project_name:
      __init__.py: ""
  tests:
    __init__.py: ""
  docs: {}
  README.md: ""
  setup.py: ""
  requirements.txt: ""
  .gitignore: ""
```
#### Command

```sh
dirmap write write_template.yaml directory
```

#### Sample Template (JSON)
```json
{
    "meta": {
      "version": "1.0",
      "tool": "dirmapper",
      "author": "YOUR_NAME"
    },
    "template": {
      "src": {
        "project_name": {
          "__init__.py": ""
        }
      },
      "tests": {
        "__init__.py": ""
      },
      "docs": {},
      "README.md": "",
      "setup.py": "",
      "requirements.txt": "",
      ".gitignore": ""
    }
  }
```

#### Command

```sh
dirmap write write_template.json directory
```

## Development

### Running Tests

Tests are written using `pytest`. To run the tests:

1. Install the development dependencies:

```sh
pip install -e .[dev]
```

2. Run the tests:

```sh
pytest
```

## Troubleshooting

### Homebrew

If you have previously tapped and installed the dirmapper package, here’s how you can uninstall and untap it:

1. Uninstall the Package:

```sh
brew uninstall dirmapper
```

2. Untap the Repository:

```sh
brew untap nashdean/dirmap
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue on GitHub.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Author

**Nash Dean**
- [GitHub](https://github.com/nashdean)
- [Email](mailto:nashdean.github@gmail.com)

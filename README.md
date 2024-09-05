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
- Support for various output styles and formats.


## Installation

### Using Homebrew

You can install `dirmapper` using Homebrew:

```sh
brew tap nashdean/dirmap
brew install dirmapper
```

If you have previously tapped and installed the dirmapper package, here’s how you can uninstall and untap it:

1. Uninstall the Package:

```sh
brew uninstall dirmapper
```

2. Untap the Repository:

```sh
brew untap nashdean/dirmap
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

# Usage

## READ COMMANDS
### Basic Usage

To generate a directory structure mapping:

```sh
dirmap read /path/to/root_directory /path/to/output_file
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

You can now include complex regex patterns in your `.mapping-ignore` file:

```
.git/
.*cache
regex:^.*\.log$
```
This file can be overridden by specifying your own *.mapping-ignore* file (named anything you want) using the flag specified earlier `--ignore_file /path/to/.mapping-ignore`.

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

### Specify Output Style and Format

You can specify the style and format of the output using `--style` and `--format` options. Available styles include `tree`, `indentation`, `flat_list`, `markdown`, `html`, and `json`. Available formats include `plain`, `html`, and `json`.

#### Example: HTML Style with HTML Format

```sh
dirmap read /path/to/root_directory /path/to/output_file --style html --format html
```

#### Running All Styles with Their Respective Formats

```sh
mkdir -p ./style_outputs
dirmap . ./style_outputs/indentation_output.txt --sort asc --style indentation
dirmap . ./style_outputs/flat_list_output.txt --sort asc --style flat_list
dirmap . ./style_outputs/html_output.html --sort asc --style html --format html
dirmap . ./style_outputs/json_output.json --sort asc --style json --format json
dirmap . ./style_outputs/markdown_output.md --sort asc --style markdown
dirmap . ./style_outputs/tree_output.txt --sort asc --style tree
```
## WRITE COMMANDS
### Writing Directory Structure from a Template

To create a directory structure from a template file (YAML or JSON):

#### JSON
**Sample Template (JSON)**
__write_template.json__
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

Enter the following command to write a JSON template to a specific directory.
```sh
dirmap write write_template.json /path/to/root_directory
```

#### YAML
**Sample Template (YAML)**
__write_template.yaml__
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

Enter the following command to write a YAML template to a specific directory.
```sh
dirmap write write_template.yaml directory
```

### Writing Directory Structure from a Text File

To create a directory structure from a text file with the directory map/structure:

```sh
dirmap write /path/to/directory_map.txt /path/to/root_directory
```

This will create the directories and files for a given text file that follows the same output format from the `read` command. For example, if the below example was in a text file, the above write command would take that formatted directory structure/map and turn it into an actual directory with subfolders and files.

`directory_map.txt`
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
├── .mapping-ignore
└── README.md
```

**Output**
The Write command specifying the path to the example file `directory_map.txt` would create a root directory __project/__ with empty files __.mapping-ignore__ and __README.md__ and subfolders __.git/__, __.github__, and __src/__ followed by the contents of these subfolders. This generated directory structure would be generated at `/path/to/root_directory`.

### Writing a Directory Structure from a Text File and outputting a template

You may also decide it would be useful to create a template file while creating a directory with the specified subfolders and files. This could be useful if you had to share the workflow for creating a directory structure with a service/component that reads YAML or JSON (or if you wanted to share it with a team). You can do this with the `--template` flag.

```sh
dirmap write /path/to/directory_map.txt /path/to/root_directory --template
```

This outputs a JSON template called `generated_template.json` by default to the root directory. You may change the name of this template if you wish and are allowed to output to YAML.

For example, `dirmap write /path/to/directory_map.txt /path/to/root_directory --template my_template.yaml` will create a template called `my_template.yaml` instead of the default.

### 
## Example

**Sample Directory Structure**

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
├── .mapping-ignore
└── README.md
```

**Sample .mapping-ignore**

```
.git/
.github/
```

**Command to read the directory structure:**

```sh
dirmap read project output.txt --ignore_file project/.mapping-ignore
```

**Sample output from running above command in example:**

```
project/
├── src/
│   ├── main.py
│   └── utils.py
└── README.md
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

Coming soon...

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue on GitHub.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Author

**Nash Dean**
- [GitHub](https://github.com/nashdean)
- [Email](mailto:nashdean.github@gmail.com)
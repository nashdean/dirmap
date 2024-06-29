# Dirmapper

**Dirmapper** is a CLI tool to generate a directory structure mapping. It provides a visual representation of the directory and file structure, similar to the `tree` command, with support for `.gitignore`-like patterns to exclude specific files and directories.

## Features

- Generate a hierarchical view of a directory structure.
- Support for `.mapping-ignore` file to exclude files and directories.
- Optional integration with `.gitignore` to exclude patterns specified in `.gitignore`.

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
dirmap /path/to/root_directory /path/to/output_file
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
dirmap /path/to/root_directory /path/to/output_file --ignore_file /path/to/.mapping-ignore
```

**NOTE**: By default, the CLI ships with a `.mapping-ignore` file that will ignore the following:
```
.git/
```
This file can be overriden by specifiying your own *.mapping-ignore* file (named anything you want) using the flag specified earlier `--ignore_file /path/to/.mapping-ignore`.

### Disable .gitignore Integration

By default, `dirmap` will also consider patterns in `.gitignore`. To disable this feature:

```sh
dirmap /path/to/root_directory /path/to/output_file --ignore_file /path/to/.mapping-ignore --no_gitignore
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
dirmap project output.txt --ignore_file project/.mapping-ignore
```

### Sample Output

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

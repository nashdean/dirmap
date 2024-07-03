# Define the paths
PYPROJECT_TOML = pyproject.toml
SRC_DIR = src

# Extract the version from pyproject.toml
VERSION = $(shell grep -oE 'version = "[^"]+"' $(PYPROJECT_TOML) | sed -E 's/version = "(.*)"/\1/')

# Define the package name
PACKAGE_NAME = dirmapper

.PHONY: build clean install uninstall reinstall

build: clean
	@echo "Building the package..."
	python -m build

clean:
	@echo "Cleaning build artifacts..."
	rm -rf build dist $(SRC_DIR)/*.egg-info

install: build
	@echo "Installing the package..."
	pip install dist/$(PACKAGE_NAME)-$(VERSION)-py3-none-any.whl

uninstall:
	@echo "Uninstalling the package..."
	yes | pip uninstall $(PACKAGE_NAME)

reinstall: uninstall install
	@echo "Reinstalling the package..."

run:
	@echo "Running test `dirmap` call"
	dirmap --version
	dirmap . directory_structure.txt

run-asc:
	@echo "Running test `dirmap` call --sort asc"
	dirmap --version
	dirmap . directory_structure.txt --sort asc

run-all-styles:
	@echo "Running Styles Output Test"
	dirmap --version
	mkdir -p ./style_outputs
	@echo "Running test  indentation test."
	dirmap . ./style_outputs/indentation_output.txt --sort asc --style indentation
	@echo "Running test  flat_list test."
	dirmap . ./style_outputs/flat_list_output.txt --sort asc --style flat_list
	@echo "Running test  html test."
	dirmap . ./style_outputs/html_output.html --sort asc --style html --format html
	@echo "Running test  json test."
	dirmap . ./style_outputs/json_output.json --sort asc --style json --format json
	@echo "Running test  markdown test."
	dirmap . ./style_outputs/markdown_output.md --sort asc --style markdown
	@echo "Running test  tree test."
	dirmap . ./style_outputs/tree_output.txt --sort asc --style tree


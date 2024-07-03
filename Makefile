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

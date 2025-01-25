#!/usr/bin/env just --justfile

# Show all available recipes (default)
default:
    #!/usr/bin/env python3
    import re
    with open('justfile', 'r') as f:
        content = f.read()
    for match in re.finditer(r'^([a-zA-Z_-]+)(\s*.*?)#\*?\s*(.*)$', content, re.MULTILINE):
        recipe, _, desc = match.groups()
        if not recipe.startswith('_'):
            print(f'\033[36m{recipe:<20}\033[0m {desc}')

# Install the virtual environment and install the pre-commit hooks
install: # Install the virtual environment and install the pre-commit hooks
    @echo "🚀 Creating virtual environment using uv"
    uv sync
    uv run pre-commit install

# Run code quality tools
check: #* Run code quality tools
    @echo "🚀 Checking lock file consistency with 'pyproject.toml'"
    uv lock --locked
    @echo "🚀 Linting code: Running pre-commit"
    uv run pre-commit run -a
    @echo "🚀 Static type checking: Running mypy"
    uv run mypy
    @echo "🚀 Checking for obsolete dependencies: Running deptry"
    uv run deptry .

# Test the code with pytest
test: #* Test the code with pytest
    @echo "🚀 Testing code: Running pytest"
    uv run python -m pytest --cov --cov-config=pyproject.toml --cov-report=xml

# Clean build artifacts
clean-build: #* Clean build artifacts
    @echo "🚀 Removing build artifacts"
    uv run python -c "import shutil; import os; shutil.rmtree('dist') if os.path.exists('dist') else None"

# Build wheel file
build: clean-build #* Build wheel file
    @echo "🚀 Creating wheel file"
    uvx --from build pyproject-build --installer uv

# Publish a release to PyPI
publish: #* Publish a release to PyPI
    @echo "🚀 Publishing"
    uvx twine upload --repository-url https://upload.pypi.org/legacy/ dist/*

# Build and publish
build-and-publish: build publish #* Build and publish
